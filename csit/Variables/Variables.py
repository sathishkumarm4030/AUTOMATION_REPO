import os
import pandas as pd
import getpass

cpe_list = ""

if __name__ == "__main__":
    fileDir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))
else:
    fileDir = os.path.dirname(os.path.realpath('__file__'))

print fileDir


interface_template = os.path.join(fileDir, 'Utils/TEXTFSM/versa_interface_template')
bgp_nbr_template = os.path.join(fileDir, 'Utils/TEXTFSM/versa_bgp_neighbor_org_template')
route_template = os.path.join(fileDir, 'Utils/TEXTFSM/versa_route_template')
show_config_template = os.path.join(fileDir, 'Utils/TEXTFSM/versa_show_config_template')



#Variables
task_url = "/vnms/tasks/task/"
template_url = "/vnms/sdwan/workflow/templates/template"
upgrade_dev_url = "/api/config/nms/actions/packages/upgrade"
appliance_url = '/vnms/appliance/appliance?offset=0&limit=1000'
package_url = '/api/operational/nms/packages/package?select=name;uri'
headers = {'Accept': 'application/vnd.yang.data+json'}
headers2 = {'Accept': 'application/vnd.yang.data+json', 'Content-Type': 'application/vnd.yang.data+json'}
headers3 = {'Accept': 'application/json', 'Content-Type': 'application/json'}


#Commands
cmd1 = 'show interfaces brief | tab | nomore'
cmd2 = 'show bgp neighbor brief | nomore'
cmd3 = 'show route | nomore'
cmd4 = 'show configuration | display set | nomore'

ps_template_body = """
	"versanms.sdwan-template-workflow": {
		"templateName": "PS",
		"templateType": "sdwan-post-staging",
		"controllers": ["NV-WC01-N2-BLR", "NV-WC02-N2-BLR"],
		"providerOrg": {
			"name": "IPC00012",
			"statefulFW": true,
			"nextGenFW": false
		},
		"analyticsCluster": "LogCollectors",
		"deviceFirmfactor": "6",
		"wanInterfaces": [{
			"interfaceName": "vni-0/1",
			"pppoe": false,
			"unitInfo": [{
				"subUnit": 0,
				"vlanId": 0,
				"networkName": "MPLS-WAN",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv6Static": false,
				"ipv6Dhcp": false,
				"allowSSH": false,
				"monitor": {},
				"linkPriority": "",
				"transportDomains": ["MPLS-TD"]
			}]
		}, {
			"interfaceName": "vni-0/2",
			"pppoe": false,
			"unitInfo": [{
				"subUnit": 0,
				"vlanId": 0,
				"networkName": "INT-WAN",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv6Static": false,
				"ipv6Dhcp": false,
				"allowSSH": false,
				"monitor": {},
				"linkPriority": "",
				"transportDomains": ["INTERNET-TD"]
			}]
		}],
		"deviceType": "full-mesh",
		"redundantPair": {
			"enable": false
		},
		"lanInterfaces": [{
			"interfaceName": "vni-0/4",
			"unitInfo": [{
				"subUnit": "{$v_vni-0-4_LAN1_Unit-0__unit}",
				"vlanId": "{$v_vni-0-4_LAN1_Unit-0__vlanId}",
				"networkName": "LAN1",
				"subOrganization": "IPC00012",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ip6Static": false,
				"ipv6Dhcp": false,
				"vrfName": "LAN1-VRF",
				"zoneName": ""
			}]
		}],
		"solutionTier": "standard-sdwan-plus-ngfw",
		"bandwidth": 1000,
		"customParams": [],
		"minimumImageVersion": "16.1R2-S2.2",
		"isAnalyticsEnabled": false,
		"isPrimary": true,
		"diaConfig": {
			"loadBalance": false
		},
		"splitTunnels": [{
			"vrfName": "LAN1-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}],
		"inBoundNats": []
	}
}"""