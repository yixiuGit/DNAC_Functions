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
    # addnewsite = dnac_func.create_site("AUS", dnac_token)
    # addnewbuilding = dnac_func.create_building("AUS",'SYD',"376 Liverpool Rd, Ashfield NSW 2131", dnac_token)
    # Has problem to create new floor, script shows accepted, but unable to see in DNA
    addnewfloor = dnac_func.create_floor("AUS",'SYD','level1',dnac_token)
    # site_id = dnac_func.get_site_id('Germany',dnac_token)
    # building_id = dnac_func.get_building_id('AUS', 'SYD', dnac_token)
    # site_detail = dnac_func.get_site_detail(building_id,dnac_token) #can be site_id, building_id or floor_id
    # member_detail = dnac_func.get_site_memebership(building_id,dnac_token)
    # pprint(addnewfloor)
if __name__ == "__main__":
    main()