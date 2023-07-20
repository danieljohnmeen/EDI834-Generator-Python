import datetime
import pandas as pd
import math
import re
from constants import *
def convert_date_to_ccyymmdd(date):
    if pd.notnull(date):
        date_obj = datetime.datetime.strptime(date, "%m/%d/%Y")
        return date_obj.strftime("%Y%m%d")
    return ''
def convert_to_gender_code(gender_string):
    gender_mapping = {
        'Female': 'F',
        'Male': 'M',
        'Unknown': 'U'
    }
    return gender_mapping.get(gender_string, 'U')
def convert_to_2_length(input_string):
    # Truncate the string to 2 characters if it's longer
    if len(input_string) > 2:
        return input_string[:2]
    # Pad the string with leading zeros to make it 2 characters long
    elif len(input_string) < 2:
        return input_string.zfill(2)
    else:
        return input_string
def convert_to_lenth_str(input_string, str_length):
    # Truncate the string to 2 characters if it's longer
    if len(input_string) > str_length:
        return input_string[:str_length]
    # Pad the string with leading zeros to make it 2 characters long
    elif len(input_string) < str_length:
        return input_string.zfill(str_length)
    else:
        return input_string
def generate_ISA(control_num):
    current_date = datetime.datetime.now().strftime("%y%m%d")  # YYMMDD
    current_time = datetime.datetime.now().strftime("%H%M")
    isa_segment = f"ISA*{ISA_AUTH_INFO_QUALIFIER}*{ISA_AUTH_INFO}*{ISA_SEC_INFO_QUALIFIER}*{ISA_SEC_INFO}*{ISA_SENDER_ID_QUALIFIER}*{ISA_SENDER_ID}*{ISA_RECEIVER_ID_QUALIFIER}*{ISA_RECEIVER_ID}*{current_date}*{current_time}*U*{ISA_CONTROL_VERSION_NUMBER}*{control_num:09}*{ISA_ACK_REQUESTED}*{ISA_USAGE_INDICATOR}*>~"
    return isa_segment
def generate_GS(control_num):
    current_date = datetime.datetime.now().strftime("%Y%m%d")  # CCYYMMDD
    current_time = datetime.datetime.now().strftime("%H%M")
    gs_segment = f"GS*{GS_FUN_IDENTI_CODE}*{GS_APP_SENDER_CODE}*{GS_APP_RECEIV_CODE}*{current_date}*{current_time}*{control_num}*{GS_RES_AGENCY_CODE}*{GS_VER_REL_IND_IDENTI_CODE}~"
    return gs_segment
def generate_ST(control_num):
    st_segment = f"ST*{ST_TRANS_SET_ID_CODE}*{control_num:09}*{ST_IMP_CONV_REFER}~"
    return st_segment
def generate_BGN(trans_set_purpurse_code, trans_set_ref_num, original_trans_set_ref_num):
    current_date = datetime.datetime.now().strftime("%Y%m%d")  # CCYYMMDD
    current_time = datetime.datetime.now().strftime("%H%M")
    bgn_segment = f"BGN*{trans_set_purpurse_code}*{trans_set_ref_num}*{current_date}*{current_time}*{BGN_TIMEZONE_CODE}*{original_trans_set_ref_num}*{BGN_07}*{BGN_ACTION_CODE}~"
    return bgn_segment
def generate_N1(entity_id_code, name, id_code_qualifier,identifier):
    n1_segment = f"N1*{entity_id_code}*{name}*{id_code_qualifier}*{identifier}~"
    return n1_segment
def generate_segment_from_array(data_array):
    result_segment = "*".join(data_array) + "~"
    return result_segment
def get_student_status_code(status_code):
    if status_code == 'Yes':
        return 'F'
    else:
        return 'N'
    
def generate_edi_for_person(data, ins_code):
    segments = []
    # Generate Ins Segment
    data_medicare_status_code = data['MedicarePlanCode']
    if data['MedicareReasonCode'] != '' and math.isnan(data['MedicareReasonCode']) == False:
        data_medicare_status_code = str(data_medicare_status_code) + '>' + str(int(data['MedicareReasonCode']))
    try:
        student_status_code_from_data = data['StudentStatus']
        student_status_code = get_student_status_code(student_status_code_from_data)
    except KeyError:
        student_status_code = 'N'
    ins_seg_array = [
        'INS',                                      # Segment Name
        'Y',                                        # Member Indicator (Y/N)
        ins_code,                                   # Individual Relationship Code
        '030',                                      # Maintenance Type Code
        str(data['ReasonCode']).zfill(2),           # Maintenance Reason Code
        str(data['BenefitStatusCode']),             # Benefit Status Code
        str(data_medicare_status_code),             # Medicare Status Code
        '',                                         # Consolidated Omnibus Budget Reconciliation Act (COBRA) Qualifying Event Code
        str(data['EmployeeStatus']),                # Employment Status Code
        student_status_code,                        # Student Status Code
        '',                             # Handicap Indicator
        '',                             # Date Time Period Format Qualifier  (Empty if no value for member individual death date)
        '',                             # Member Individual Death Date
        'U',                            # Confidentiality Code (R: Restricted Access, U: Unrestricted Access)
        '',                             # Birth Sequence Number (Min 1, Max 9)
    ]

    data_ins_segment = generate_segment_from_array(ins_seg_array)
    # print(f"Ins Segment: {data_ins_segment}")
    segments.append(data_ins_segment)


    # REF Segments (Subscriber Identifier)
    ref_seg_array = [
        'REF',                                      # Segment Name
        '0F',                                       # Reference Identification Qualifier
        str(data['EmployeeId'])                 # Subscriber Identifier
    ]
    data_ref_segment = generate_segment_from_array(ref_seg_array)
    # print(f"REF Segment: {data_ref_segment}")
    segments.append(data_ref_segment)
    # REF Segments (Member Policy Number) --- Optional
    ref_seg_array = [
        'REF',                                      # Segment Name
        '1L',                                       # Reference Identification Qualifier
        str(data['SocialSecurityNumber'])       # Member Group or Policy Number
    ]
    data_ref_segment = generate_segment_from_array(ref_seg_array)
    # print(f"Member Policy Number: {data_ref_segment}")
    segments.append(data_ref_segment)


    # DTP Segments for Employment Started
    dtp_seg_array = [
        'DTP',                                      # Segment Name
        '336',                                      # Date Time Qualifier (336: Employment Begin)
        'D8',                                       # Date Expressed in Format CCYYMMDD
        convert_date_to_ccyymmdd(data['DateHired'])  # Status Information Effective Date
    ]
    data_dtp_segment = generate_segment_from_array(dtp_seg_array)
    # print(f"DTP Segments for Employment Started: {data_dtp_segment}")
    segments.append(data_dtp_segment)
    # DTP Segments for Employment End
    dtp_seg_array = [
        'DTP',                                      # Segment Name
        '337',                                      # Date Time Qualifier (337: Employment End)
        'D8',                                       # Date Expressed in Format CCYYMMDD
        convert_date_to_ccyymmdd(data['TerminationDate'])  # Status Information Effective Date
    ]
    data_dtp_segment = generate_segment_from_array(dtp_seg_array)
    # print(f"DTP Segments for Employment End: {data_dtp_segment}")
    segments.append(data_dtp_segment)


    # NM1 Segment
    nm1_seg_array = [
        'NM1',                                      # Segment Name
        '74',                                       # Entity Identifier Code (74: Corrected Insured, IL: Insured or Subscriber)
        '1',                                        # Entity Type Qualifier
        data['LastName'],                       # Member Last Name
        data['FirstName'],                      # Member First Name
        '',                                         # Member Middle Name
        '',                                         # Member Name Prefix,
        '',                                         # Member Name Suffix,
        '34',                                       # Identification Code Qualifier (34: SSN, ZZ: Mutually Defined)
        re.sub(r'[-]', '', data['SocialSecurityNumber']) # Member Identifier
    ]
    data_nm1_segment = generate_segment_from_array(nm1_seg_array)
    # print(f"NM1 Segment: {data_nm1_segment}")
    segments.append(data_nm1_segment)



    # N3 Segment
    n3_seg_array = [
        'N3',                                       # Segment Name
        data['Address1']                        # Member Address Line
    ]
    data_n3_segment = generate_segment_from_array(n3_seg_array)
    # print(f"N3 Segment: {data_n3_segment}")
    segments.append(data_n3_segment)

    # N4 Segment
    n4_seg_array = [
        'N4',                                       # Segment Name
        data['City'],                           # Member City Name
        convert_to_2_length(data['State']),     # Member State Code (Min/Max 2)
        str(data['Zip']),                       # Member Postal Zone or Zip Code
        'US'                                        # Country Code
    ]
    data_n4_segment = generate_segment_from_array(n4_seg_array)
    # print(f"N4 Segment: {data_n4_segment}")
    segments.append(data_n4_segment)


    # DMG Segment
    dmg_seg_array = [
        'DMG',                                          # Segment Name
        'D8',                                           # Date Time Period Format Qualifier
        convert_date_to_ccyymmdd(data['BirthDate']),                           # Member Birth Date
        convert_to_gender_code(data['Gender']),     # Gender Code
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
    # print(f"DMG Segment: {data_dmg_segment}")
    segments.append(data_dmg_segment)


    # HD Segment
    hd_seg_array = [
        'HD',                                           # Segment Name
        '001',                                          # Maintenance Type Code
        '',
        'AH',                                           # Insurance Line Code
        '',                                             # Plan Coverage Description
        str.upper(convert_to_lenth_str(data['CoverageLevel'], 3))   ,# Coverage Level Code
        '',                                             # 
        '',                                             # 
        '',                                             # 
        'N'                                             # Late Enrollment Indicator
    ]
    data_hd_segment = generate_segment_from_array(hd_seg_array)
    # print(f"HD Segment: {data_hd_segment}")
    segments.append(data_hd_segment)


    # DTP Segments for Health Coverage Dates
    dtp_seg_array = [
        'DTP',                                      # Segment Name
        '348',                                      # Date Time Qualifier (336: Employment Begin)
        'D8',                                       # Date Expressed in Format CCYYMMDD
        convert_date_to_ccyymmdd(data['CoverageEffectiveFrom'])  # Status Information Effective Date
    ]
    data_dtp_segment = generate_segment_from_array(dtp_seg_array)
    # print(f"DTP Segments for Health Coverage Dates: {data_dtp_segment}")
    segments.append(data_dtp_segment)

    # DTP Segments for Health Coverage Dates
    dtp_seg_array = [
        'DTP',                                      # Segment Name
        '349',                                      # Date Time Qualifier (337: Employment End)
        'D8',                                       # Date Expressed in Format CCYYMMDD
        convert_date_to_ccyymmdd(data['CoverageEffectiveTo'])  # Status Information Effective Date
    ]
    data_dtp_segment = generate_segment_from_array(dtp_seg_array)
    # print(f"DTP Segments for Health Coverage Dates: {data_dtp_segment}")
    segments.append(data_dtp_segment)
    return segments
