import pandas as pd

# Load the data
enrollees = pd.read_csv('enrollees.csv')
dependents = pd.read_csv('dependents.csv')

# Group enrollees by benefit plan provider name
grouped = enrollees.groupby('Benefit Plan Provider Name')

for provider_name, enrollee_group in grouped:
    print(f"Provider Name: {provider_name}")
    for _, enrollee in enrollee_group.iterrows():
        print(f"Enrollee: {enrollee['FirstName']} {enrollee['LastName']}")
        enrollee_dependents = dependents[dependents['EmployeeId'] == enrollee['EmployeeId']]
        for _, dependent in enrollee_dependents.iterrows():
            print(f"\tDependent: {dependent['FirstName']} {dependent['LastName']} - {provider_name}")
