#!/usr/bin/env python3
"""Non-confirmatory AR algebra cross-check for E11 B0/B1 (NOT science PASS).

Review-only: independent algebraic moment formula vs an OLS HC1 null-test API.
A pilot of the *candidate* HC1/chi-square approach, not a final independent
methodology approval, library/API approval, or Monte Carlo coverage claim.
"""
from __future__ import annotations
import hashlib
import json
import numpy as np
import statsmodels.api as sm
from scipy.stats import chi2

SEED = 20261122

def fixture(b1: bool, seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n = 512
    z = np.array([0.0, 1.0] * (n // 2))
    rng.shuffle(z)
    c = rng.normal(size=n) if b1 else np.empty((n, 0))
    u = rng.normal(size=n)
    a = (0.95 * z + 0.6 * u + (0.3 * c if b1 else 0.0)
         + rng.normal(size=n) > 0.7).astype(float)
    beta = 1.4 if b1 else 2.0
    y = beta * a + 0.7 * c * int(b1) + 0.7 * u + rng.normal(scale=0.45, size=n) if b1 else beta * a + 0.7 * u + rng.normal(scale=0.45, size=n)
    q = np.column_stack((np.ones(n), c)) if b1 else np.ones((n, 1))
    return y, a, z, q

def moments(y: np.ndarray, a: np.ndarray, z: np.ndarray, q: np.ndarray):
    n = len(y)
    x = np.column_stack((q, z))
    assert np.linalg.matrix_rank(q) == q.shape[1]
    assert np.linalg.matrix_rank(x) == x.shape[1]
    assert n > x.shape[1]
    z_t = z - q @ np.linalg.lstsq(q, z, rcond=None)[0]
    e_y = y - x @ np.linalg.lstsq(x, y, rcond=None)[0]
    e_a = a - x @ np.linalg.lstsq(x, a, rcond=None)[0]
    g_y, g_a = np.dot(z_t, y), np.dot(z_t, a)
    h = n / (n - x.shape[1])
    s0 = np.sum(z_t**2 * e_y**2)
    s1 = np.sum(z_t**2 * e_y * e_a)
    s2 = np.sum(z_t**2 * e_a**2)
    ccrit = chi2.ppf(0.95, 1)
    coeff = (g_a**2 - ccrit * h * s2,
             -2 * g_y * g_a + 2 * ccrit * h * s1,
             g_y**2 - ccrit * h * s0)
    return (z_t, e_y, e_a, g_y, g_a, h, s0, s1, s2, ccrit, coeff)

def check(b1: bool, seed: int) -> dict:
    y, a, z, q = fixture(b1, seed)
    zt, ey, ea, gy, ga, h, s0, s1, s2, ccrit, coef = moments(y, a, z, q)
    x = np.column_stack((q, z))
    beta_hat = gy / ga
    max_error = 0.0
    test_cases = [float(beta_hat), -5., -2., 0., 1.4, 2., 5., 20.]
    for beta in test_cases:
        r = y - beta * a
        fit = sm.OLS(r, x).fit(cov_type='HC1')
        t_sm = float((fit.params[-1] / fit.bse[-1]) ** 2)
        residual_var_numerator = h * np.sum(zt**2 * (ey - beta * ea)**2)
        t_moment = float((gy - beta * ga)**2 / residual_var_numerator)
        q_poly = (coef[0] * beta + coef[1]) * beta + coef[2]
        q_direct = (gy - beta * ga)**2 - ccrit * residual_var_numerator
        max_error = max(max_error, abs(t_sm - t_moment), abs(q_poly-q_direct))
        assert np.isclose(t_sm, t_moment, rtol=5e-10, atol=5e-10), (b1, beta, t_sm, t_moment)
        assert np.isclose(q_poly, q_direct, rtol=5e-10, atol=5e-8), (b1, beta, q_poly, q_direct)
    point = float(beta_hat)
    t_at_point = float((gy - point * ga)**2 / (h * np.sum(zt**2 * (ey-point*ea)**2)))
    assert abs(t_at_point) < 1e-20
    return {'variant':'B1' if b1 else 'B0','n':len(y),'k':x.shape[1],
            'seed':seed,'true_structural_beta':1.4 if b1 else 2.,
            'sample_wald_2sls_beta':point,'first_stage_gA':float(ga),
            't_ar_at_ratio':t_at_point,'q_coefficients':list(map(float,coef)),
            'num_evaluations':len(test_cases),'max_absolute_algebra_error':max_error}

def zero_first_stage_topology() -> dict:
    """Synthetic algebraic stress fixture; deliberately NOT a valid causal IV DGP."""
    n = 128
    z = np.tile([0., 1., 0., 1.], n // 4)
    a = np.tile([1., 1., 0., 0.], n // 4)  # equal treatment means in both Z arms
    y = 3. * z + 0.05 * np.sin(np.arange(n) * 0.3)  # violates IV exclusion: geometry only
    q = np.ones((n, 1))
    zt, ey, ea, gy, ga, h, s0, s1, s2, crit, coefficients = moments(y, a, z, q)
    assert abs(ga) < 1e-11
    q2, q1, q0 = coefficients
    discr = q1 * q1 - 4 * q2 * q0
    assert q2 < 0 and discr > 0 and q0 > 0
    assert np.polyval(coefficients, -100) < 0 < np.polyval(coefficients, 0)
    assert np.polyval(coefficients, 100) < 0
    roots = np.sort(np.roots(coefficients))
    assert np.isrealobj(roots) and roots[0] < 0 < roots[1]
    for beta in [-100., 0., 100.]:
        stat = (gy-beta*ga)**2 / (h*np.sum(zt**2*(ey-beta*ea)**2))
        assert (stat <= crit) == (np.polyval(coefficients,beta) <= 0)
    return {'case':'ZERO_FIRST_STAGE_TWO_RAYS', 'n':n,
            'first_stage_gA':float(ga),'point_ratio':'NOT_AVAILABLE',
            'AR_topology':'TWO_UNBOUNDED_RAYS',
            'roots':[float(z) for z in roots],
            'identification_validity':'FALSE; intentionally invalid exclusion; topology only'}

if __name__ == '__main__':
    result={'status':'NONCONFIRMATORY_ALGEBRA_CHECK', 'candidate':'HC1_CHI2_QUADRATIC_AR',
            'tests':[check(False,SEED),check(True,SEED+1)],
            'geometry_adversary': zero_first_stage_topology(),
            'limitations':['Python 3.13 review-only, not Python 3.12 target',
                'Neither a separate reviewer nor a frozen reference implementation',
                'No calibrated coverage, weak-IV Monte Carlo, T2/T3 or exhaustive topology verification',
                'Nominal 0.95 is illustrative; not preregistered T3 decision threshold'],
            'python_script_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    print(json.dumps(result,ensure_ascii=False,indent=2))
