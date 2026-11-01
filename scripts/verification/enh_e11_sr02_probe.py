#!/usr/bin/env python3
"""ENH-E11 SR-02: backend API probes only, not scientific acceptance."""
import argparse
import importlib.metadata as md
import json
import os
import platform
import subprocess
import sys
import time
import traceback
from pathlib import Path

PACKAGES = ["numpy","pandas","scipy","scikit-learn","statsmodels","causal-learn",
            "lingam","dowhy","econml","tigramite"]

def probe(rows, name, f):
    start=time.monotonic()
    try:
        details=f() or {}
        rows.append({"method":name,"status":"PASS","details":details,
                     "seconds":round(time.monotonic()-start,2)})
    except Exception as e:
        rows.append({"method":name,"status":"FAIL","error":type(e).__name__,
                     "reason":str(e)[:450],"traceback":traceback.format_exc()[-900:],
                     "seconds":round(time.monotonic()-start,2)})

def dowhy(rows):
    import numpy as np
    import pandas as pd
    from dowhy import CausalModel
    rng=np.random.default_rng(11)
    n=250
    x=rng.normal(size=n);z=rng.normal(size=n)
    t=.8*x+.7*z+rng.normal(size=n)
    m=.8*t+rng.normal(size=n)
    y=1.4*t+.6*x+.6*m+rng.normal(size=n)
    df=pd.DataFrame({"X":x,"Z":z,"T":t,"M":m,"Y":y})
    def identify(graph,field):
        model=CausalModel(data=df,treatment="T",outcome="Y",graph=graph)
        found=model.identify_effect(proceed_when_unidentifiable=True)
        value=getattr(found,field,None)
        if value is None or value==[] or value=={}:
            raise AssertionError("No "+field+": "+str(found)[:300])
        return {"identified":str(value)[:200]}
    probe(rows,"DoWhy Backdoor identify",lambda:identify(
        "digraph {X -> T; X -> Y; T -> Y;}","backdoor_variables"))
    probe(rows,"DoWhy Frontdoor identify",lambda:identify(
        "digraph {T -> M; M -> Y; U -> T; U -> Y;}","frontdoor_variables"))
    probe(rows,"DoWhy IV identify",lambda:identify(
        "digraph {Z -> T; T -> Y; U -> T; U -> Y;}","instrumental_variables"))
    def estimate():
        model=CausalModel(data=df,treatment="T",outcome="Y",
                          graph="digraph {X -> T; X -> Y; T -> Y;}")
        v=float(model.estimate_effect(model.identify_effect(),
                                     method_name="backdoor.linear_regression").value)
        if not np.isfinite(v): raise AssertionError("nonfinite")
        return {"effect":v}
    probe(rows,"DoWhy Backdoor estimate",estimate)

def econml(rows):
    import numpy as np
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import LogisticRegression
    from econml.dml import LinearDML,CausalForestDML
    from econml.dr import DRLearner,ForestDRLearner
    from econml.metalearners import SLearner,TLearner,XLearner
    from econml.iv.dr import DRIV
    rng=np.random.default_rng(11);n=220
    X=rng.normal(size=(n,2));W=rng.normal(size=(n,2));Z=rng.normal(size=n)
    p=1/(1+np.exp(-(.5*X[:,0]+.4*W[:,0]+.7*Z)))
    T=(rng.uniform(size=n)<p).astype(int)
    Y=(1+.4*X[:,0])*T+.7*W[:,0]+rng.normal(size=n)
    Ti=.85*Z+.5*W[:,0]+rng.normal(size=n)
    Yi=(1.4+.25*X[:,0])*Ti+W[:,0]+rng.normal(size=n)
    rf=lambda:RandomForestRegressor(n_estimators=12,min_samples_leaf=5,
                                   random_state=11,n_jobs=1)
    def fit(e,iv=False,meta=False):
        kwargs={"X":X,"W":W}
        if iv:kwargs["Z"]=Z
        if meta:kwargs.pop("W")
        e.fit(Yi if iv else Y,Ti if iv else T,**kwargs)
        effect=np.asarray(e.effect(X[:5]),dtype=float)
        if not effect.size or not np.isfinite(effect).all():
            raise AssertionError("invalid effect")
        out={"shape":list(effect.shape),"mean":float(effect.mean())}
        try:
            a,b=e.effect_interval(X[:5])
            out["interval"]="FINITE" if np.isfinite(a).all() and np.isfinite(b).all() else "NONFINITE"
        except Exception as exc:
            out["interval"]="UNAVAILABLE_OR_FAILED:"+type(exc).__name__+":"+str(exc)[:110]
        return out
    methods=[
       ("LinearDML",lambda:LinearDML(model_y=rf(),model_t=rf(),cv=2,random_state=11),False,False),
       ("CausalForestDML",lambda:CausalForestDML(model_y=rf(),model_t=rf(),n_estimators=100,cv=2,random_state=11),False,False),
       ("DRLearner",lambda:DRLearner(model_propensity=LogisticRegression(max_iter=300),
                                   model_regression=rf(),model_final=rf(),cv=2),False,False),
       ("ForestDRLearner",lambda:ForestDRLearner(n_estimators=100,cv=2,random_state=11),False,False),
       ("SLearner",lambda:SLearner(overall_model=rf()),False,True),
       ("TLearner",lambda:TLearner(models=rf()),False,True),
       ("XLearner",lambda:XLearner(models=rf()),False,True),
       ("DRIV",lambda:DRIV(cv=2,prel_cv=2),True,False)]
    for name,ctor,iv,meta in methods:
        probe(rows,"EconML "+name,lambda ctor=ctor,iv=iv,meta=meta:fit(ctor(),iv,meta))

def tigramite(rows):
    import numpy as np
    from tigramite import data_processing as pp
    from tigramite.pcmci import PCMCI
    from tigramite.lpcmci import LPCMCI
    from tigramite.independence_tests.parcorr import ParCorr
    rng=np.random.default_rng(11)
    data=rng.normal(size=(320,3))
    for i in range(2,len(data)):
        data[i,0]+=.6*data[i-1,0]
        data[i,1]+=.55*data[i-1,0]+.4*data[i-1,1]
        data[i,2]+=.45*data[i-1,1]
    frame=pp.DataFrame(data,var_names=["X","Y","Z"])
    def inspect(out):
        if not isinstance(out,dict):raise AssertionError("non-dict output")
        result={"keys":list(out.keys())}
        graph=out.get("graph")
        if graph is None:raise AssertionError("missing graph field")
        arr=np.asarray(graph)
        if arr.ndim!=3 or arr.shape[:2]!=(3,3):
            raise AssertionError("graph shape "+str(arr.shape))
        result["shape"]=list(arr.shape)
        result["endpoints"]=sorted(set(str(v) for v in arr.ravel()))
        return result
    probe(rows,"Tigramite PCMCI",lambda:inspect(
        PCMCI(dataframe=frame,cond_ind_test=ParCorr()).run_pcmci(tau_max=2,pc_alpha=.1)))
    probe(rows,"Tigramite PCMCI+",lambda:inspect(
        PCMCI(dataframe=frame,cond_ind_test=ParCorr()).run_pcmciplus(tau_max=2,pc_alpha=.1)))
    probe(rows,"Tigramite LPCMCI",lambda:inspect(
        LPCMCI(dataframe=frame,cond_ind_test=ParCorr()).run_lpcmci(tau_max=2,pc_alpha=.1)))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--group",choices=["dowhy","econml","tigramite","combined"],required=True)
    parser.add_argument("--install-rc",type=int,default=0)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--summary",type=Path,required=True)
    a=parser.parse_args()
    tests={"dowhy":[dowhy],"econml":[econml],"tigramite":[tigramite],
           "combined":[dowhy,econml,tigramite]}
    rows=[]
    for test in tests[a.group]:
        try:test(rows)
        except Exception as exc:
            rows.append({"method":test.__name__+" module/import","status":"BLOCKED",
                        "error":type(exc).__name__,"reason":str(exc)[:400]})
    try:
        c=subprocess.run(["uv","pip","check","--python",sys.executable],
                         capture_output=True,text=True,timeout=30)
        deps={"return_code":c.returncode,"message":(c.stdout+c.stderr)[-1200:]}
    except Exception as exc:deps={"error":str(exc)}
    versions={}
    for p in PACKAGES:
        try:versions[p]=md.version(p)
        except md.PackageNotFoundError:versions[p]=None
    data={"classification":"INSTALL/API SMOKE only, not scientific validation",
          "group":a.group,"install_rc":a.install_rc,"os":platform.platform(),
          "python":sys.version,"versions":versions,"dependency_check":deps,"results":rows}
    a.output.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    lines=["### ENH-E11 SR-02 probe: "+a.group,
           "SHA: "+os.getenv("GITHUB_SHA","local"),
           "Environment: "+platform.platform()+" / Python "+sys.version.split()[0],
           "Install exit: "+str(a.install_rc)+", dependency check: "+str(deps.get("return_code","N/A")),
           "Versions: "+", ".join(f"{k}={v}" for k,v in versions.items() if v),
           "| Method | Status | Details |","|---|---|---|"]
    for row in rows:
        detail=str(row.get("reason",row.get("details",""))).replace("|","/").replace("\n"," ")[:240]
        lines.append("| "+row["method"]+" | "+row["status"]+" | "+detail+" |")
    lines.append("\n**Not science PASS. Not SR-02 closure.**")
    a.summary.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"group":a.group,"install_rc":a.install_rc,
                      "passed":sum(x["status"]=="PASS" for x in rows),
                      "not_pass":sum(x["status"]!="PASS" for x in rows)}))
if __name__=="__main__":
    main()
