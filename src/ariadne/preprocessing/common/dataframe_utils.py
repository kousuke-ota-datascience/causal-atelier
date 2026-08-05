import pandas as pd
import numpy as np
import yaml
import pickle

import re

from multiprocessing import Pool

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

matplotlib.rcParams['font.family'] = 'IPAexGothic'

class DataHandleUtils_Exception(Exception): 
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg


class DataHandleUtils(): 
    """
    File IO 以外のデータ操作でも使うか否か？という基準で、FileIOUtils から切り分ける
    """
    def __init__(self, logger):
        self._logger=logger


    def recurcive_update_dict(self, ret_dict, **kwargs):
        try: 
            for k, v in kwargs.items():
                if isinstance(v, dict):
                    self.recurcive_update_dict(ret_dict[k], **kwargs[k])
                else:
                    ret_dict.update(kwargs)
                    return 
        except Exception as e: 
            self._logger.error("k:{}, v:{}".format(k, v))
            self._logger.error(e, exc_info=True)
            raise
    ## end ; def recurcive_update_dict(self, ret_dict, **kwargs):
    

    def recurcive_pop_key(self, ret_dict, **kwargs):
        try: 
            for k, v in kwargs.items():
                if isinstance(v, dict):
                    ret_dict[k]={}
                    self.recurcive_pop_key(ret_dict[k], **kwargs[k])
                else:
                    ret_dict.update(dict.fromkeys(kwargs, None))
                    return 
        except Exception as e: 
            self._logger.error(e, exc_info=True)
            raise
    ## end ; def recurcive_update_dict(self, ret_dict, **kwargs):

    
    def get_filter_cond(self, df, filter_cond): 
        try: 
            df_out = df.reset_index().drop(['index'], axis=1)
            df_dtype = pd.DataFrame(df_out.dtypes, columns=['dtype'])

            cond_tmp = pd.Series([True for s in df_out.index])
            for clnm, value_list in filter_cond.items():
                if df_dtype.loc[clnm, 'dtype'] in ['datetime64[ns]', 'float64', 'int64']: 
                    cond_tmp = cond_tmp & ((value_list[0] <= df_out.loc[:, clnm]) & (df_out.loc[:, clnm] <= value_list[1]))
                else : 
                    cond_tmp = cond_tmp & df_out.loc[:, clnm].isin(pd.Series(value_list, dtype="object"))
            ## end ; for clnm, value_list in filter_cond.items():

            return cond_tmp
        except Exception as e: 
            self._logger.error("clnm:{}, value_list:{}".format(clnm, value_list))
            self._logger.error(e, exc_info=True)
            raise


    def get_filtered_df(self, df, filter_cond): 
        try: 
            df_out = df.reset_index().drop(['index'], axis=1)
            df_out = df_out.loc[self.get_filter_cond(df_out, filter_cond), :].reset_index().drop(['index'], axis=1)
            return df_out
        except Exception as e: 
            self._logger.error(e, exc_info=True)
            raise
    
    
    def get_filter_cond_re_to_series(self, tgt_series, re_exps, logical_operation="OR"): 
        try: 
            if logical_operation == "OR": 
                cond_match = pd.Series([False for s in tgt_series])
            elif logical_operation == "AND": 
                cond_match = pd.Series([True for s in tgt_series])
            else: 
                msg = "logical_operation must be AND or OR"
                raise DataHandleUtils_Exception(msg)
            
            for i1, re_exp in enumerate(re_exps): 
            
                cond_tmp = tgt_series.str.contains(re_exp)
                ## extract = tgt_series.str.extract(re_exp, expand=False)
                
                if logical_operation == "OR": 
                    cond_match = cond_match | cond_tmp
                elif logical_operation == "AND": 
                    cond_match = cond_match & cond_tmp
                else: 
                    cond_match = cond_match
            ## end ; for i1, re_exp in enumerate(re_exps): 
            
            return cond_match

        except Exception as e: 
            self._logger.error(e, exc_info=True)
            raise

    
    def get_replaced_str(self, in_str, replace_def): 
        try: 
            out_str  = in_str
            for k, v in replace_def.items():
                out_str = out_str.replace(k, v)    

            return out_str
        except Exception as e: 
            self._logger.error(e, exc_info=True)
            raise


    def get_digit(self, in_value): 

        abs_in_value=abs(in_value)
        sign = np.log10(abs_in_value)/abs(np.log10(abs_in_value))

        if abs_in_value==0: 
            digit_abs = 0
        else: 
            digit_abs = abs(int(np.log10(abs_in_value)))

        return sign*(digit_abs+1)            


    def get_formatted_float_with_digit_number(self, float_value, digit=None): 

        if digit is None: 
            digit = self.get_digit(float_value)

        if digit<0: 
            if digit<=-6: 
                str_grp_name="{:,.06f}".format(float_value)
            elif digit<=-5: 
                str_grp_name="{:,.05f}".format(float_value)
            elif digit<=-4: 
                str_grp_name="{:,.04f}".format(float_value)
            elif digit<=-3: 
                str_grp_name="{:,.03f}".format(float_value)
            elif digit<=-2: 
                str_grp_name="{:,.02f}".format(float_value)
            elif digit<=-1: 
                str_grp_name="{:,.01f}".format(float_value)
            else: 
                str_grp_name="{:,.00f}".format(float_value)        
        else: 
            str_grp_name="{:,.00f}".format(float_value)

        return str_grp_name

    
    def get_columns_order_swapped_df(self, df, clnms_to_be_left): 
        try: 
            cond_ = df.columns.isin(clnms_to_be_left)
            clnms_complements = df.columns[~cond_].tolist()
            clnms_left_actual = df.columns[cond_].tolist()

            return df.loc[:, clnms_left_actual+clnms_complements].reset_index(drop=True)
        except Exception as e: 
            self._logger.error(e, exc_info=True)
            raise

    ## 2024/01/20 add -- start --
    def split_df_by_column_value(self, df_in, clnm_split_criteria): 
        try: 
            original_column_order = df_in.columns
            df_tmp = df_in.sort_values([clnm_split_criteria]).set_index([clnm_split_criteria])
            unique_val = df_in.loc[:, clnm_split_criteria].unique().tolist()

            ret_dict = {v:df_tmp.loc[v, :].reset_index().loc[:, original_column_order] for v in unique_val}            
            
            return ret_dict
        except Exception as e: 
            self._logger.error(e, exc_info=True)
            raise
    ## 2024/01/20 add --  end  --

    ## 2024/02/04 add -- start --
    def split_df_by_multi_column_value(self, df_in, clnms_split_criteria): 
        try: 
            original_column_order = df_in.columns
            df_tmp = df_in.sort_values(clnms_split_criteria).set_index(clnms_split_criteria)
            
            df_unique_val_set = df_in.loc[:, clnms_split_criteria].drop_duplicates().sort_values(clnms_split_criteria)
            unique_val_set = [tuple(row_i1) for i1, row_i1 in df_unique_val_set.iterrows()]

            ret_dict = {v:df_tmp.loc[v, :].reset_index().loc[:, original_column_order] for v in unique_val_set}            
            
            return ret_dict
        except Exception as e: 
            self._logger.error(e, exc_info=True)
            raise
    ## 2024/02/04 add --  end  --


    def get_substituted_prm_in_out_dict(self, prm_dict, re_replace_dict):
        try: 
            ret_dict = prm_dict.copy()
            for k, v in re_replace_dict.items(): 

                re_exp="{"+k+"}"
                re_replace=v

                if "path" in ret_dict["file"].keys(): 
                    ret_dict["file"]["path"] = re.sub(re_exp, re_replace, ret_dict["file"]["path"])

                if "names" in ret_dict["file"].keys(): 
                    ret_dict["file"]["names"] = pd.Series(
                        ret_dict["file"]["names"]
                    ).map(lambda s:re.sub(re_exp, re_replace, s)).tolist()

                elif "name" in ret_dict["file"].keys(): 
                    ret_dict["file"]["name"] = re.sub(re_exp, re_replace, ret_dict["file"]["name"])
                else: 
                    raise DataConverter_Exception("name or names please")
            ## end ; for k, v in re_replace_dict.items(): 

            return ret_dict
        except Exception as e: 
            err_msg=""
            self._logger.error(err_msg)
            self._logger.error(e, exc_info=True)
            raise

    
    def get_random_alphabet_str(self, dummy_args, length=5): 
        try: 
            alphabets_lower = [chr(ord("a")+s) for s in range(0, 26, 1)]
            alphabets_upper = [chr(ord("A")+s) for s in range(0, 26, 1)]
            numbers = [s for s in range(0, 10, 1)]
            
            ret_str = "".join([np.random.choice(alphabets_lower+alphabets_upper+numbers) for t in range(0, length, 1)])
            
            return ret_str
        except Exception as e: 
            err_msg=""
            self._logger.error(err_msg)
            self._logger.error(e, exc_info=True)
            raise
    
    
    def soft_drop_columns(self, df, del_clnms): 
        try: 
            cond = df.columns.isin(del_clnms)
            clnms_remain = df.columns[~cond]
            
            return df.loc[:, clnms_remain]
        except Exception as e: 
            err_msg=""
            self._logger.error(err_msg)
            self._logger.error(e, exc_info=True)
            raise
    
    


