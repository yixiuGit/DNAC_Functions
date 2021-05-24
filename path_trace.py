import time
import urllib3
import json
import logging
from pprint import pprint

import dnac_func


from requests.auth import HTTPBasicAuth  # for Basic Auth
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings

from config import DNAC_PASS, DNAC_USER


urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)


def main():
    dnac_token = dnac_func.get_dnac_token(DNAC_AUTH)
    #Need to change hostname
    query_string_params = {'hostname': 'leaf1.abc.inc'}
    response = dnac_func.get_device_info_with_filter(query_string_params, dnac_token)
    src_ip_address = response[0]['managementIpAddress']
    query_string_params = {'hostname': 'leaf2.abc.inc'}
    response = dnac_func.get_device_info_with_filter(query_string_params,dnac_token)
    dst_ip_address = response[0]['managementIpAddress']
    path_trace_payload = {
        'sourceIP': src_ip_address,
        'destIP': dst_ip_address,
        'inclusions': [
            'INTERFACE-STATS',
            'DEVICE-STATS',
            'ACL-TRACE',
            'QOS-STATS'
        ],
        'protocol': 'icmp'
    }

    response = dnac_func.create_path_trace(path_trace_payload, dnac_token)
    flow_analysis_id = response['response']['flowAnalysisId']
    # Waiting until the path trace is done
    time.sleep(10)

    response = dnac_func.get_path_trace_by_id(flow_analysis_id,dnac_token)
    pprint(response)

    response = dnac_func.delete_path_trace(flow_analysis_id,dnac_token)
    pprint(response.status_code)




if __name__ == "__main__":
    main()