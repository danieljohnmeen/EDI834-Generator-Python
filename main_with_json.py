import time
import pandas as pd
from constants import *
from load_json import *
from functions import *


json_data = load_json_from_sql()
edi_documents = []
unique_control_num = 1
if json_data:
    for provider in json_data:
        provider_segments = []
        # EDI Document Data List for Each Provider
        edi_provider_documents = []
        provider_name = provider.get('Provider', 'N/A')
        print(f"{provider_name}")

        # ISA SEGMENT
        isa_segment = generate_ISA(unique_control_num)
        print(f"ISA SEGMENT: {isa_segment}")
        provider_segments.append(isa_segment)
        # END ISA SEGMENT

        # GS SEGMENT
        gs_segment = generate_GS(unique_control_num)
        print(f"GS SEGMENT: {gs_segment}")
        provider_segments.append(gs_segment)
        # END GS SEGMENT

        # ST SEGMENT
        st_segment = generate_ST(unique_control_num)
        print(f"ST SEGMENT: {st_segment}")
        provider_segments.append(st_segment)
        # END ST SEGMENT

        # BGN SEGMENT
        ## Pass the params for the BGN Segment here
        trans_set_ref_num = BGN_TRANS_SET_REF_NUM
        original_trans_set_ref_num = BGN_ORIGIN_TRANS_SET_REF_NUM
        bgn_segment = generate_BGN(BGN_TRANS_PURP_CODE_ORIGIN, trans_set_ref_num, original_trans_set_ref_num)
        print(f"BGN SEGMENT: {bgn_segment}")
        provider_segments.append(bgn_segment)
        #End BGN SEGMENT

        if provider_name != 'CIGNA':
            header_dtp_seg_array = [
                'DTP', '007', 'D8', datetime.now().strftime("%Y%m%d") 
            ]
            header_dtp_seg = generate_segment_from_array(header_dtp_seg_array)
            provider_segments.append(header_dtp_seg)
        # N1 SEGMENTS for Sponsor and Payer
        ## sponsor segment
        sponser_name = SPONSER_NAME
        sponsor_id_number = SPONSER_ID_NUMBER   # Sponser Identifier: Code identifying a party or other code (Min 2, Max 80)
        n1_sponsor_segment = generate_N1(N1_PLAN_SPONSOR_CODE, sponser_name, N1_FEDERAL_ID_NUMBER, sponsor_id_number)
        print(f"N1_SPONSOR: {n1_sponsor_segment}")
        provider_segments.append(n1_sponsor_segment)
        ## payer segment
        insurer_id_code = CIGNA_INS_ID_NUM if provider_name == 'CIGNA' else BCBS_INS_ID_NUM
        n1_payer_segment = generate_N1(N1_INSURER_CODE, provider_name, N1_FEDERAL_ID_NUMBER, insurer_id_code)
        provider_segments.append(n1_payer_segment)
        print(f"N1_PAYER: {n1_payer_segment}")

        for enrollee in provider.get("Enrollees", []):
            enrolleeId = enrollee.get("EmployeeId", 'N/A')
            provider_segments += generate_edi_for_person_from_json(provider_name, enrollee)
            
        # SE Segment
        se_seg_array = [
            'SE',                                          # Segment Name
            str(len(provider_segments) -1 ),                                           # Date Time Period Format Qualifier
            f'{unique_control_num:09}'
        ]
        data_se_segment = generate_segment_from_array(se_seg_array)
        print(f"SE Segment: {data_se_segment}")
        provider_segments.append(data_se_segment)
        # GE Segment
        ge_seg_array = [
            'GE',                                          # Segment Name
            '1',                                           # Date Time Period Format Qualifier
            f'{unique_control_num}'
        ]
        data_ge_segment = generate_segment_from_array(ge_seg_array)
        print(f"SE Segment: {data_ge_segment}")
        provider_segments.append(data_ge_segment)
        # IEA Segment
        iea_seg_array = [
            'IEA',                                          # Segment Name
            '1',                                           # Date Time Period Format Qualifier
            f'{unique_control_num:09}'
        ]
        data_iea_segment = generate_segment_from_array(iea_seg_array)
        print(f"SE Segment: {data_iea_segment}")
        provider_segments.append(data_iea_segment)

        provider_edi_document = "\n".join(provider_segments)
        if provider_name == 'CIGNA':
            file_name = f"{OUTPUT_FILE_PREFIX_CIGNA}_{time.time_ns()}.txt"  #customize file name for cigna
        else:
            file_name = f"{OUTPUT_FILE_PREFIX_BCBS}_{time.time_ns()}.txt"  #customize file name for bcbs
        with open(file_name, 'w') as file:
            file.write(provider_edi_document)
        print(f"End Writing EDI for {provider_name}")
        if provider_name == 'CIGNA' and CIGNA_SFTP_ALLOW == 'Y':
            writeTextOverSFTP(provider_edi_document, True, file_name)
        if provider_name != 'CIGNA' and BCBS_SFTP_ALLOW == 'Y':
            writeTextOverSFTP(provider_edi_document, False, file_name)
