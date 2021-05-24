import time
import urllib3
import logging
from pprint import pprint

import dnac_func


from requests.auth import HTTPBasicAuth  # for Basic Auth
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings

from config import DNAC_PASS, DNAC_USER


urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)


def main():
    #device_id = '85daf2da-571a-4570-9ce3-c68867ad891a'
    project_name = 'STR'
    template_name = 'str01'
    ip_address = '10.2.2.3'
    src_ip = '10.10.20.81'
    dest_ip = '10.10.20.82'

    dnac_token = dnac_func.get_dnac_token(DNAC_AUTH)

    ## Network Discovery

    credentials = dnac_func.get_global_credential('CLI',dnac_token)

    ## Network Discovery

    ## Device level
    devices = dnac_func.get_all_device_info(dnac_token)
    device_sn_id = dnac_func.get_device_id_sn('FCW2214L0VK', dnac_token)
    device_name_id = dnac_func.get_device_id_name('leaf1',dnac_token)
    device = dnac_func.get_device_info(device_sn_id,dnac_token)
    device_info = dnac_func.get_device_info_ip(ip_address, dnac_token)
    device_host, device_int = dnac_func.check_ipv4_network_interface(ip_address,dnac_token)
    device_config = dnac_func.get_device_config('leaf1',dnac_token)
    #adddevicetosite = dnac_func.assign_device_sn_building('FCW2214L0VK','abc', dnac_token)



    ## Project&Template level
    project_info = dnac_func.get_project_info(project_name, dnac_token)
    project_id = dnac_func.get_project_id(project_name,dnac_token)
    templates = dnac_func.get_all_template_info(dnac_token)
    template_detail = dnac_func.get_template_detail(template_name, project_name, dnac_token)



    ## pnp onboarding
    pnp_devices = dnac_func.pnp_get_device_list(dnac_token)
    pnp_unclaimed_device_count = dnac_func.pnp_get_device_count('Unclaimed', dnac_token)
    device_detail = dnac_func.get_site_design('10.10.20.81', dnac_token) #not working yet

    ## Site level
    # #Need test for this
    # #addnewsite = dnac_func.create_site("AUS", dnac_token)
    #addnewbuilding = dnac_func.create_building("AUS",'global','ABC',"376 Liverpool Rd, Ashfield NSW 2131", dnac_token)
    #addnewfloor = dnac_func.create_floor("AUS",'global','ABC','GF',dnac_token)
    site_id = dnac_func.get_site_id('Germany',dnac_token)
    building_id = dnac_func.get_building_id('HQ', 'Floor 17', dnac_token)
    site_detail = dnac_func.get_site_detail(building_id,dnac_token) #can be site_id, building_id or floor_id
    member_detail = dnac_func.get_site_memebership(building_id,dnac_token)



    ## Assurance
    #permission issue, unable to run
    #path_id = dnac_func.create_path_trace(src_ip,dest_ip,dnac_token)
    pprint(member_detail)




if __name__ == '__main__':
    main()