import pandas as pd
from constants import *
# Load functions
from functions import generate_ISA, generate_GS, generate_ST, generate_BGN
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
    isa_segment = generate_ISA(unique_control_num)
    print(f"ISA SEGMENT: {isa_segment}")
    gs_segment = generate_GS(unique_control_num)
    print(f"GS SEGMENT: {gs_segment}")
    st_segment = generate_ST(unique_control_num)
    print(f"ST SEGMENT: {st_segment}")
    # Pass the params for the BGN Segment here
    trans_set_ref_num = 'TRANS_SET_REF_NUM'
    original_trans_set_ref_num = 'ORIGIN_TRANS_SET_REF_NUM'
    bgn_segment = generate_BGN(BGN_TRANS_PURP_CODE_ORIGIN, trans_set_ref_num, original_trans_set_ref_num)
    print(f"BGN SEGMENT: {bgn_segment}")
    #End BGN SEGMENT
    for _, enrollee in enrollee_group.iterrows():
        # print(f"Enrollee: {enrollee[FIRST_NAME_COL]} {enrollee[LAST_NAME_COL]}")
        enrollee_dependents = dependents[dependents[EMPLOYEE_ID_COL] == enrollee[EMPLOYEE_ID_COL]]
        for _, dependent in enrollee_dependents.iterrows():
            print(f"\tDependent: {dependent[FIRST_NAME_COL]} {dependent[LAST_NAME_COL]}")
