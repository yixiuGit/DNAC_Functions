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
    cli_credentials = [
        {
            "comments": "CLI Credentials for the guide",
            "description": "Guide creds",
            "enablePassword": "Cisco123!",
            "password": "Cisco123!",
            "username": "dnac"
        }
    ]

    http_credentials = [
        {
            "comments": "DNA Center HTTP credentials",
            "description": "HTTP Creds",
            "password": "HTTP-cr3d$",
            "port": "443",
            "secure": "true",
            "username": "dna-http-user"
        }
    ]

    snmp_credentials = [
        {
            "authType": "SHA",
            "authPassword": "DNAC-2020",
            "snmpMode": "AUTHPRIV",
            "username": "dnac-guide",
            "privacyType": "AES128",
            "privacyPassword": "DNAC-PRIV-2020"
        },
        {
            "snmpMode": "NOAUTHNOPRIV",
            "username": "dnac-guide-2"
        }
    ]

    # new_credential = dnac_func.add_global_credential(cli_credentials,dnac_token)


if __name__ == "__main__":
    main()