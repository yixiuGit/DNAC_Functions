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
    swim = dnac_func.get_swim_id(dnac_token)
    pprint(swim)
if __name__ == "__main__":
    main()