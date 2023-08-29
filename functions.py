from datetime import datetime, date
import pysftp
import pandas as pd
import math
import re
from constants import *

def writeTextOverSFTP(doc_content, isCigna, file_name):
    # SFTP connection parameters
    if isCigna == True:
        hostname = CIGNA_SFTP_HOST
        port = CIGNA_SFTP_PORT
        username = CIGNA_SFTP_USER
        password = CIGNA_SFTP_PASS
        remote_directory  = CIGNA_SFTP_PATH
    else:
        hostname = BCBS_SFTP_HOST
        port = BCBS_SFTP_PORT
        username = BCBS_SFTP_USER
        password = BCBS_SFTP_PASS
        remote_directory  = BCBS_SFTP_PATH
    remote_file_path = remote_directory  + file_name
    text_to_write = doc_content

    # Set up connection options to ignore host key verification
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    # Establish an SFTP connection
    with pysftp.Connection(hostname, username=username, password=password, cnopts=cnopts, port=port) as sftp:
        # Change directory to the remote directory
        if not sftp.exists(remote_directory):
            sftp.makedirs(remote_directory)

        # Write text to the remote file
        with sftp.open(remote_file_path, 'w') as remote_file:
            remote_file.write(text_to_write)

    print("Text written to remote file successfully")
def convert_date_to_ccyymmdd(date_param):
    """
    Convert a date parameter to the 'CCYYMMDD' format.
    If the input is a string, convert it to a datetime object and then to the desired format.
    """
    if date_param is None or date_param == 'NULL' or date_param == '':
        # return datetime.now().strftime("%Y%m%d")
        return ''

    if isinstance(date_param, str):
        try:
            if len(date_param) == 8:
                date_obj = datetime.strptime(date_param, '%Y%m%d')
            else:
                date_obj = datetime.strptime(date_param, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid date string format. Original value is: {date_param}. Expected 'YYYY-MM-DD' or 'CCYYMMDD'.")

    elif isinstance(date_param, (datetime, date)):
        date_obj = date_param
    else:
        raise TypeError("Input date must be either a string (format: 'YYYY-MM-DD' or 'CCYYMMDD') or a datetime object.")

    return date_obj.strftime('%Y%m%d')


def convert_to_gender_code(gender_string):
    """Convert gender string to gender code."""
    if len(gender_string) == 1:
        return gender_string  # Return the original value if it's a single character
    else:
        gender_mapping = {
            'Female': 'F',
            'Male': 'M',
            'Unknown': 'U'
        }
        return gender_mapping.get(gender_string, 'U')


def convert_to_2_length(input_string):
    """Truncate or pad the string to 2 characters."""
    return input_string[:2].zfill(2)


def convert_to_lenth_str(input_string, str_length):
    """Truncate or pad the string to the specified length."""
    return input_string[:str_length].zfill(str_length)


def generate_ISA(control_num):
    """Generate the ISA segment with the provided control number."""
    current_date = datetime.now().strftime("%y%m%d")  # YYMMDD
    current_time = datetime.now().strftime("%H%M")
    isa_segment = f"ISA*{ISA_AUTH_INFO_QUALIFIER}*{ISA_AUTH_INFO}*{ISA_SEC_INFO_QUALIFIER}*{ISA_SEC_INFO}*{ISA_SENDER_ID_QUALIFIER}*{ISA_SENDER_ID}*{ISA_RECEIVER_ID_QUALIFIER}*{ISA_RECEIVER_ID}*{current_date}*{current_time}*U*{ISA_CONTROL_VERSION_NUMBER}*{control_num:09}*{ISA_ACK_REQUESTED}*{ISA_USAGE_INDICATOR}*>~"
    return isa_segment


def generate_GS(control_num):
    """Generate the GS segment with the provided control number."""
    current_date = datetime.now().strftime("%Y%m%d")  # CCYYMMDD
    current_time = datetime.now().strftime("%H%M")
    gs_segment = f"GS*{GS_FUN_IDENTI_CODE}*{GS_APP_SENDER_CODE}*{GS_APP_RECEIV_CODE}*{current_date}*{current_time}*{control_num}*{GS_RES_AGENCY_CODE}*{GS_VER_REL_IND_IDENTI_CODE}~"
    return gs_segment


def generate_ST(control_num):
    """Generate the ST segment with the provided control number."""
    st_segment = f"ST*{ST_TRANS_SET_ID_CODE}*CA{control_num:07}*{ST_IMP_CONV_REFER}~"
    return st_segment


def generate_BGN(trans_set_purpurse_code, trans_set_ref_num, original_trans_set_ref_num):
    """Generate the BGN segment with the provided parameters."""
    current_date = datetime.now().strftime("%Y%m%d")  # CCYYMMDD
    current_time = datetime.now().strftime("%H%M%S%d") #HHMMSSDD  
    bgn_segment = f"BGN*{trans_set_purpurse_code}*{trans_set_ref_num}*{current_date}*{current_time}*{BGN_TIMEZONE_CODE}*{original_trans_set_ref_num}*{BGN_07}*{BGN_ACTION_CODE}~"
    return bgn_segment
def generate_N1(entity_id_code, name, id_code_qualifier,identifier):
    """Generate the N1 segment with the provided parameters."""
    n1_segment = f"N1*{entity_id_code}*{name}*{id_code_qualifier}*{identifier}~"
    return n1_segment
def generate_segment_from_array(data_array):
    """Generate the segment with the provided array."""
    result_segment = "*".join(data_array) + "~"
    return result_segment
def get_student_status_code(status_code):
    """Get Student Status Code with the provided string."""
    if status_code == 'Yes':
        return 'F'
    else:
        return 'N'

def convert_to_insurance_line_code(benefit_type):
    """Get Insurance Line Code with the provided string."""
    if benefit_type == 'Medical' or benefit_type == "MEDICAL"  or benefit_type == "MED":
        return 'HLT'
    elif benefit_type == 'Dental':
        return 'DEN'
    elif benefit_type == 'Vision':
        return 'VIS'
    else:
        return str.upper(convert_to_lenth_str(benefit_type, 3))

def convert_to_coverage_level_code(coverage_name):
    """Get Coverage Level Code with the provided string."""
    if coverage_name == 'Employee Only':
        return 'EMP'
    elif coverage_name == 'Employee + Family':
        return 'FAM'
    elif coverage_name == 'Employee + One':
        return 'EMP'
    if len(coverage_name) == 3:
        return coverage_name
    return 'EMP'
def generate_edi_for_person_from_json(provider_name, data, isSelf = True):
    """Get EDI with the provided json object."""
    segments = []
    # Generate Ins Segment
    ins_seg_array = [
        'INS',                                      # Segment Name
        'Y' if isSelf else 'N',                                        # Member Indicator (Y/N)
        data.get('RelationShipCode', '18'),                                   # Individual Relationship Code
        '030',                                      # Maintenance Type Code
        'XN',           # Maintenance Reason Code
        convert_to_lenth_str(str(data.get('BenefitStatusCode', 'A')),1),                   # Benefit Status Code
        '',             # Medicare Status Code
        '',                                         # Consolidated Omnibus Budget Reconciliation Act (COBRA) Qualifying Event Code
        data.get('EmployeeType', '') if data.get('EmployeeType', '') != None else '',                # Employment Status Code
        get_student_status_code(data.get('StudentStatus', '')) if data.get('StudentStatus', '') != None else '',                        # Student Status Code
        '',                             # Handicap Indicator
        '',                             # Date Time Period Format Qualifier  (Empty if no value for member individual death date)
        '',                             # Member Individual Death Date
        '',                             # Confidentiality Code (R: Restricted Access, U: Unrestricted Access)
        '',                             # Birth Sequence Number (Min 1, Max 9)
    ]
    data_ins_segment = generate_segment_from_array(ins_seg_array)
    print(f"Ins Segment: {data_ins_segment}")
    segments.append(data_ins_segment)


    # REF Segments (Subscriber Identifier)
    ref_seg_array = [
        'REF',                                          # Segment Name
        '0F',                                           # Reference Identification Qualifier
        re.sub(r'[-]', '', data.get('SocialSecurityNumber'))               # Subscriber Identifier
    ]
    data_ref_segment = generate_segment_from_array(ref_seg_array)
    print(f"REF Segment: {data_ref_segment}")
    segments.append(data_ref_segment)


    if provider_name != 'CIGNA':
        # REF Segments (Subscriber Identifier)
        ref_seg_array = [
            'REF',                                          # Segment Name
            '1L',                                           # Reference Identification Qualifier
            data.get('BCBCGruop')                           # Subscriber Identifier
        ]
        data_ref_segment = generate_segment_from_array(ref_seg_array)
        segments.append(data_ref_segment)

        # REF Segments (Subscriber Identifier)
        ref_seg_array = [
            'REF',                                          # Segment Name
            '17',                                           # Reference Identification Qualifier
            data.get('BCBCClass')                   # Subscriber Identifier
        ]
        data_ref_segment = generate_segment_from_array(ref_seg_array)
        segments.append(data_ref_segment)


    # REF Segments (Subscriber Identifier)
    ref_seg_array = [
        'REF',                                          # Segment Name
        'DX',                                           # Reference Identification Qualifier
        data.get('CompanyCode')               # Subscriber Identifier
    ]
    data_ref_segment = generate_segment_from_array(ref_seg_array)
    print(f"REF Segment: {data_ref_segment}")
    segments.append(data_ref_segment)
    if isSelf == True:
        # DTP Segments for Employment Started
        dtp_seg_array = [
            'DTP',                                      # Segment Name
            '336',                                      # Date Time Qualifier (336: Employment Begin)
            'D8',                                       # Date Expressed in Format CCYYMMDD
            convert_date_to_ccyymmdd(data.get('DateHired'))  # Status Information Effective Date
        ]
        data_dtp_segment = generate_segment_from_array(dtp_seg_array)
        # print(f"DTP Segments for Employment Started: {data_dtp_segment}")
        segments.append(data_dtp_segment)
        # DTP Segments for Employment End
        if data.get('TerminationDate') != None and data.get('TerminationDate') != '' :
            dtp_seg_array = [
                'DTP',                                      # Segment Name
                '337',                                      # Date Time Qualifier (337: Employment End)
                'D8',                                       # Date Expressed in Format CCYYMMDD
                convert_date_to_ccyymmdd(data.get('TerminationDate'))  # Status Information Effective Date
            ]
            data_dtp_segment = generate_segment_from_array(dtp_seg_array)
            # print(f"DTP Segments for Employment End: {data_dtp_segment}")
            segments.append(data_dtp_segment)

    # NM1 Segment
    nm1_seg_array = [
        'NM1',                                      # Segment Name
        'IL',                                       # Entity Identifier Code (74: Corrected Insured, IL: Insured or Subscriber)
        '1',                                        # Entity Type Qualifier
        data.get('LastName', ''),                       # Member Last Name
        data.get('FirstName', ''),                      # Member First Name
        '',                                         # Member Middle Name
        '',                                         # Member Name Prefix,
        '',                                         # Member Name Suffix,
        '34',                                       # Identification Code Qualifier (34: SSN, ZZ: Mutually Defined)
        re.sub(r'[-]', '', data.get('SocialSecurityNumber', '000000000')) # Member Identifier
    ]
    data_nm1_segment = generate_segment_from_array(nm1_seg_array)
    print(f"NM1 Segment: {data_nm1_segment}")
    segments.append(data_nm1_segment)


    if isSelf == True:
        # N3 Segment
        n3_seg_array = [
            'N3',                                       # Segment Name
            data.get('Address', 'Address')                        # Member Address Line
        ]
        data_n3_segment = generate_segment_from_array(n3_seg_array)
        print(f"N3 Segment: {data_n3_segment}")
        segments.append(data_n3_segment)

        # N4 Segment
        n4_seg_array = [
            'N4',                                       # Segment Name
            data.get('City', 'City'),                           # Member City Name
            convert_to_2_length(data.get('State', 'ST')),     # Member State Code (Min/Max 2)
            str(data.get('Zip', '00000')),                       # Member Postal Zone or Zip Code
            ''                                        # Country Code
        ]
        data_n4_segment = generate_segment_from_array(n4_seg_array)
        print(f"N4 Segment: {data_n4_segment}")
        segments.append(data_n4_segment)

    # DMG Segment
    dmg_seg_array = [
        'DMG',                                          # Segment Name
        'D8',                                           # Date Time Period Format Qualifier
        convert_date_to_ccyymmdd(data.get('BirthDate')),                           # Member Birth Date
        convert_to_gender_code(data.get('Gender')),     # Gender Code
        '',                                             # Marital Status Code
        '',                                             # Composite Race or Ethnicity Information
        '',                                             # Citizenship Status Code
        '',                                             # DMG-07
        '',                                             # DMG-08
        '',                                             # DMG-09
        '',                                             # Code List Qualifier Code
        ''                                              # Race or Ethnicit Collection Code
    ]
    data_dmg_segment = generate_segment_from_array(dmg_seg_array)
    print(f"DMG Segment: {data_dmg_segment}")
    segments.append(data_dmg_segment)

    for benefit in data.get("Benefits", []):
        # HD Segment
        coverage_plan = benefit.get('CoveragePlan')
        coverage_code = benefit.get('CoverageCode', '')
        hd_seg_array = [
            'HD',                                           # Segment Name
            '030',                                          # Maintenance Type Code
            '',
            convert_to_insurance_line_code(benefit.get('BenefitType', '')),                                           # Insurance Line Code
            coverage_plan if coverage_plan != None  else '',                                             # Plan Coverage Description
            convert_to_coverage_level_code(coverage_code if coverage_code != None else 'EMP') if isSelf == True else ''   ,# Coverage Level Code
            '',                                             # 
            '',                                             # 
            '',                                             # 
            'N'                                             # Late Enrollment Indicator
        ]
        data_hd_segment = generate_segment_from_array(hd_seg_array)
        print(f"HD Segment: {data_hd_segment}")
        segments.append(data_hd_segment)


        # DTP Segments for Health Coverage Dates
        dtp_seg_array = [
            'DTP',                                      # Segment Name
            '348',                                      # Date Time Qualifier (336: Employment Begin)
            'D8',                                       # Date Expressed in Format CCYYMMDD
            convert_date_to_ccyymmdd(benefit.get('CoverageEffectiveFrom'))  # Status Information Effective Date
        ]
        data_dtp_segment = generate_segment_from_array(dtp_seg_array)
        print(f"DTP Segments for Health Coverage Dates: {data_dtp_segment}")
        segments.append(data_dtp_segment)


        if convert_date_to_ccyymmdd(benefit.get('CoverageEffectiveTo')) != '':
            # DTP Segments for Health Coverage Dates
            dtp_seg_array = [
                'DTP',                                      # Segment Name
                '349',                                      # Date Time Qualifier (337: Employment End)
                'D8',                                       # Date Expressed in Format CCYYMMDD
                convert_date_to_ccyymmdd(benefit.get('CoverageEffectiveTo'))  # Status Information Effective Date
            ]
            data_dtp_segment = generate_segment_from_array(dtp_seg_array)
            print(f"DTP Segments for Health Coverage Dates: {data_dtp_segment}")
            segments.append(data_dtp_segment)
    
    for depent in data.get('Dependents', []):
        print('Dependent')
        segments += generate_edi_for_person_from_json(provider_name, depent, False)
        
    
   
    return segments
