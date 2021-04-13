import time
import os
# from Bio import SeqIO
import multiprocessing as mp
import numpy as np
import platform

import Util
import Logic
import LogicPrep
#################### st env ####################
WORK_DIR = os.getcwd() + "/"
PROJECT_NAME = WORK_DIR.split("/")[-2]
SYSTEM_NM = platform.system()

if SYSTEM_NM == 'Linux':
    # REAL
    REF_DIR = "/extdata1/reference/hg38/Splited/"  #B206
    pass
else:
    # DEV
    WORK_DIR = "D:/000_WORK/ParkJiHye/20210330/WORK_DIR/"
    REF_DIR = "D:/000_WORK/000_reference_path/human/hg38/Splited/"

IN = 'input/'
OU = 'output/'
HG38_REF_FLT = "filtered_hg38_refFlat.txt"
SPCR_ARR = [
            "20210405_TR_final-guide_list_n=2387_toKSH_PJH.csv"
            , "20210405_TE_final-guide_list_n=7403_toKSH_PJH.csv"
            ]

os.makedirs(WORK_DIR + IN, exist_ok=True)
os.makedirs(WORK_DIR + OU, exist_ok=True)

TOTAL_CPU = mp.cpu_count()
MULTI_CNT = int(TOTAL_CPU*0.8)

pam_rule = "NRG"
len_sprcr = 20
INIT = [REF_DIR, pam_rule, len_sprcr]
#################### en env ####################


def multi_process():
    util = Util.Utils()
    logic_prep = LogicPrep.LogicPreps()

    hg38_info = util.read_tsv_ignore_N_line(WORK_DIR + IN + HG38_REF_FLT)
    trncrpt_rgin_dict = logic_prep.get_trncrpt_rgin_by_chr(hg38_info)

    for spcr_fl in SPCR_ARR:
        spacer_info = util.read_tsv_ignore_N_line(WORK_DIR + IN + spcr_fl, deli_str=",")
        spacer_info_dict = logic_prep.make_list_to_dict_by_ele_key(spacer_info, 1)

        logic = Logic.Logics(INIT, spacer_info_dict, trncrpt_rgin_dict)

        chr_list = ["chrX", "chrY"]
        for i in range(1, 23):
            chr_list.append("chr" + str(i))
        # divide data_list by MULTI_CNT
        proc_cnt = min(MULTI_CNT, len(chr_list))
        splited_chr_list = np.array_split(chr_list, proc_cnt)
        print("platform.system() : ", SYSTEM_NM)
        print("total cpu_count : ", str(TOTAL_CPU))
        print("will use : ", str(proc_cnt))
        pool = mp.Pool(processes=proc_cnt)

        pool_list = pool.map(logic.check_spcr_from_whole_gen_by_chr, splited_chr_list)

        result_dict = logic_prep.make_pool_list_to_dict(pool_list)
        pool.close()
        pool_list[:] = []

        result_1_list = logic_prep.make_freq_result_list(logic, result_dict, spacer_info_dict)
        result_1_list = logic_prep.sort_list_by_ele(result_1_list, 0, False)

        result_2_list = logic_prep.make_dict_to_list(result_dict, spacer_info_dict)
        result_2_list = logic_prep.sort_list_by_ele(result_2_list, 0, False)

        header = ["Transposable element", "spacer (20 bp)", "#duple", "#trscprt", "#freq_align", "#trscprt_align"]
        util.make_tsv(WORK_DIR + OU + spcr_fl.replace(".csv", "") + "_result_1_list.txt", header, result_1_list)
        result_1_list.clear()

        header = ["Transposable element", "spacer (20 bp)", "index"]
        util.make_tsv(WORK_DIR + OU + spcr_fl.replace(".csv", "") + "_result_2_list.txt", header, result_2_list)
        result_2_list.clear()


if __name__ == '__main__':
    start_time = time.perf_counter()
    print("start [ " + PROJECT_NAME + " ]>>>>>>>>>>>>>>>>>>")
    multi_process()
    print("::::::::::: %.2f seconds ::::::::::::::" % (time.perf_counter() - start_time))