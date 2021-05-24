import requests
import json
import time
import urllib3
from pprint import pprint


from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
from requests.auth import HTTPBasicAuth  # for Basic Auth

from config import DNAC_URL, DNAC_PASS, DNAC_USER


urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)

def get_dnac_token(dnac_auth):
    """
    Create the authorization token required to access DNA C
    Call to DNA C - /api/system/v1/auth/login
    :param dnac_auth - DNA C Basic Auth string
    :return: DNA C JWT token
    """

    url = DNAC_URL + '/dna/system/api/v1/auth/token'
    header = {'content-type': 'application/json'}
    response = requests.post(url, auth=dnac_auth, headers=header, verify=False)
    dnac_token = response.json()['Token']
    return dnac_token



#######  Network
def get_netwrok(dnac_token):
    """
    The function will return DHCP and DNS info
    :param credential_type: credential type
    :param dnac_token: DNA C token
    :return: DNA C device inventory info
    """
    url = DNAC_URL + '/dna/intent/api/v1/network'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    network_response = requests.get(url, headers=header, verify=False)
    network = network_response.json()
    return network

def get_global_pool(dnac_token):
    """
    The function will return DHCP and DNS info
    :param dnac_token: DNA C token
    :return: DNA C device inventory info
    """
    url = DNAC_URL + '/dna/intent/api/v1/global-pool'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    pool_response = requests.get(url, headers=header, verify=False)
    global_pool = pool_response.json()
    return global_pool


def create_network(site_id, network_info, dnac_token):
    """
    The function will return DHCP and DNS info
    :param credential_type: credential type
    :param dnac_token: DNA C token
    :return: DNA C device inventory info
    """
    url = DNAC_URL + '/dna/intent/api/v1/network/' + site_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    network_response = requests.post(url, headers=header, data=json.dumps(network_info),verify=False)
    network = network_response.json()
    return network
####### Network

#######  Network Discovery
def get_global_credential(credential_type, dnac_token):
    """
    The function will return all network devices info
    :param credential_type: credential type CLI / SNMPV2_READ_COMMUNITY / SNMPV2_WRITE_COMMUNITY / SNMPV3 / HTTP_WRITE / HTTP_READ / NETCONF
    :param dnac_token: DNA C token
    :return: DNA C device inventory info
    """
    url = DNAC_URL + '/dna/intent/api/v1/global-credential?credentialSubType=' + credential_type
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    credential_response = requests.get(url, headers=header, verify=False)
    credential = credential_response.json()
    return credential


#######  Network Discovery




#######  Device related

def get_all_device_info(dnac_token):
    """
    The function will return all network devices info
    :param dnac_token: DNA C token
    :return: DNA C device inventory info
    """
    url = DNAC_URL + '/dna/intent/api/v1/network-device'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    all_device_response = requests.get(url, headers=header, verify=False)
    all_device_info = all_device_response.json()
    return all_device_info['response']

def get_device_info_with_filter(filter,dnac_token):
    """
    The function will return all network devices info
    :param filter: search criteria
    :param dnac_token: DNA C token
    :return: list of network devices based on filter criteria
    """
    url = DNAC_URL + '/dna/intent/api/v1/network-device'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    all_device_response = requests.get(url, headers=header, params=filter, verify=False)
    all_device_info = all_device_response.json()
    return all_device_info['response']

def get_device_info(device_id, dnac_token):
    """
    This function will retrieve all the information for the device with the DNA C device id
    :param device_id: DNA C device_id
    :param dnac_token: DNA C token
    :return: device info
    """
    url = DNAC_URL + '/dna/intent/api/v1/network-device?id=' + device_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    device_response = requests.get(url, headers=header, verify=False)
    device_info = device_response.json()
    return device_info['response'][0]

def get_device_id_sn(device_sn, dnac_token):
    """
    The function will return the DNA C device id for the device with serial number {device_sn}
    :param device_sn: network device SN
    :param dnac_token: DNA C token
    :return: DNA C device id
    """
    url = DNAC_URL + '/dna/intent/api/v1/network-device/serial-number/' + device_sn
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    device_response = requests.get(url, headers=header, verify=False)
    device_info = device_response.json()
    device_id = device_info['response']['id']
    return device_id

def get_device_id_name(device_name, dnac_token):
    """
    This function will find the DNA C device id for the device with the name {device_name}
    :param device_name: device hostname
    :param dnac_token: DNA C token
    :return:
    """
    device_id = None
    device_list = get_all_device_info(dnac_token)
    for device in device_list:
        if device['hostname'] == device_name:
            device_id = device['id']
    return device_id

def get_device_int_vlan(device_name, dnac_token):
    """
    This function will find the DNA C device vlan info base on the name {device_name}
    :param device_name: device hostname
    :param dnac_token: DNA C token
    :return:
    """
    uuid = get_device_id_name(device_name, dnac_token)
    url = DNAC_URL + '/dna/intent/api/v1/network-device/' + uuid + '/vlan'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    device_response = requests.get(url, headers=header, verify=False)
    vlan_info = device_response.json()
    return vlan_info


def get_device_int(device_name, int_name,dnac_token):
    """
    This function will find the DNA C interface info
    :param device_name: device hostname
    :param int_name: interface name
    :param dnac_token: DNA C token
    :return: interface and related device info such as interface type, id, vlan,mac, status etc
             device id, sn, pid etc
    """
    device_id = get_device_id_name(device_name, dnac_token)
    url = DNAC_URL + '/dna/intent/api/v1/interface/network-device/' + device_id + '/interface-name?name=' + int_name
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    device_response = requests.get(url, headers=header,verify=False)
    int_info = device_response.json()
    return int_info

def get_int_detail(int_id, dnac_token):
    """
    This function will find the DNA C interface info
    :param int_id: interface id
    :param dnac_token: DNA C token
    :return: interface and related device info such as interface type, id, vlan,mac, status etc
             device id, sn, pid etc
    """
    url = DNAC_URL + '/dna/intent/api/v1/interface/' + int_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.get(url, headers=header,verify=False)
    int_info = response.json()
    return int_info


def check_ipv4_network_interface(ip_address, dnac_token):
    """
    This function will check if the provided IPv4 address is configured on any network interfaces
    :param ip_address: IPv4 address
    :param dnac_token: DNA C token
    :return: None, or device_hostname and interface_name
    """
    url = DNAC_URL + '/dna/intent/api/v1/interface/ip-address/' + ip_address
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.get(url, headers=header, verify=False)
    response_json = response.json()
    try:
        response_info = response_json['response'][0]
        interface_name = response_info['portName']
        device_id = response_info['deviceId']
        device_info = get_device_info(device_id, dnac_token)
        device_hostname = device_info['hostname']
        return device_hostname, interface_name
    except:
        device_info = get_device_info_ip(ip_address, dnac_token)  # required for AP's
        device_hostname = device_info['hostname']
        return device_hostname, ''



def get_device_info_ip(ip_address, dnac_token):
    """
    This function will retrieve the device information for the device with the management IPv4 address {ip_address}
    :param ip_address: device management ip address
    :param dnac_token: DNA C token
    :return: device information, or None
    """
    url = DNAC_URL + '/dna/intent/api/v1/network-device/ip-address/' + ip_address
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.get(url, headers=header, verify=False)
    response_json = response.json()
    device_info = response_json['response']
    if 'errorCode' == 'Not found':
        return None
    else:
        return device_info


def get_device_config(device_name, dnac_token):
    """
    This function will get the configuration file for the device with the name {device_name}
    :param device_name: device hostname
    :param dnac_token: DNA C token
    :return: configuration file
    """
    device_id = get_device_id_name(device_name, dnac_token)
    url = DNAC_URL + '/dna/intent/api/v1/network-device/' + device_id + '/config'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.get(url, headers=header, verify=False)
    config_json = response.json()
    config_file = config_json['response']
    return config_file


def assign_device_sn_building(device_sn, building_name, dnac_token):
    """
    This function will assign a device with the specified SN to a building with the name {building_name}
    :param device_sn: network device SN
    :param building_name: DNA C building name
    :param dnac_token: DNA C token
    :return:
    """
    # get the building and device id's
    building_id = get_building_id('AUS',building_name, dnac_token)
    device_id = get_device_id_sn(device_sn, dnac_token)

    url = DNAC_URL + '/dna/system/api/v1/site/' + building_id + '/device'
    payload = {"id": device_id}
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    return response.json()
#######  Device related




#######  Site Design
#not working yet
def get_site_design(ip_addr,dnac_token):
    """
    This function will assign a device with the specified SN to a building with the name {building_name}
    :param ip_addr: network device ip address
    :param dnac_token: DNA C token
    :return: device detail
    """
    url = DNAC_URL + '/dna/intent/api/v1/business/nfv/provisioningDetail/'
    payload = {"device_ip": ip_addr}
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.get(url, data=json.dumps(payload), headers=header, verify=False)
    return response
#######  Site Design




#########   Project/Template related

def get_project_info(project_name, dnac_token):
    """
    This function will retrieve all templates associated with the project with the name {project_name}
    :param project_name: project name
    :param dnac_token: DNA C token
    :return: list of all templates, including names and ids
    """
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/project?name=' + project_name
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.get(url, headers=header, verify=False)
    project_json = response.json()
    template_list = project_json[0]['templates']
    return template_list

def get_project_id(project_name, dnac_token):
    """
    This function will retrieve the CLI templates project id for the project with the name {project_name}
    :param project_name: CLI project template
    :param dnac_token: DNA token
    :return: project id
    """
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/project?name=' + project_name
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.get(url, headers=header, verify=False)
    proj_json = response.json()
    proj_id = proj_json[0]['id']
    return proj_id



def get_all_template_info(dnac_token):
    """
    This function will return the info for all CLI templates existing on DNA C, including all their versions
    :param dnac_token: DNA C token
    :return: all info for all templates
    """
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/template'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.get(url, headers=header, verify=False)
    all_template_list = response.json()
    return all_template_list


def get_template_id(template_name, project_name, dnac_token):
    """
    This function will return the latest version template id for the DNA C template with the name {template_name},
    part of the project with the name {project_name}
    :param template_name: name of the template
    :param project_name: Project name
    :param dnac_token: DNA C token
    :return: DNA C template id
    """
    template_list = get_project_info(project_name, dnac_token)
    template_id = None
    for template in template_list:
        if template['name'] == template_name:
            template_id = template['id']
    return template_id




def get_template_detail(template_name, project_name, dnac_token):
    """
    This function will return the info for the CLI template with the name {template_name}
    :param template_name: template name
    :param project_name: Project name
    :param dnac_token: DNA C token
    :return: all info for all templates
    """
    template_id = get_template_id(template_name, project_name, dnac_token)
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/template/' + template_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.get(url, headers=header, verify=False)
    template_json = response.json()
    return template_json


def get_template_id_version(template_name, project_name, dnac_token):
    """
    This function will return the latest version template id for the DNA C template with the name {template_name},
    part of the project with the name {project_name}
    :param template_name: name of the template
    :param project_name: Project name
    :param dnac_token: DNA C token
    :return: DNA C template id for the last version
    """
    template_id = get_template_id(template_name, project_name, dnac_token)
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/template/version/' + template_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.get(url, headers=header, verify=False)
    project_json = response.json()
    for template in project_json:
        if template['name'] == template_name:
            version = 0
            versions_info = template['versionsInfo']
            for ver in versions_info:
                try:
                    if int(ver['version']) > version:
                        template_id_ver = ver['id']
                        version = int(ver['version'])
                except:
                    pass
    return template_id_ver

def create_template(project_id, template, dnac_token):
    """
    This function will return the info for the CLI template with the name {template_name}
    :param project_id: project ID
    :param template: template detail
    :param dnac_token: DNA C token
    :return: all info for all templates
    """
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/project/' + project_id + '/template'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.post(url, headers=header, data=json.dumps(template),verify=False)
    template_json = response.json()
    return template_json

def delete_template(template_id, dnac_token):
    """
    This function will return the info for the CLI template with the name {template_name}
    :param template_id: template ID
    :param dnac_token: DNA C token
    :return: all info for all templates
    """
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/template/' + template_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.delete(url, headers=header, verify=False)
    return response
########  Project/Template related




########   pnp related
def pnp_get_device_list(dnac_token):
    """
    This function will retrieve the PnP device list info
    :param dnac_token: DNA C token
    :return: PnP device info
    """
    url = DNAC_URL + '/dna/intent/api/v1/onboarding/pnp-device'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.get(url, headers=header, verify=False)
    pnp_device_json = response.json()
    return pnp_device_json


def pnp_get_device_count(device_state, dnac_token):
    """
    This function will return the count of the PnP devices in the state {state}
    :param device_state: device state, example 'Unclaimed'
    :param dnac_token: DNA C token
    :return: device count
    """
    url = DNAC_URL + '/dna/intent/api/v1/onboarding/pnp-device/count'
    payload = {'state': device_state}
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.get(url, headers=header, data=json.dumps(payload), verify=False)
    pnp_device_count = response.json()
    return pnp_device_count['response']


def pnp_workflows(dnac_token):
    """
    This function will retrieve the PnP device list info
    :param dnac_token: DNA C token
    :return: PnP device info
    """
    url = DNAC_URL + '/dna/intent/api/v1/onboarding/pnp-workflow'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.get(url, headers=header, verify=False)
    pnp_workflow = response.json()
    return pnp_workflow


def pnp_device_import(pnp_import_info, dnac_token):
    """
        This function will retrieve the PnP device list info
        :param pnp_import_info: imported devices info
        :param dnac_token: DNA C token
        :return: PnP device info
        """
    url = DNAC_URL + '/dna/intent/api/v1/onboarding/pnp-device/import'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.post(url, headers=header, data=json.dumps(pnp_import_info),verify=False)
    import_info = response.json()
    return import_info


def pnp_device_claim(pnp_claim_info, dnac_token):
    """
        This function will retrieve the PnP device list info
        :param pnp_claim_info: imported devices info
        :param dnac_token: DNA C token
        :return: PnP device info
        """
    url = DNAC_URL + '/dna/intent/api/v1/onboarding/pnp-device/site-claim'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.post(url, headers=header, json=pnp_claim_info,verify=False)
    # response = requests.post(url, headers=header, data=json.dumps(pnp_claim_info), verify=False)
    claim_info = response.json()
    return claim_info


def pnp_delete_device(device_id,dnac_token):
    """
    This function will retrieve the PnP device list info
    :param device_id: pnp device id
    :param dnac_token: DNA C token
    :return: PnP device info
    """
    url = DNAC_URL + '/dna/intent/api/v1/onboarding/pnp-device/' + device_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.delete(url, headers=header, verify=False)
    return response
########  pnp related


######   Site related

def get_site_id (site_name, dnac_token):
    """
    The function will get the DNA C site id for the site with the name {site_name}
    :param site_name: DNA C site name
    :param dnac_token: DNA C token
    :return: DNA C site id
    """
    url = DNAC_URL + '/dna/intent/api/v1/site'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    site_response = requests.get(url, headers=header, verify=False)
    site_json = site_response.json()
    site_list = site_json['response']
    for site in site_list:
        if site_name == site['name']:
            site_id = site['id']
    return site_id


def get_building_id (site_name,building_name, dnac_token):
    """
    The function will get the DNA C site id for the site with the name {site_name}
    :param site_name: DNA C site name
    :param dnac_token: DNA C token
    :return: DNA C site id
    """
    url = DNAC_URL + '/dna/intent/api/v1/site?name=global/' + site_name + '/' + building_name
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    building_response = requests.get(url, headers=header, verify=False)
    building_json = building_response.json()
    building_list = building_json['response']
    for building in building_list:
        #pprint(building['additionalInfo'][0]['attributes'])
        if building_name == building['name']:
            building_id = building['id']
    return building_id



def get_site_detail (site_id, dnac_token):
    """
    The function will get the DNA C site basic information based on site id {site_id}
    :param stie_id: DNA C site, building or floor id
    :param dnac_token: DNA C token
    :return: DNA C site id
    """
    url = DNAC_URL + '/dna/intent/api/v1/site?siteId='+site_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    site_response = requests.get(url, headers=header, verify=False)
    site_detail = site_response.json()
    return site_detail


def get_site_memebership(site_id, dnac_token):
    """
    The function will get the DNA C devices' information associated with a particular site {site_id}
    :param site_id: DNA C site, building or floor id
    :param dnac_token: DNA C token
    :return: DNA C site id
    """
    url = DNAC_URL + '/dna/intent/api/v1/membership/'+site_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    member_response = requests.get(url, headers=header, verify=False)
    membership = member_response.json()
    return membership


def create_site(site_name, dnac_token):
    """
    The function will create a new site with the name {site_name}
    :param site_name: DNA C site name
    :param dnac_token: DNA C token
    :return: none
    """

    payload = {
    "type": "area",
        "site": {
            "area": {
                "name": site_name,
                "parentName": "Global"
            }
        }
    }
    url = DNAC_URL + '/dna/intent/api/v1/site'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    site = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    return site.json()

def create_building(site_name, bld_name, bld_address,dnac_token):
    """
    The function will create a new site with the name {site_name}
    :param site_name: DNA C site name
    :param site_parentname: DNA C parent site name(global)
    :param bld_name: DNA C building name
    :param bld_address: DNA C building address
    :param dnac_token: DNA C token
    :return: none
    either latitude&longitude is compulsory or address is compulsory
    """
    site_id = get_site_id("AUS", dnac_token)
    # payload = {
    #     "type": "building",
    #     "site": {
    #         "building": {
    #             "name": bld_name,
    #             "parentName": "Global/" + site_name,
    #             "latitude": "37.409424",
    #             "longitude": "-121.928868"
    #         }
    #     }
    # }
    payload = {
        "type": "building",
        "site": {
            "building": {
                "name": bld_name,
                "parentName": "Global/" + site_name,
                "address": bld_address

            }
        }
    }
    url = DNAC_URL + '/dna/intent/api/v1/site'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    building=requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    return building.json()

def create_floor(site_name, bld_name, floor_name,dnac_token):
    """
    The function will create a new site with the name {site_name}
    :param site_name: DNA C site name
    :param site_parentname: DNA C parent site name(global)
    :param bld_name: DNA C building name
    :param floor_name: DNA C floor name
    :param dnac_token: DNA C token
    :return: none
    unable to create floor, need to find the reasons
    """
    payload = {
    "type": "floor",
        "site": {
            "floor": {
                "name": floor_name,
                "parentName": "Global/" + site_name + "/" + bld_name,
                "rfModel": "Cubes And Walled Offices",
                "width": 50,
                "length": 60,
                "height": 10
            }
         }
    }
    url = DNAC_URL + '/dna/intent/api/v1/site'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    return response.json()
#######  Site related



######  Assurance related

def create_path_trace(path_trace_payload, dnac_token):
    """
    This function will create a new Path Trace between the source IP address and the
    destination IP address
    :param path_trace_payload: Source IP address
    :param dnac_token: DNA C tokenf
    :return: DNA C path visualisation id
    """


    url = DNAC_URL + '/dna/intent/api/v1/flow-analysis'
    header = {'accept': 'application/json', 'content-type': 'application/json', 'x-auth-token': dnac_token}
    path_response = requests.post(url, data=json.dumps(path_trace_payload), headers=header, verify=False)
    path_json = path_response.json()
    return path_json


def get_path_trace_by_id(trace_id, dnac_token):
    url = DNAC_URL + '/dna/intent/api/v1/flow-analysis'  + trace_id
    header = {'accept': 'application/json', 'content-type': 'application/json', 'x-auth-token': dnac_token}
    path_response = requests.get(url, headers=header, verify=False)
    path_json = path_response.json()
    pprint(path_json)
    return path_json

def delete_path_trace(trace_id, dnac_token):
    url = DNAC_URL + '/dna/intent/api/v1/flow-analysis' + trace_id
    header = {'accept': 'application/json', 'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.delete(url, headers=header, verify=False)
    return response

def get_site_health(timestamp, dnac_token):
    """
    This function will return overall health info for all sites
    :param timestamp: epoch time
    :param dnac_token: DNA C token
    :return: DNA C each site health info
    """
    url = DNAC_URL + '/dna/intent/api/v1/site-health?timestamp='+timestamp
    header = {'accept': 'application/json', 'content-type': 'application/json', 'x-auth-token': dnac_token}
    site_health = requests.get(url, headers=header, verify=False)
    return site_health.json()

def get_network_health(timestamp, dnac_token):
    """
    This function will return Overall Network Health information by Device category
    (Access, Distribution, Core, Router, Wireless) for any given point of time
    :param timestamp: epoch time
    :param dnac_token: DNA C token
    :return: DNA C Global overall health info
    """
    url = DNAC_URL + '/dna/intent/api/v1/network-health?timestamp='+timestamp
    header = {'accept': 'application/json', 'content-type': 'application/json', 'x-auth-token': dnac_token}
    site_health = requests.get(url, headers=header, verify=False)
    return site_health.json()

def get_client_health(timestamp, dnac_token):
    """
    This function will return Overall Client Health information by Client type
    (Wired and Wireless) for any given point of time
    :param timestamp: epoch time
    :param dnac_token: DNA C token
    :return: DNA C Global overall health info
    """
    url = DNAC_URL + '/dna/intent/api/v1/client-health?timestamp='+timestamp
    header = {'accept': 'application/json', 'content-type': 'application/json', 'x-auth-token': dnac_token}
    client_health = requests.get(url, headers=header, verify=False)
    return client_health.json()

# Have problem to retrieve info, need to test later
def get_client_health_detail(timestamp, mac, dnac_token):
    """
    This function will return  detailed Client information retrieved by
    Mac Address for any given point of time.
    :param timestamp: epoch time
    :param mac : client mac address
    :param dnac_token: DNA C token
    :return: DNA C Global overall health info
    """
    url = DNAC_URL + '/dna/intent/api/v1/client-detail?macAddress='+mac
    header = {'accept': 'application/json', 'content-type': 'application/json', 'x-auth-token': dnac_token}
    client_health_detail = requests.get(url, headers=header, verify=False)
    return client_health_detail.json()



###### Site Profile
def get_siteProfile(dnac_token):
    """
    This function will return basic info of site profile(network profiles).
    :param dnac_token: DNA C token
    :return: DNA C network profile info
    """
    url = DNAC_URL + '/api/v1/siteprofile'
    header = {'accept': 'application/json', 'content-type': 'application/json', 'x-auth-token': dnac_token}
    siteprofile = requests.get(url, headers=header, verify=False)
    return siteprofile.json()

def get_siteprofile_detail(siteprofile_id, dnac_token):
    """
    This function will return basic info of a particular site profile(network profiles).
    :param siteprofile_id : network profile id
    :param dnac_token: DNA C token
    :return: DNA C network profile info
    """
    url = DNAC_URL + '/api/v1/siteprofile/' + siteprofile_id
    url = DNAC_URL + '/api/v1/siteprofile/507b88b2-d6a9-4a4e-a084-70b6733c5315'
    header = {'accept': 'application/json', 'content-type': 'application/json', 'x-auth-token': dnac_token}
    siteprofile = requests.get(url, headers=header, verify=False)
    return siteprofile.json()

def create_siteProfile(site_profile_info, dnac_token):
    """
    This function will return basic info of a particular site profile(network profiles).
    :param site_profile_info : network profile configuration
    :param dnac_token: DNA C token
    :return: DNA C network profile info
    Can create network profile, but not as same as manual creation via UI
    """
    url = DNAC_URL + '/api/v1/siteprofile'
    header = {'accept': 'application/json', 'content-type': 'application/json', 'x-auth-token': dnac_token}
    siteprofile = requests.post(url, headers=header, data=json.dumps(site_profile_info),verify=False)
    return siteprofile.json()['response']

def assign_site_to_siteProfile(siteProfile_id,site_id,dnac_token):
    """
    This function will return basic info of a particular site profile(network profiles).
    :param siteprofile_id : network profile id
    :param site_id : site id that need to associate with site profile
    :param dnac_token: DNA C token
    :return: DNA C network profile info
    """
    url = DNAC_URL + '/api/v1/siteprofile/' + siteProfile_id + '/site/' + site_id
    header = {'accept': 'application/json', 'content-type': 'application/json', 'x-auth-token': dnac_token}
    siteprofile = requests.post(url, headers=header, verify=False)
    return siteprofile.json()
#####  Site Profile

##########################################################################
##___________________________________________________________________
def add_global_pool(pool_info, dnac_token):
    """
    The function will return DHCP and DNS info
    :param dnac_token: DNA C token
    :return: DNA C device inventory info
    """
    url = DNAC_URL + '/dna/intent/api/v1/global-pool'
    header = {'accept': 'application/json', 'content-type': 'application/json', 'x-auth-token': dnac_token}
    pool_response = requests.post(url, headers=header, data=json.dumps(pool_info),verify=False)
    pool_response = requests.post(url, headers=header, json=pool_info, verify=False)
    global_pool = pool_response.json()
    return pool_response


def add_global_credential(credential, dnac_token):
    """
    The function will return DHCP and DNS info
    :param dnac_token: DNA C token
    :return: DNA C device inventory info
    """
    url = DNAC_URL + '/dna/intent/api/v1/global-credential/cli'
    # url = DNAC_URL + '/dna/intent/api/v1/global-credential/snmpv3'
    # url = DNAC_URL + '/dna/intent/api/v1/global-credential/http-write'
    header = {'accept': 'application/json','content-type': 'application/json', 'x-auth-token': dnac_token}
    credential_response = requests.post(url, headers=header, data=json.dumps(credential),verify=False)
    #global_pool = pool_response.json()
    return credential_response.json()


def get_command_output(commands,dnac_token):
    url = DNAC_URL + '/dna/intent/api/v1/network-device-poller/cli/read-request'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    command_response = requests.post(url, headers=header,data=json.dumps(commands),verify=False)

    return command_response.json()


def get_site_topology(dnac_token):
    """
    The function will return site topology
    :param dnac_token: DNA C token
    :return: DNA C site topology info incluing area/building/floor
             name, id, address etc
    """
    url = DNAC_URL + '/dna/intent/api/v1/topology/site-topology'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    site_top = requests.get(url, headers=header,  verify=False)

    return site_top.json()


def get_physic_topology(dnac_token):
    """
    The function will return site topology
    :param dnac_token: DNA C token
    :return: DNA C site topology info including area/building/floor
             name, id, address etc
    """
    url = DNAC_URL + '/dna/intent/api/v1/topology/physical-topology'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    physic_top = requests.get(url, headers=header,  verify=False)
    return physic_top.json()

def get_L2_topology(vlan, dnac_token):
    """
    The function will return layer 2 network topology by specified vlan ID
    :param dnac_token: DNA C token
    :return: DNA C site topology info including area/building/floor
             name, id, address etc
    """
    url = DNAC_URL + '/dna/intent/api/v1/topology/l2/' + vlan
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    l2_topology = requests.get(url, headers=header,  verify=False)

    return l2_topology.json()

def get_nodes_links(data):
    """
    The function will print out node's name, ip address, connected ports and linkstatus
    :param data: topology information
    :return: DNA C site topology info including area/building/floor
             name, id, address etc
    """
    nodes = {}
    for node in data['nodes']:
        nodes[node['id']] = node['label']

    for link in data['links']:
        print('Source: {0}({1}) Target: {2}({3}) Status: {4}'.format(
            nodes[link['source']], link.get('startPortName', ''),
            nodes[link['target']], link.get('endPortName', ''),
            link['linkStatus']
        ))

########  Task
def get_task(task_id, dnac_token):
    url = DNAC_URL + '/dna/intent/api/v1/task/' + task_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.get(url, headers=header, verify=False)
    return response.json()['response']



#######  File
def get_file(file_id, dnac_token):
    url = DNAC_URL + '/dna/intent/api/v1/file/' + file_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.get(url, headers=header, verify=False)
    return response





######  SWIM
def get_swim_id(dnac_token):
    url = DNAC_URL + '/dna/intent/api/v1/image/importation'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_token}
    response = requests.get(url, headers=header, verify=False)
    return response.json()