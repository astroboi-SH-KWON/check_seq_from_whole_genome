
from astroboi_bio_tools.ToolLogicPrep import ToolLogicPreps

import Logic


class LogicPreps(ToolLogicPreps):
    def make_list_to_dict_by_ele_key(self, data_list, key_idx):
        result_dict = {}
        for tmp_arr in data_list:
            key = tmp_arr[key_idx]
            if key in result_dict:
                print("Duple!!!!!!!!!!!!!!!!!!!!!!!", tmp_arr)
            else:
                result_dict.update({key: tmp_arr})
        return result_dict

    def make_freq_result_list(self, logic, result_dict, spacer_info_dict):
        result_list = []
        for spcr, spcr_info_arr in spacer_info_dict.items():
            result_arr = []
            result_arr.extend(spcr_info_arr)
            if spcr in result_dict:
                idx_inf_arr = result_dict[spcr]
                result_arr.append(len(idx_inf_arr))
                num_trnscrpt = logic.get_cnt_of_True(idx_inf_arr)
                result_arr.append(num_trnscrpt)
            else:
                result_arr.append(0)
                result_arr.append(0)
            result_list.append(result_arr)
        # for spcr, idx_inf_arr in result_dict.items():
        #     result_arr = []
        #     result_arr.extend(spacer_info_dict[spcr])
        #
        #     result_arr.append(len(idx_inf_arr))
        #     num_trnscrpt = logic.get_cnt_of_True(idx_inf_arr)
        #     result_arr.append(num_trnscrpt)
        #     result_list.append(result_arr)
        return result_list

    def make_dict_to_list(self, result_dict, spcr_info_dict):
        result_list = []
        for spcr, spcr_info_arr in spcr_info_dict.items():
            result_arr = [spcr_info_arr[0], spcr]
            tmp_str = ""
            if spcr in result_dict:
                for idx_inf in result_dict[spcr]:
                    tmp_str += idx_inf + ", "
            result_arr.append(tmp_str)
            result_list.append(result_arr)

        # for spcr, idx_inf_arr in result_dict.items():
        #     result_arr = [spcr_info_dict[spcr][0], spcr]
        #     tmp_str = ""
        #     for idx_inf in idx_inf_arr:
        #         tmp_str += idx_inf + ", "
        #     result_arr.append(tmp_str)
        #     result_list.append(result_arr)
        return result_list

    def get_trncrpt_rgin_by_chr(self, cds_list):
        result_dict ={}
        for cds_arr in cds_list:
            chr_key = cds_arr[2]
            if chr_key in result_dict:
                result_dict[chr_key].append([int(cds_arr[4]), int(cds_arr[5])])
            else:
                result_dict.update({chr_key: [[int(cds_arr[4]), int(cds_arr[5])]]})
        return result_dict

    def make_pool_list_to_dict(self, pool_list):
        tot_result_dict = {}
        for tmp_dict in pool_list:
            for spcr, idx_inf_arr in tmp_dict.items():
                if spcr in tot_result_dict:
                    tot_result_dict[spcr].extend(idx_inf_arr)
                else:
                    tot_result_dict.update({spcr: idx_inf_arr})
        return tot_result_dict
