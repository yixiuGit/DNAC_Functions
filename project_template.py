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
    template_name = "DNA Center Guide - Day0"
    project_name = "Onboarding Configuration"
    # project_info = dnac_func.get_project_info(project_name, dnac_token)
    # project_id = dnac_func.get_project_id(project_name,dnac_token)
    # templates = dnac_func.get_all_template_info(dnac_token)
    # template_detail = dnac_func.get_template_detail(template_name, project_name, dnac_token)
    template_id = dnac_func.get_template_id(template_name, project_name, dnac_token)
    # template_ver = dnac_func.get_template_id_version(template_name, project_name, dnac_token)
    delete_template = dnac_func.delete_template(template_id, dnac_token)
    #
    # ## pnp onboarding
    # pnp_devices = dnac_func.pnp_get_device_list(dnac_token)
    # pnp_unclaimed_device_count = dnac_func.pnp_get_device_count('Unclaimed', dnac_token)
    # device_detail = dnac_func.get_site_design('10.10.20.81', dnac_token) #not working yet
    # workflows = dnac_func.pnp_workflows(dnac_token)
if __name__ == "__main__":
    main()