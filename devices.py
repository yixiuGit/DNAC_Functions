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
    # devices = dnac_func.get_all_device_info(dnac_token)
    # device_id_sn = dnac_func.get_device_id_sn('FCW2139G03G', dnac_token)
    # device_id_name = dnac_func.get_device_id_name('jk',dnac_token)
    # #device = dnac_func.get_device_info(device_id_sn,dnac_token)
    # device_info = dnac_func.get_device_info_ip(ip_address, dnac_token)
    # device_host, device_int = dnac_func.check_ipv4_network_interface(ip_address,dnac_token)
    # #device_config = dnac_func.get_device_config('leaf1',dnac_token)
    # #device_vlan = dnac_func.get_device_int_vlan('leaf1',dnac_token)
    # device_interface = dnac_func.get_device_int('spine1.abc.inc',"GigabitEthernet1/0/3", dnac_token)
    # int_detail = dnac_func.get_int_detail('1314444e-ad4c-473b-9711-9c20dc2a1319',dnac_token)
    adddevicetosite = dnac_func.assign_device_sn_building('FCW2139G03E','SYD', dnac_token)
    pprint(adddevicetosite)
if __name__ == "__main__":
    main()