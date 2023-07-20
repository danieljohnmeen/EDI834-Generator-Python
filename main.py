import pandas as pd
from constants import *
# Load functions
from functions import generate_ISA, generate_GS, generate_ST, generate_BGN, generate_N1
# Load the data
enrollees = pd.read_csv(ENROLLEE_CSV)
dependents = pd.read_csv(DEPENDENT_CSV)
# EDI Document List
edi_documents = []
# Group enrollees by benefit plan provider name
grouped = enrollees.groupby(PROVIDER_NAME_COL)
unique_control_num = 1
for provider_name, enrollee_group in grouped:
    # print(f"Provider Name: {provider_name}")
    # EDI Document Data List for Each Provider
    edi_provider_documents = []

    # ISA SEGMENT
    isa_segment = generate_ISA(unique_control_num)
    print(f"ISA SEGMENT: {isa_segment}")
    # END ISA SEGMENT

    # GS SEGMENT
    gs_segment = generate_GS(unique_control_num)
    print(f"GS SEGMENT: {gs_segment}")
    # END GS SEGMENT

    # ST SEGMENT
    st_segment = generate_ST(unique_control_num)
    print(f"ST SEGMENT: {st_segment}")
    # END ST SEGMENT

    # BGN SEGMENT
    ## Pass the params for the BGN Segment here
    trans_set_ref_num = 'TRANS_SET_REF_NUM'
    original_trans_set_ref_num = 'ORIGIN_TRANS_SET_REF_NUM'
    bgn_segment = generate_BGN(BGN_TRANS_PURP_CODE_ORIGIN, trans_set_ref_num, original_trans_set_ref_num)
    print(f"BGN SEGMENT: {bgn_segment}")
    #End BGN SEGMENT

    # N1 SEGMENTS for Sponsor and Payer
    ## sponsor segment
    sponser_name = 'LBMC Employment Partners LLC'
    sponsor_id_number = 'XXX'   # Sponser Identifier: Code identifying a party or other code (Min 2, Max 80)
    n1_sponsor_segment = generate_N1(N1_PLAN_SPONSOR_CODE, sponser_name, N1_FEDERAL_ID_NUMBER, sponsor_id_number)
    print(f"N1_SPONSOR: {n1_sponsor_segment}")
    ## payer segment
    insurer_id_code = 'XXXX'
    n1_payer_segment = generate_N1(N1_INSURER_CODE, provider_name, N1_FEDERAL_ID_NUMBER, insurer_id_code)
    print(f"N1_PAYER: {n1_payer_segment}")
    for _, enrollee in enrollee_group.iterrows():
        # print(f"Enrollee: {enrollee[FIRST_NAME_COL]} {enrollee[LAST_NAME_COL]}")
        enrollee_dependents = dependents[dependents[EMPLOYEE_ID_COL] == enrollee[EMPLOYEE_ID_COL]]
        for _, dependent in enrollee_dependents.iterrows():
            print(f"\tDependent: {dependent[FIRST_NAME_COL]} {dependent[LAST_NAME_COL]}")
