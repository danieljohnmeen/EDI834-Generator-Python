import datetime
from constants import *
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