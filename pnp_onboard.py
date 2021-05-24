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
    project_name = "Onboarding Configuration"
    project_id = dnac_func.get_project_id(project_name,dnac_token)
    # pnp_devices = dnac_func.pnp_get_device_list(dnac_token)
    # for p in pnp_devices:
    #     pprint(p['deviceInfo']['serialNumber'])
    #     if p['deviceInfo']['serialNumber'] == '919L3GOS8QC':
    #         pprint(p['id'])
    #         pnp_device_id = p['id']
    # pnp_delete_device = dnac_func.pnp_delete_device(pnp_device_id,dnac_token)
    sitename = "SYD"
    site_id = dnac_func.get_site_id(sitename, dnac_token)
    device_serial = '919L3GOS8QC'
    device_name = 'CAT9k-DNAC-Guide'
    device_pid = 'C9500-40X'
    # Create template
    template_info = {
        "name": "DNA Center Guide - Day0",
        "description": "Guide Configuration Template",
        "tags": [],
        "deviceTypes": [
            {
                "productFamily": "Switches and Hubs",
                "productSeries": "Cisco Catalyst 9500 Series Switches"
            }
        ],
        "softwareType": "IOS-XE",
        "softwareVariant": "XE",
        "templateContent": "ip access-list extended $permitACLName\npermit ip 10.0.0.0 0.255.255.25.0 any\npermit ip 172.16.0.0 0.15.255.255 any\npermit ip 192.168.0.0 0.0.255.255 any\n!\n\nip access-list extended $denyACLName\ndeny ip 10.0.0.0 0.255.255.25.0 any\ndeny ip 172.16.0.0 0.15.255.255 any\ndeny ip 192.168.0.0 0.0.255.255 any\n!\n",
        "rollbackTemplateContent": "",
        "templateParams": [
            {
                "parameterName": "permitACLName",
                "dataType": "STRING",
                "defaultValue": None,
                "description": None,
                "required": True,
                "notParam": False,
                "paramArray": False,
                "displayName": None,
                "instructionText": None,
                "group": None,
                "order": 1,
                "selection": {
                    "selectionType": None,
                    "selectionValues": {},
                    "defaultSelectedValues": []
                },
                "range": [],
                "key": None,
                "provider": None,
                "binding": ""
            },
            {
                "parameterName": "denyACLName",
                "dataType": "STRING",
                "defaultValue": None,
                "description": None,
                "required": True,
                "notParam": False,
                "paramArray": False,
                "displayName": None,
                "instructionText": None,
                "group": None,
                "order": 2,
                "selection": {
                    "selectionType": None,
                    "selectionValues": {},
                    "defaultSelectedValues": []
                },
                "range": [],
                "key": None,
                "provider": None,
                "binding": ""
            }
        ],
        "rollbackTemplateParams": [],
        "composite": False,
        "containingTemplates": []
    }

    response = dnac_func.create_template(project_id, template_info, dnac_token)
    task_id = response['response']['taskId']
    time.sleep(3)
    response = dnac_func.get_task(task_id, dnac_token)
    template_id = response['data']

    # Create site profile
    site_profile_info = {
        "name": "DNA Center Guide Profile",
        "namespace": "switching",
        "profileAttributes": [
            {
                "key": "day0.templates",
                "attribs": [
                    {
                        "key": "device.family",
                        "value": "Switches and Hubs",
                        "attribs": [
                            {
                                "key": "device.series",
                                "value": "Cisco Catalyst 9500 Series Switches",
                                "attribs": [
                                    {
                                        "key": "device.type",
                                        "attribs": [
                                            {
                                                "key": "template.id",
                                                "value": template_id,
                                            },
                                            {
                                                "key": "device.tag",
                                                "value": "",
                                                "attribs": [

                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    response = dnac_func.create_siteProfile(site_profile_info,dnac_token)
    task_id = response['taskId']

    time.sleep(3)
    response = dnac_func.get_task(task_id,dnac_token)
    # print(response)
    # site_profile_id = response['data']
    response = dnac_func.get_siteProfile(dnac_token)
    for profile in response['response']:
        if profile['name'] == "DNA Center Guide Profile":
            site_profile_id = profile['siteProfileUuid']
    print(site_profile_id)

    response = dnac_func.assign_site_to_siteProfile(site_profile_id, site_id, dnac_token)

    pnp_import_info =[
        {
            "deviceInfo": {
                "hostname": device_name,
                "serialNumber": device_serial,
                "pid": device_pid,
                "sudiRequired": False,
                "userSudiSerialNos": [],
                "aaaCredentials": {
                    "username": "",
                    "password": ""
                }
            }
        }
    ]

    response = dnac_func.pnp_device_import(pnp_import_info,dnac_token)
    pprint(response)
    device_id = response['successList'][0]['id']
    print(device_id)
    #
    claim_info = {
        "siteId": site_id,
        "deviceId": device_id,
        "type": "Default",
        # "imageInfo": {"imageId": "4b28b322-6675-4b29-97f0-885ef782087a", "skip": False},
        "configInfo": {
            "configId": template_id,
            "configParameters": {
                "permitACLName": "GUIDEALLOWACL",
                "denyACLName": "GUIDEDNEYACL"
            }
        },
        "imageInfo": {"imageId": "4b28b322-6675-4b29-97f0-885ef782087a", "skip": False}
    }

    device_claim = dnac_func.pnp_device_claim(claim_info, dnac_token)
    pprint(device_claim)
if __name__ == "__main__":
    main()
