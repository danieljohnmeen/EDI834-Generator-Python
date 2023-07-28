import json
import pyodbc

from constants import *

# This function provides to make json structure from the sql
# You can define the table names for the enrollee and dependents in constants.py file


def load_json_from_sql():
    try:
        conn_str = f'DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={DB_DATABASE};UID={DB_USER_NAME};PWD={DB_USER_PASS}'

        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()

        #   Get Plan Provider Name List from { ENROLLEE_TBL }
        query_for_providers = f'''SELECT [{BENEFIT_PLAN_PROVIDER_NAME_COL}] AS provider_name
                        FROM {ENROLLEE_TBL}
                        GROUP BY [{BENEFIT_PLAN_PROVIDER_NAME_COL}];'''

        cursor.execute(query_for_providers)
        providers = cursor.fetchall()
        data_json = []
        for provider in providers:
            enrollees_array = []
            provider_name = provider.provider_name
            print(f'Start Provider -> ID: {provider_name}')
            #   Get EmployeeID list from { ENROLLEE_TBL } for the provider name
            query_for_enrollee_ids = f'''SELECT [{EMPLOYEE_ID_COL}] AS EmployeeID
                FROM {ENROLLEE_TBL}
                WHERE [{BENEFIT_PLAN_PROVIDER_NAME_COL}] = '{provider_name}' AND [{EMPLOYEE_STATUS_COL}] IN ('Active', 'Cobra', 'Surviving Spouse')
                GROUP BY [{EMPLOYEE_ID_COL}];
                '''
            cursor.execute(query_for_enrollee_ids)
            print(query_for_enrollee_ids)
            enrollee_ids = cursor.fetchall()
            for enrollee_id in enrollee_ids:
                #   Get enrollee details from provided employee id
                query_for_enrollees = f'''select 
                [{BENEFIT_PLAN_PROVIDER_NAME_COL}]  as Benefit_Plan_Provider_Name,
                [{EMPLOYEE_ID_COL}]                 as Employee_Id,
                [{BENEFIT_STATUS_CODE_COL}]         as Benefit_Status_Code,
                [{EMPLOYEE_STATUS_COL}]             as Employee_Status,
                [{LAST_NAME_COL}]                   as Last_Name,
                [{FIRST_NAME_COL}]                  as First_Name,
                [{SSN_COL}]                         as SocialSecurityNumber,
                [{ADDRESS1_COL}]                    as Address_1,
                [{ADDRESS2_COL}]                    as Address_2,
                [{ADDRESS3_COL}]                    as Address_3,
                [{CITY_COL}]                        as City,
                [{STATE_COL}]                       as State,
                [{ZIP_CODE_COL}]                    as Zip_Code,
                [{BIRTH_DATE_COL}]                  as BirthDate,
                [{GENDER_COL}]                      as Gender,
                [{COVERAGE_NAME_COL}]               as Coverage_Name,
                [{DATE_HIRED_COL}]                  as Date_Hired,
                [{DATE_TERMINATED_COL}]             as Date_Terminated,
                [{BENEFIT_TYPE_COL}]                as Benefit_Type,
                [{COVERAGE_EFFECTIVE_FROM_COL}]     as Coverage_Effective_From,
                [{COVERAGE_EFFECTIVE_TO_COL}]       as Coverage_Effective_To
                from {ENROLLEE_TBL} where [{EMPLOYEE_ID_COL}] = {enrollee_id.EmployeeID}'''
                cursor.execute(query_for_enrollees)
                enrollee = cursor.fetchone()
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
    #   Get dpeendent details from provided SSN Number
    query_for_benefits = f'''select 
        [{DEPENDENT_SSN_COL}]                         as Dependent_SSN,
        [{DEPENDENT_BENEFIT_TYPE_COL}]                as Benefit_Type,
        [{DEPENDENT_COVERAGE_EFFECTIVE_FROM_COL}]     as Coverage_Effective_From,
        [{DEPENDENT_COVERAGE_EFFECTIVE_TO_COL}]       as Coverage_Effective_To,
        [{DEPENDENT_BENEFIT_STATUS_CODE_COL}]         as Benefit_Status_Code,
        [{DEPENDENT_EMPLOYEE_STATUS_COL}]             as Employee_Status,
        [{DEPENDENT_TYPE_COL}]                        as Dependent_Type,
        [{DEPENDENT_LAST_NAME_COL}]                   as Dependent_Last_Name,
        [{DEPENDENT_FIRST_NAME_COL}]                  as Dependent_First_Name,
        [{DEPENDENT_BIRTH_DATE_COL}]                  as Date_Birthday,
        [{DEPENDENT_GENDER_COL}]                      as Dependent_Gender,
        [{DEPENDENT_COVERAGE_NAME_COL}]               as Coverage_Name
       from {DEPENDENT_TBL} where TRIM([{DEPENDENT_SSN_COL}]) = \'{str(dependent_ssn).strip()}\''''
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
        "BenefitStatusCode": dependent.Benefit_Status_Code  if dependent.Benefit_Status_Code != None  else 'A',
        "EmployeeStatus": dependent.Employee_Status,
        "RelationShipCode": dependent.Dependent_Type,
        "LastName": dependent.Dependent_Last_Name,
        "FirstName": dependent.Dependent_First_Name,
        "SocialSecurityNumber": str(dependent.Dependent_SSN).strip().replace('.0', ''),
        "BirthDate": dependent.Date_Birthday,
        "Gender": dependent.Dependent_Gender,
        "CoverageLevel": dependent.Coverage_Name,
        "Benefits": benefits_array,
    }
    return row_enrollee
def make_json_from_enrollee(enrollee, cursor):
    benefits_array = []
    query_for_benefits = f'''select 
            [{BENEFIT_PLAN_PROVIDER_NAME_COL}]  as Benefit_Plan_Provider_Name,
            [{EMPLOYEE_ID_COL}]                 as Employee_Id,
            [{BENEFIT_STATUS_CODE_COL}]         as Benefit_Status_Code,
            [{EMPLOYEE_STATUS_COL}]             as Employee_Status,
            [{LAST_NAME_COL}]                   as Last_Name,
            [{FIRST_NAME_COL}]                  as First_Name,
            [{SSN_COL}]                         as SocialSecurityNumber,
            [{ADDRESS1_COL}]                    as Address_1,
            [{ADDRESS2_COL}]                    as Address_2,
            [{ADDRESS3_COL}]                    as Address_3,
            [{CITY_COL}]                        as City,
            [{STATE_COL}]                       as State,
            [{ZIP_CODE_COL}]                    as Zip_Code,
            [{BIRTH_DATE_COL}]                  as BirthDate,
            [{GENDER_COL}]                      as Gender,
            [{COVERAGE_NAME_COL}]               as Coverage_Name,
            [{DATE_HIRED_COL}]                  as Date_Hired,
            [{DATE_TERMINATED_COL}]             as Date_Terminated,
            [{BENEFIT_TYPE_COL}]                as Benefit_Type,
            [{COVERAGE_EFFECTIVE_FROM_COL}]     as Coverage_Effective_From,
            [{COVERAGE_EFFECTIVE_TO_COL}]       as Coverage_Effective_To
        from {ENROLLEE_TBL} where [{EMPLOYEE_ID_COL}] = {enrollee.Employee_Id}'''
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
    query_for_dependents_ssn_list = f'select [{DEPENDENT_SSN_COL}] as Dependent_SSN from {DEPENDENT_TBL} where  [{EMPLOYEE_ID_COL}] = {enrollee.Employee_Id} group by [{DEPENDENT_SSN_COL}]'
    print(query_for_dependents_ssn_list)
    cursor.execute(query_for_dependents_ssn_list)
    dependent_ssn_list = cursor.fetchall()
    for dependent_ssn in dependent_ssn_list:
        print(dependent_ssn.Dependent_SSN)
        if dependent_ssn.Dependent_SSN != None:
            row_dependent = make_json_from_dependent(dependent_ssn.Dependent_SSN, cursor)
            dependents_array.append(row_dependent)
    row_enrollee = {
        "EmployeeId": enrollee.Employee_Id,
        "BenefitStatusCode": str(enrollee.Benefit_Status_Code).strip()  if enrollee.Benefit_Status_Code != None else 'A',
        "EmployeeStatus": enrollee.Employee_Status,
        "LastName": str(enrollee.Last_Name).strip(),
        "FirstName": str(enrollee.First_Name).strip(),
        "SocialSecurityNumber": str(enrollee.SocialSecurityNumber).strip(),
        "Address": f'{enrollee.Address_1 if enrollee.Address_1!= None  and  enrollee.Address_1 != "NULL" else "" } {enrollee.Address_2 if enrollee.Address_2 != None  and  enrollee.Address_2 != "NULL" else ""} {enrollee.Address_3 if enrollee.Address_3 !=  None  and  enrollee.Address_3 != "NULL" else ""}'.strip(),
        "City": str(enrollee.City).strip() if enrollee.City != None and  enrollee.City != 'NULL' else "",
        "State": str(enrollee.State).strip()  if enrollee.State != None and  enrollee.State != 'NULL' else "",
        "Zip": str(enrollee.Zip_Code).strip()  if enrollee.Zip_Code != None and  enrollee.Zip_Code != 'NULL'else "",
        "BirthDate": enrollee.BirthDate,
        "Gender": enrollee.Gender,
        "CoverageLevel": enrollee.Coverage_Name,
        "DateHired": enrollee.Date_Hired,
        "TerminationDate": enrollee.Date_Terminated,
        "Benefits": benefits_array,
        "Dependents": dependents_array
    }
    return row_enrollee
