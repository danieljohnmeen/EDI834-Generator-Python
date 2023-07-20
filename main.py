import pandas as pd
from constants import *
# Load functions
from functions import generate_ISA
# Load the data
enrollees = pd.read_csv(ENROLLEE_CSV)
dependents = pd.read_csv(DEPENDENT_CSV)
# EDI Document List
edi_documents = []
# Group enrollees by benefit plan provider name
grouped = enrollees.groupby(PROVIDER_NAME_COL)
unique_control_num = 1
for provider_name, enrollee_group in grouped:
    print(f"Provider Name: {provider_name}")
    # EDI Document Data List for Each Provider
    edi_provider_documents = []
    isa_segment = generate_ISA(unique_control_num)
    print(f"ISA SEGMENT: {isa_segment}")
    for _, enrollee in enrollee_group.iterrows():
        print(f"Enrollee: {enrollee[FIRST_NAME_COL]} {enrollee[LAST_NAME_COL]}")
        enrollee_dependents = dependents[dependents[EMPLOYEE_ID_COL] == enrollee[EMPLOYEE_ID_COL]]
        for _, dependent in enrollee_dependents.iterrows():
            print(f"\tDependent: {dependent[FIRST_NAME_COL]} {dependent[LAST_NAME_COL]}")
