import json
import pyodbc

from constants import *
def load_json_from_sql():
    try:
        conn_str = f'DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={DB_DATABASE};UID={DB_USER_NAME};PWD={DB_USER_PASS}'

        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()

        query_for_providers = f'''SELECT Benefit_Plan_Provider_Name AS provider_name
                        FROM {ENROLLEE_TBL}
                        GROUP BY Benefit_Plan_Provider_Name;'''

        cursor.execute(query_for_providers)
        providers = cursor.fetchall()
        data_json = []
        for provider in providers:
            enrollees_array = []
            provider_name = provider.provider_name
            print(f'Start Provider -> ID: {provider_name}')

            query_for_enrollee_ids = f'''SELECT Employee_Id AS EmployeeID
                FROM {ENROLLEE_TBL}
                WHERE Benefit_Plan_Provider_Name = '{provider_name}'
                GROUP BY Employee_Id;
                '''
            cursor.execute(query_for_enrollee_ids)
            print(query_for_enrollee_ids)
            enrollee_ids = cursor.fetchall()
            for enrollee_id in enrollee_ids:
                query_for_enrollees = f'select * from {ENROLLEE_TBL} where Employee_Id = {enrollee_id.EmployeeID}'
                print(query_for_enrollees)
                cursor.execute(query_for_enrollees)
                enrollee = cursor.fetchone()
                print(enrollee.First_Name)
                print(enrollee.Employee_Id)
                row_enrollee = make_json_from_enrollee(enrollee, cursor)
                enrollees_array.append(row_enrollee)
            row_provider = {
                "Provider": provider_name,
                "Enrollees": enrollees_array
            }
            data_json.append(row_provider)


        return data_json
    except pyodbc.Error as ex:
        print("Error connecting to the database:", ex)
        return []
def make_json_from_dependent(dependent_ssn, cursor):
    query_for_benefits = f'select * from {DEPENDENT_TBL} where TRIM(Dependent_SSN_1) = \'{str(dependent_ssn).strip()}\''
    print(query_for_benefits)
    benefits_array = []
    cursor.execute(query_for_benefits)
    benefits = cursor.fetchall()
    for benefit in benefits:
        row_benefit = {
            "BenefitType": benefit.Benefit_Type,
            "CoverageEffectiveFrom": benefit.Coverage_Effective_From,
            "CoverageEffectiveTo": benefit.Coverage_Effective_To
        }
        benefits_array.append(row_benefit)
    cursor.execute(query_for_benefits)
    dependent = cursor.fetchone()
    row_enrollee = {
        "BenefitStatusCode": dependent.Benefit_Status_Code  if dependent.Benefit_Status_Code != None else 'A',
        "EmployeeStatus": dependent.Employee_Status,
        "RelationShipCode": dependent.Dependent_Type,
        "LastName": dependent.Dependent_Last_Name,
        "FirstName": dependent.Dependent_First_Name,
        "SocialSecurityNumber": str(dependent.Dependent_SSN_1).strip(),
        "BirthDate": dependent.Date_Birthday,
        "Gender": dependent.Dependent_Gender,
        "CoverageLevel": dependent.Coverage_Name,
        "Benefits": benefits_array,
    }
    return row_enrollee
def make_json_from_enrollee(enrollee, cursor):
    benefits_array = []
    query_for_benefits = f'select * from {ENROLLEE_TBL} where Employee_Id = {enrollee.Employee_Id}'
    print(query_for_benefits)
    cursor.execute(query_for_benefits)
    benefits = cursor.fetchall()
    for benefit in benefits:
        row_benefit = {
            "BenefitType": benefit.Benefit_Type,
            "CoverageEffectiveFrom": benefit.Coverage_Effective_From,
            "CoverageEffectiveTo": benefit.Coverage_Effective_To
        }
        benefits_array.append(row_benefit)
    dependents_array = []
    query_for_dependents_ssn_list = f'select Dependent_SSN_1 from {DEPENDENT_TBL} where  Employee_Id = {enrollee.Employee_Id} group by Dependent_SSN_1'
    print(query_for_dependents_ssn_list)
    cursor.execute(query_for_dependents_ssn_list)
    dependent_ssn_list = cursor.fetchall()
    for dependent_ssn in dependent_ssn_list:
        print(dependent_ssn.Dependent_SSN_1)
        if dependent_ssn.Dependent_SSN_1 != None:
            row_dependent = make_json_from_dependent(dependent_ssn.Dependent_SSN_1, cursor)
            dependents_array.append(row_dependent)
    row_enrollee = {
        "EmployeeId": enrollee.Employee_Id,
        "BenefitStatusCode": str(enrollee.Benefit_Status_Code).strip()  if enrollee.Benefit_Status_Code != None else 'A',
        "EmployeeStatus": enrollee.Employee_Status,
        "LastName": str(enrollee.Last_Name).strip(),
        "FirstName": str(enrollee.First_Name).strip(),
        "SocialSecurityNumber": str(enrollee.SocialSecurityNumber).strip(),
        "Address": f'{enrollee.Address_1} {enrollee.Address_2} {enrollee.Address_3}'.strip(),
        "City": str(enrollee.City).strip(),
        "State": str(enrollee.State).strip(),
        "Zip": str(enrollee.Zip_Code).strip(),
        "BirthDate": enrollee.BirthDate,
        "Gender": enrollee.Gender,
        "CoverageLevel": enrollee.Coverage_Name,
        "DateHired": enrollee.Date_Hired,
        "TerminationDate": enrollee.Date_Terminated,
        "Benefits": benefits_array,
        "Dependents": dependents_array
    }
    return row_enrollee
    