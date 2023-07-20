import datetime
from constants import *
def generate_ISA(control_num):
    current_date = datetime.datetime.now().strftime("%Y%m%d")  # CCYYMMDD
    current_time = datetime.datetime.now().strftime("%H%M")
    isa_segment = f"ISA*{ISA_AUTH_INFO_QUALIFIER}*{ISA_AUTH_INFO}*{ISA_SEC_INFO_QUALIFIER}*{ISA_SEC_INFO}*{ISA_SENDER_ID_QUALIFIER}*{ISA_SENDER_ID}*{ISA_RECEIVER_ID_QUALIFIER}*{ISA_RECEIVER_ID}*{current_date}*{current_time}*U*{ISA_CONTROL_VERSION_NUMBER}*{control_num:09}*{ISA_ACK_REQUESTED}*{ISA_USAGE_INDICATOR}*>~"
    return isa_segment
