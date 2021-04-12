# check_seq_from_whole_genome

    1. spacer (20bp): 아래 파일에서 가져오기
        a. 20210405_TE_final-guide_list_n=7403_toKSH_PJH.csv
        b. 20210405_TR_final-guide_list_n=2387_toKSH_PJH.csv
    2. #duple: Dfam, TRD에서 target sequence를 먼저 뽑은 다음, 여기서 unique한 spacer로 target할 수 있는 copy 정보 (예전 분석 결과)
    3. #trscprt: #duple에서 뽑힌 target site가 "filtered_hg38_refFlat.txt" 파일의 transcript_start, end 좌표 안에 들어가는지 여부 정보 (예전 분석 결과)
    4. #freq_align: 1번 spacer sequence를 hg38에 각각 align하여 NRG PAM으로 perfect match되는 locus의 개수
    5. #trscprt_align: #freq_align에서 뽑힌 target site가 "filtered_hg38_refFlat.txt" 파일의 transcript_start, end 좌표 안에 들어가는지 여부 정보
    6. index: "20bp spacer 첫 bp index" - "NRG PAM 끝나는 bp index" : +/- strand 정보 : #trscprt_align에서 조사한transcription 여부