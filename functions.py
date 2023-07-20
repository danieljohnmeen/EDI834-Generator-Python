import datetime
import pandas as pd
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