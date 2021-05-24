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
    site_topology = dnac_func.get_site_topology(dnac_token)
    for site in site_topology['response']['sites']:
        print(site['name'], '-->', site['groupNameHierarchy'])
    physical_topology = dnac_func.get_physic_topology(dnac_token)
    physical_top_printout = dnac_func.get_nodes_links(physical_topology['response'])
    l2_topology = dnac_func.get_L2_topology('1',dnac_token)
    l2_topology_printout = dnac_func.get_nodes_links(l2_topology['response'])
if __name__ == "__main__":
    main()