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
            if provider_name == 'CIGNA':
                continue
            print(f'Start Provider -> ID: {provider_name}')
            #   Get EmployeeID list from { ENROLLEE_TBL } for the provider name
            query_for_enrollee_ids = f'''SELECT [{SSN_COL}] AS SocialSecurityNumber
                FROM {ENROLLEE_TBL}
                WHERE [{BENEFIT_PLAN_PROVIDER_NAME_COL}] = '{provider_name}' AND [{EMPLOYEE_STATUS_COL}] IN ('Active', 'Cobra', 'Surviving Spouse')
                GROUP BY [{SSN_COL}];
                '''
            cursor.execute(query_for_enrollee_ids)
            enrollee_ids = cursor.fetchall()
            for enrollee_id in enrollee_ids:
                #   Get enrollee details from provided employee id
                query_for_enrollees = f'''select 
                [{BENEFIT_PLAN_PROVIDER_NAME_COL}]  as Benefit_Plan_Provider_Name,
                [{EMPLOYEE_ID_COL}]                 as Employee_Id,
                [{BENEFIT_STATUS_CODE_COL}]         as Benefit_Status_Code,
                [{RELATION_COL}]                    as RelationCode,
                [{EMPLOYEE_STATUS_COL}]             as Employee_Status,
                [{EMPLOYEE_TYPE_COL}]               as Employee_Type,
                [{COMPANY_CODE_COL}]                as CompanyCode,
                [{BCBS_CLASS_ID_COL}]                 as BCBC_Class,
                [{BCBS_GROUP_ID_COL}]                 as BCBC_Group,
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
                from {ENROLLEE_TBL} where [{BENEFIT_PLAN_PROVIDER_NAME_COL}] = '{provider_name}' AND [{SSN_COL}] = \'{enrollee_id.SocialSecurityNumber}\''''
                cursor.execute(query_for_enrollees)
                enrollee = cursor.fetchone()
                print(f'Start Enrollee -> {enrollee.SocialSecurityNumber}: {enrollee.First_Name}  {enrollee.Last_Name}')
                row_enrollee = make_json_from_enrollee(provider_name, enrollee, cursor)
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
def make_json_from_dependent(provider_name, dependent_ssn, cursor):
    #   Get dpeendent details from provided SSN Number
    print(f'>>> >>> >>> >>> Get Dependent: {dependent_ssn}')
    query_for_benefits = f'''select 
        [{DEPENDENT_SSN_COL}]                         as Dependent_SSN,
        [{DEPENDENT_PARENT_SSN_COL}]                  as Dependent_Parent_SSN,
        [{DEPENDENT_BENEFIT_TYPE_COL}]                as Benefit_Type,
        [{DEPENDENT_RELATION_COL}]                    as RelationCode,
        [{DEPENDENT_BCBS_CLASS_ID_COL}]                 as BCBC_Class,
        [{DEPENDENT_BCBS_GROUP_ID_COL}]                 as BCBC_Group,
        [{DEPENDENT_COVERAGE_EFFECTIVE_FROM_COL}]     as Coverage_Effective_From,
        [{DEPENDENT_COVERAGE_EFFECTIVE_TO_COL}]       as Coverage_Effective_To,
        [{DEPENDENT_COVERAGE_CODE_COL}]               as Coverage_Code,
        [{DEPENDENT_COVERAGE_PLAN_COL}]               as Coverage_Plan,
        [{DEPENDENT_BENEFIT_STATUS_CODE_COL}]         as Benefit_Status_Code,
        [{DEPENDENT_EMPLOYEE_STATUS_COL}]             as Employee_Status,
        [{DEPENDENT_COMPANY_CODE_COL}]                as CompanyCode,
        [{DEPENDENT_TYPE_COL}]                        as Dependent_Type,
        [{DEPENDENT_LAST_NAME_COL}]                   as Dependent_Last_Name,
        [{DEPENDENT_FIRST_NAME_COL}]                  as Dependent_First_Name,
        [{DEPENDENT_ADDRESS1_COL}]                    as Address_1,
        [{DEPENDENT_ADDRESS2_COL}]                    as Address_2,
        [{DEPENDENT_ADDRESS3_COL}]                    as Address_3,
        [{DEPENDENT_CITY_COL}]                        as City,
        [{DEPENDENT_STATE_COL}]                       as State,
        [{DEPENDENT_ZIP_CODE_COL}]                    as Zip_Code,
        [{DEPENDENT_BIRTH_DATE_COL}]                  as Date_Birthday,
        [{DEPENDENT_GENDER_COL}]                      as Dependent_Gender,
        [{DEPENDENT_COVERAGE_NAME_COL}]               as Coverage_Name
       from {DEPENDENT_TBL} where [{DEPENDENT_BENEFIT_PLAN_PROVIDER_NAME_COL}] = '{provider_name}' AND  TRIM([{DEPENDENT_SSN_COL}]) = \'{str(dependent_ssn).strip()}\''''
    benefits_array = []
    cursor.execute(query_for_benefits)
    benefits = cursor.fetchall()
    for benefit in benefits:
        row_benefit = {
            "BenefitType": benefit.Benefit_Type,
            "CoverageEffectiveFrom": benefit.Coverage_Effective_From,
            "CoverageEffectiveTo": benefit.Coverage_Effective_To,
            "CoverageCode": benefit.Coverage_Code,
            "CoveragePlan": benefit.Coverage_Plan
        }
        benefits_array.append(row_benefit)
    cursor.execute(query_for_benefits)
    dependent = cursor.fetchone()
    bcbcClasId = ''
    if provider_name != 'CIGNA':
        query_for_dependent_bcbc = query_for_benefits  +  f''' AND  [{DEPENDENT_BCBS_CLASS_ID_COL}] IS NOT NULL AND LEN([{DEPENDENT_BCBS_CLASS_ID_COL}]) = 8'''
        cursor.execute(query_for_dependent_bcbc)
        row = cursor.fetchone()
        if row is not None:
            bcbcClasId = row.BCBC_Class
    row_enrollee = {
        "BenefitStatusCode": dependent.Benefit_Status_Code  if dependent.Benefit_Status_Code != None  else 'A',
        "EmployeeStatus": dependent.Employee_Status,
        "EmployeeType": "",
        "BCBCClass": bcbcClasId,
        "BCBCGruop": dependent.BCBC_Group,
        "CompanyCode": dependent.CompanyCode,
        "RelationShipCode": dependent.RelationCode,
        "LastName": dependent.Dependent_Last_Name,
        "FirstName": dependent.Dependent_First_Name,
        "Address": f'{dependent.Address_1 if dependent.Address_1!= None  and  dependent.Address_1 != "NULL" else "" } {dependent.Address_2 if dependent.Address_2 != None  and  dependent.Address_2 != "NULL" else ""} {dependent.Address_3 if dependent.Address_3 !=  None  and  dependent.Address_3 != "NULL" else ""}'.strip(),
        "City": str(dependent.City).strip() if dependent.City != None and  dependent.City != 'NULL' else "",
        "State": str(dependent.State).strip()  if dependent.State != None and  dependent.State != 'NULL' else "",
        "Zip": str(dependent.Zip_Code).strip()  if dependent.Zip_Code != None and  dependent.Zip_Code != 'NULL'else "",
        "SocialSecurityNumber": str(dependent.Dependent_SSN).strip().replace('.0', ''),
        "ParentSocialSecurityNumber": str(dependent.Dependent_Parent_SSN).strip().replace('.0', ''),
        "BirthDate": dependent.Date_Birthday,
        "Gender": dependent.Dependent_Gender,
        "CoverageLevel": dependent.Coverage_Name,
        "Benefits": benefits_array
    }
    return row_enrollee
def make_json_from_enrollee(provider_name, enrollee, cursor):
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
            [{COVERAGE_CODE_COL}]               as Coverage_Code,
            [{COVERAGE_PLAN_COL}]               as Coverage_Plan,
            [{COVERAGE_EFFECTIVE_FROM_COL}]     as Coverage_Effective_From,
            [{COVERAGE_EFFECTIVE_TO_COL}]       as Coverage_Effective_To
        from {ENROLLEE_TBL} where [{BENEFIT_PLAN_PROVIDER_NAME_COL}] = '{provider_name}' AND [{SSN_COL}] = \'{enrollee.SocialSecurityNumber}\''''
    cursor.execute(query_for_benefits)
    benefits = cursor.fetchall()
    for benefit in benefits:
        print(f">>>>>>> Get Benefit -> {enrollee.SocialSecurityNumber} -> {benefit.Benefit_Type}")
        row_benefit = {
            "BenefitType": benefit.Benefit_Type,
            "CoverageEffectiveFrom": benefit.Coverage_Effective_From,
            "CoverageEffectiveTo": benefit.Coverage_Effective_To,
            "CoverageCode": benefit.Coverage_Code,
            "CoveragePlan": benefit.Coverage_Plan
        }
        benefits_array.append(row_benefit)
    dependents_array = []
    query_for_dependents_ssn_list = f'select [{DEPENDENT_SSN_COL}] as Dependent_SSN from {DEPENDENT_TBL} where [{DEPENDENT_BENEFIT_PLAN_PROVIDER_NAME_COL}] = \'{provider_name}\' AND [{DEPENDENT_PARENT_SSN_COL}] = \'{enrollee.SocialSecurityNumber}\' group by [{DEPENDENT_SSN_COL}]'
    # print(query_for_dependents_ssn_list)
    cursor.execute(query_for_dependents_ssn_list)
    dependent_ssn_list = cursor.fetchall()
    for dependent_ssn in dependent_ssn_list:
        if dependent_ssn.Dependent_SSN != None:
            row_dependent = make_json_from_dependent(provider_name, dependent_ssn.Dependent_SSN, cursor)
            dependents_array.append(row_dependent)
    bcbcClasId = ''
    if provider_name != 'CIGNA':
        query_for_enrolee_bcbc = f'''select 
                [{BCBS_CLASS_ID_COL}]                 as BCBC_Class
                from {ENROLLEE_TBL} where [{BENEFIT_PLAN_PROVIDER_NAME_COL}] = '{provider_name}' AND [{SSN_COL}] = \'{enrollee.SocialSecurityNumber}\' AND  [{BCBS_CLASS_ID_COL}] IS NOT NULL AND LEN([{BCBS_CLASS_ID_COL}]) = 8;'''
        cursor.execute(query_for_enrolee_bcbc)
        row = cursor.fetchone()
        # Check if a row was fetched
        if row:
            # Process the row data
            bcbcClasId = row.BCBC_Class
    row_enrollee = {
        "EmployeeId": enrollee.Employee_Id,
        "BenefitStatusCode": str(enrollee.Benefit_Status_Code).strip()  if enrollee.Benefit_Status_Code != None else 'A',
        "EmployeeStatus": enrollee.Employee_Status,
        "EmployeeType": enrollee.Employee_Type,
        "RelationShipCode": enrollee.RelationCode,
        "BCBCClass": bcbcClasId,
        "CompanyCode": enrollee.CompanyCode,
        "BCBCGruop": enrollee.BCBC_Group,
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
