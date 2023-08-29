# Define Constants for the DB Connection
DB_SERVER = '127.0.0.1'
DB_DATABASE = 'enrollees'
DB_USER_NAME = 'teszt'
DB_USER_PASS = 'teszt'
DB_DRIVER = '{ODBC Driver 17 for SQL Server}'

#Define Constants for the SFTP
## CIGNA

CIGNA_SFTP_HOST = ''
CIGNA_SFTP_PORT = 22
CIGNA_SFTP_USER = ''
CIGNA_SFTP_PASS = ''
CIGNA_SFTP_PATH = 'edi/'
CIGNA_SFTP_ALLOW = 'Y'
## BCBS
BCBS_SFTP_HOST = ''
BCBS_SFTP_PORT = 22
BCBS_SFTP_USER = ''
BCBS_SFTP_PASS = ''
BCBS_SFTP_PATH = 'inbox/'
BCBS_SFTP_ALLOW = 'Y'

# Define constants variables

ENROLLEE_TBL = 'enrollee_Test'
DEPENDENT_TBL = 'dependent_test'

# Define output file prefix
OUTPUT_FILE_PREFIX_CIGNA = 'TEST_CIGNA'
OUTPUT_FILE_PREFIX_BCBS = 'TEST_BCBS'
#  Define column names of Enrollee Table

BENEFIT_PLAN_PROVIDER_NAME_COL  = 'Benefit_Plan_Provider_Name'
EMPLOYEE_ID_COL                 = 'Employee_Id'
BENEFIT_STATUS_CODE_COL         = 'Benefit_Status_Code'
EMPLOYEE_STATUS_COL             = 'Employee_Status'
LAST_NAME_COL                   = 'Last_Name'
FIRST_NAME_COL                  = 'First_Name'
SSN_COL                         = 'SocialSecurityNumber'
ADDRESS1_COL                    = 'Address_1'
ADDRESS2_COL                    = 'Address_2'
ADDRESS3_COL                    = 'Address_3'
CITY_COL                        = 'City'
STATE_COL                       = 'State'
ZIP_CODE_COL                    = 'Zip_Code'
BIRTH_DATE_COL                  = 'BirthDate'
GENDER_COL                      = 'Gender'
COVERAGE_NAME_COL               = 'Coverage_Name'
DATE_HIRED_COL                  = 'Date_Hired'
DATE_TERMINATED_COL             = 'Date_Terminated'
BENEFIT_TYPE_COL                = 'product_category'
COVERAGE_EFFECTIVE_FROM_COL     = 'Coverage_Effective_From'
COVERAGE_EFFECTIVE_TO_COL       = 'Coverage_Effective_To'
COVERAGE_CODE_COL				= 'Coverage_Code'
COVERAGE_PLAN_COL				= 'PlanID'
BCBS_CLASS_ID_COL				= 'bcbsclassID'
BCBS_GROUP_ID_COL				= 'BCBSGroupID'
RELATION_COL					= 'Relationship_Code'
EMPLOYEE_TYPE_COL				= 'Employee_Type'
COMPANY_CODE_COL				= 'CompanyCode'
# Define column names of dependents table

DEPENDENT_SSN_COL                         = 'Dependent_SS'
DEPENDENT_BENEFIT_TYPE_COL                = 'Product_Category'
DEPENDENT_BENEFIT_PLAN_PROVIDER_NAME_COL  = 'Benefit_Plan_Provider_Name'
DEPENDENT_COVERAGE_EFFECTIVE_FROM_COL     = 'Coverage_Effective_From'
DEPENDENT_COVERAGE_EFFECTIVE_TO_COL       = 'Coverage_Effective_To'
DEPENDENT_COVERAGE_CODE_COL				= 'CoverageCode'
DEPENDENT_COVERAGE_PLAN_COL				= 'PlanID'
DEPENDENT_BENEFIT_STATUS_CODE_COL         = 'Benefit_Status_Code'
DEPENDENT_EMPLOYEE_STATUS_COL             = 'Employee_Status'
DEPENDENT_TYPE_COL                        = 'Dependent_Type'
DEPENDENT_LAST_NAME_COL                   = 'Dependent_Last_Name'
DEPENDENT_FIRST_NAME_COL                  = 'Dependent_First_Name'
DEPENDENT_BIRTH_DATE_COL                  = 'Date_Birthday'
DEPENDENT_GENDER_COL                      = 'Dependent_Gender'
DEPENDENT_COVERAGE_NAME_COL               = 'Coverage_Name'
DEPENDENT_BCBS_CLASS_ID_COL				= 'bcbsclassID'
DEPENDENT_BCBS_GROUP_ID_COL				= 'BCBSGroupID'
DEPENDENT_PARENT_SSN_COL				= 'SS'
DEPENDENT_RELATION_COL					= 'Relationship_Code'
DEPENDENT_COMPANY_CODE_COL				= 'companycode'
# Define Constants variables for the ISA Segment
ISA_AUTH_INFO_QUALIFIER             = '00'                      # No Authorization Information Present
ISA_AUTH_INFO                       = '          '              # Empty 10 characters for 00 of I01 (MIN/MAX 10)
ISA_SEC_INFO_QUALIFIER              = '00'                      # No Security Information present
ISA_SEC_INFO                        = '          '              # Empty 10 characters for 00 of I03
ISA_SENDER_ID_QUALIFIER             = 'ZZ'                      # Interchange ID Qualifiere (MIN/MAX 2)
ISA_SENDER_ID                       = '------SENDER_ID'         # Interchange Sender ID (MIN/MAX 15)
ISA_RECEIVER_ID_QUALIFIER           = 'ZZ'                      # Interchange ID Qualifiere (MIN/MAX 2)
ISA_RECEIVER_ID                     = '----RECEIVER_ID'         # Interchange Receiver ID (MIN/MAX 15)
ISA_ACK_REQUESTED                   = '1'                       # Code indicating sender's request for an interchange acknowledgment (MIN/MAX 1)
ISA_USAGE_INDICATOR                 = 'I'                       # Interchange Usage Indicator(MIN/MAX 1): Code indicating whether data enclosed by this interchange envelope is test, production or information (I:Information, P:Production Data, T:Test Data)
ISA_COMP_ELEM_SEP                   = '>'                       # Component Element Separator (MIN/MAX 1)
ISA_CONTROL_VERSION_NUMBER          = '00501'                   # Interchange Control Version Number
# Define Constants variable for the GS Segment
GS_APP_SENDER_CODE                  = 'SENDER_CODE'             # Application Sender's Code (Min 2/ Max 15)
GS_APP_RECEIV_CODE                  = 'RECEIVE_CODE'            # Application Receiver's Code (Min 2/ Max 15)
GS_FUN_IDENTI_CODE                  = 'HP'                      # Functional Identifiere Code (BE: Benefit Enrollment and Maintenance (834))
GS_RES_AGENCY_CODE                  = 'X'                       # Responsible Agency Code (T: TDCC, X: Accredited Standards Committee X12)
GS_VER_REL_IND_IDENTI_CODE          = '005010X220A1'            # Version / Release / Industry Identifier Code (005010X220A1: ANSI ASC X12 Benefit Enrollment and Maintenance (834) through June 2010)
# Define Constants variable for the ST Segment
ST_TRANS_SET_ID_CODE                = '834'                     # Transaction Set Identifier Code (834: Benefit Enrollment and Maintenance)
ST_IMP_CONV_REFER                   = '005010X220A1'            # Implementation Convention Reference
# Define Constants variable for the BGN Segment
## Transaction Set Purpose Code (OO: Original, 15: Resubmission, 22: Information Copy)
BGN_TRANS_PURP_CODE_ORIGIN          = '00'
BGN_TRANS_PURP_CODE_RE_SUB          = '15'
BGN_TRANS_PURP_CODE_INFOCP          = '22'
BGN_TIMEZONE_CODE                   = '01'                      # Time Zone Code
BGN_ACTION_CODE                     = 'RX'                       # Action Code (2: Change/Update, 4: Verify, RX: Replace)
BGN_07                              = ''                        # BGN07: Undefined
BGN_TRANS_SET_REF_NUM				= ''						# 7211
BGN_ORIGIN_TRANS_SET_REF_NUM		= ''
# Define Constants variable for the N1 Segment
## Entity Identifier Code
N1_PLAN_SPONSOR_CODE                = 'P5'
N1_INSURER_CODE                     = 'IN'
## Identification Code Qualifier
N1_EMPLOYER_ID_NUMBER               = '24'
N1_CODE_BY_ORGNIZATION              = '94'
N1_FEDERAL_ID_NUMBER                = 'FI'

SPONSER_NAME 						= 'LBMC Employment Partners LLC'
SPONSER_ID_NUMBER					= '06-0303370'

CIGNA_INS_ID_NUM					= '06-0303370'
BCBS_INS_ID_NUM						= '620427913'


