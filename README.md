# DNAC_Functions
DNA Center API Basic functions

# Connection to Cisco Always-on Sandbox
One of the sandbox may be offline for maintenance, configuration in them are different.

- DNAC_URL = 'https://sandboxdnac.cisco.com'

  DNAC_USER = 'devnetuser'
  
  DNAC_PASS = 'Cisco123!'

- DNAC_URL = 'https://sandboxdnac2.cisco.com'

  DNAC_USER = 'devnetuser'
  
  DNAC_PASS = 'Cisco123!'

# Usage
Files included:

- config.py - file with the info on how to configure access to devices and applications.
- dnac_func.py - Python modules for DNA Center.


The application "dnac_func.py" will:
##### Authentication
- get access token

##### Network Discovery
- get global credential for the given credential sub type
- add global creadential info

##### Sites
- get site id base on site name
- get building id base on building name
- get site basic information base on side id
- get devices information that associated with a particular site base on site id
- create area, building and floor

##### Devices
- get device id base on device serial number, device name(hostname)
- get all devices info, get device info based on device_id, management interface ip
- get device running configuration
- find if an ip address is configured on device
- assign device to site

##### Template
- get project id and project information base on project name
- get configuration template detail
- get template version
- get unclaimed devices
- create configuration template
- create project
- remove template


##### PnP Onboarding
- get pnp onboarding device detail 
- get the number of devices in certain state from pnp onboarding database

##### Network profile
- create network profile(site profile)
- associate template to network profile
- assign network profile to site

##### SWIM
- get image info


##### Command runner
- get output of any show command from device


##### Path trace
- get path trace info (every device and port info that traffic go through from device A to device B)
- delete path trace

##### Topology
- get physical topology for certain site
- get layer 2 topology for certain site(based on vlan)
