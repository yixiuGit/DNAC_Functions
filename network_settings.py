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
    pool_info = {
        "settings": {
            "ippool": [
                {
                    "ipPoolName": "DNAC-Guide_Pool",
                    "type": "Generic",
                    "ipPoolCidr": "172.30.200.0/24",
                    "gateway": "172.30.200.1",
                    "dhcpServerIps": ["10.255.3.50"],
                    "dnsServerIps": ["10.255.3.50"],
                    "IpAddressSpace": "IPv4"
                }
            ]
        }
    }
    # probably because ip pool has been defined, the new ip range is in
    # the existing range, which is why could not be added
    new_pool = dnac_func.add_global_pool(pool_info, dnac_token)

    network = {
        "settings": {
            "dhcpServer": [
                "172.30.200.5"
            ],
            "dnsServer": {
                "domainName": "devnet.local",
                "primaryIpAddress": "172.30.200.6",
                "secondaryIpAddress": "172.30.200.7"
            },
            "syslogServer": {
                "ipAddresses": [
                    "10.255.0.1"
                ],
                "configureDnacIP": True
            }
        }
    }
    # change site name
    site_id = dnac_func.get_site_id('SYD', dnac_token)
    print(site_id)
    response = dnac_func.create_network(site_id, network, dnac_token)
    pprint(new_pool)
    pprint(response)
    # had error when create global pool and setup network as below
    # even after disable/enable REST API under platform
    # maybe because the sandbox is too old
    # < Response[404] >
    #{'error': 'BAPI not found with technicalName '
    #          '/v1/network/a50961a8-a792-4170-9b7e-8af65301a543 and restMethod '
    #          'POST'}
if __name__ == "__main__":
    main()