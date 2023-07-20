# Define constants variables

ENROLLEE_CSV = 'enrollees.csv'
DEPENDENT_CSV = 'dependents.csv'
PROVIDER_NAME_COL = 'Benefit Plan Provider Name'
EMPLOYEE_ID_COL = 'EmployeeId'
FIRST_NAME_COL = 'FirstName'
LAST_NAME_COL = 'LastName'
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