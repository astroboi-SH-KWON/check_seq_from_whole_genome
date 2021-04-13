
from astroboi_bio_tools.ToolLogic import ToolLogics


import Util


class Logics(ToolLogics):
    def __init__(self, init, spcr_dict, trncrpt_dict):

        super().__init__()
        self.ref_dir = init[0]
        self.pam_rule = init[1]
        self.len_sprcr = init[2]

        self.spacer_info_dict = spcr_dict
        self.trncrpt_rgin_dict = trncrpt_dict

    def is_trnscprted(self, st_pos, en_pos, trncrpt_list):
        for trnscrpt_arr in trncrpt_list:
            if trnscrpt_arr[0] <= st_pos and en_pos <= trnscrpt_arr[1]:
                return True
        return False

    def get_cnt_of_True(self, idx_inf_arr):
        cnt = 0
        for tmp_str in idx_inf_arr:
            if "True" in tmp_str:
                cnt += 1
        return cnt

    def check_spcr_from_whole_gen_by_chr(self, chr_nm_arr):
        print("st check_spcr_from_whole_gen_by_chr")
        result_dict = {}
        for chr_nm in chr_nm_arr:
            print("ref :", chr_nm)
            util = Util.Utils()
            p_seq, m_seq = util.read_file_by_biopython(self.ref_dir + chr_nm + ".fa", "fasta")
            for i in range(len(p_seq)):
                p_spacr = p_seq[i: i + self.len_sprcr]
                m_spacr = m_seq[i: i + self.len_sprcr][::-1]

                if "N" in p_spacr or "N" in m_spacr:
                    continue

                if p_spacr in self.spacer_info_dict:
                    p_pam = p_seq[i + self.len_sprcr: i + self.len_sprcr + len(self.pam_rule)]
                    if "N" not in p_pam:
                        if self.match(0, p_pam, self.pam_rule):
                            st_pos = i
                            en_pos = i + self.len_sprcr + len(self.pam_rule)
                            if self.is_trnscprted(st_pos, en_pos, self.trncrpt_rgin_dict[chr_nm]):
                                if p_spacr in result_dict:
                                    result_dict[p_spacr].append(chr_nm + ":" + str(st_pos) + "-" + str(en_pos) + ":+:True")
                                else:
                                    result_dict.update(
                                        {p_spacr: [chr_nm + ":" + str(st_pos) + "-" + str(en_pos) + ":+:True"]})
                            else:
                                if p_spacr in result_dict:
                                    result_dict[p_spacr].append(chr_nm + ":" + str(st_pos) + "-" + str(en_pos) + ":+:False")
                                else:
                                    result_dict.update(
                                        {p_spacr: [chr_nm + ":" + str(st_pos) + "-" + str(en_pos) + ":+:False"]})

                if m_spacr in self.spacer_info_dict:
                    m_pam = m_seq[i - len(self.pam_rule): i][::-1]
                    if "N" not in m_pam:
                        if self.match(0, m_pam, self.pam_rule):
                            st_pos = i - len(self.pam_rule)
                            en_pos = i + self.len_sprcr
                            if self.is_trnscprted(st_pos, en_pos, self.trncrpt_rgin_dict[chr_nm]):
                                if m_spacr in result_dict:
                                    result_dict[m_spacr].append(chr_nm + ":" + str(st_pos) + "-" + str(en_pos) + ":-:True")
                                else:
                                    result_dict.update(
                                        {m_spacr: [chr_nm + ":" + str(st_pos) + "-" + str(en_pos) + ":-:True"]})
                            else:
                                if m_spacr in result_dict:
                                    result_dict[m_spacr].append(chr_nm + ":" + str(st_pos) + "-" + str(en_pos) + ":-:False")
                                else:
                                    result_dict.update(
                                        {m_spacr: [chr_nm + ":" + str(st_pos) + "-" + str(en_pos) + ":-:False"]})
            print("DONE ref :", chr_nm)
        print("DONE check_spcr_from_whole_gen_by_chr")
        return result_dict
