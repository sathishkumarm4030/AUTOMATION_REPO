import os
import pandas as pd
import getpass

cpe_list = ""

if __name__ == "__main__":
    fileDir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))
else:
    fileDir = os.path.dirname(os.path.realpath('__file__'))

# print fileDir


interface_template = os.path.join(fileDir, 'Utils/TEXTFSM/versa_interface_template')
bgp_nbr_template = os.path.join(fileDir, 'Utils/TEXTFSM/versa_bgp_neighbor_org_template')
route_template = os.path.join(fileDir, 'Utils/TEXTFSM/versa_route_template')
show_config_template = os.path.join(fileDir, 'Utils/TEXTFSM/versa_show_config_template')



#Variables
device_grp_url = "/nextgen/deviceGroup"
task_url = "/vnms/tasks/task/"
sfw_template_assc_url = "/nextgen/template/"
device_template_url = "/vnms/sdwan/workflow/devices/device"
template_url = "/vnms/sdwan/workflow/templates/template"
upgrade_dev_url = "/api/config/nms/actions/packages/upgrade"
appliance_url = '/vnms/appliance/appliance?offset=0&limit=1000'
package_url = '/api/operational/nms/packages/package?select=name;uri'
headers = {'Accept': 'application/vnd.yang.data+json'}
headers2 = {'Accept': 'application/vnd.yang.data+json', 'Content-Type': 'application/vnd.yang.data+json'}
headers3 = {'Accept': 'application/json', 'Content-Type': 'application/json'}
headers4 = {'Content-Type': 'application/json'}


routing_instances = ['LAN1-VRF', 'LAN2-VRF', 'LAN3-VRF', 'LAN4-VRF', 'LAN5-VRF', 'LAN6-VRF', 'LAN7-VRF', 'LAN8-VRF', 'LAN9-VRF', 'LAN10-VRF']

Solution_type = {
    'internet' : {
        'local_ckt_pri_1_intfs' : "INT-WAN",
        'remote_ckt_pri_1_intf' : "INT-WAN",
        'local_ckt_pri_2_intfs' : "INT-WAN, INT-WAN1, INT-WAN2",
        'remote_ckt_pri_2_intf' : "LTE-WAN",
                  },
    'hybrid' : {
        'local_ckt_pri_1_intfs' : "MPLS-WAN, INT-WAN",
        'remote_ckt_pri_1_intf' : "MPLS-WAN, MPLS-WAN1, MPLS-WAN2, INT-WAN, INT-WAN1, INT-WAN2",
        'local_ckt_pri_2_intfs' : "INT-WAN",
        'remote_ckt_pri_2_intf' : "LTE-WAN",
                  },
    'dual-internet': {
        'local_ckt_pri_1_intfs': "INT-WAN1, INT-WAN2",
        'remote_ckt_pri_1_intf': "INT-WAN, INT-WAN1, INT-WAN2",
        'local_ckt_pri_2_intfs': "INT-WAN1, INT-WAN2",
        'remote_ckt_pri_2_intf': "LTE-WAN",
    },

}




#Commands
cmd1 = 'show interfaces brief | tab | nomore'
cmd2 = 'show bgp neighbor brief | nomore'
cmd3 = 'show route | nomore'
cmd4 = 'show configuration | display set | nomore'

#PS_template_name = 'AUTO-IPC00012-BLR-PS-HS-LIB'

#Device_name = 'AUTO-CPE26'

Main_template_modication = """"""

dg_dict = {
    'dg_name' : ''
}

DG_template_body = """{
	"device-group": {
		"name": {{ dg.dg_name }},
		"dg:organization": {{ dg.org_name }},
		"dg:enable-2factor-auth": false,
		"dg:enable-staging-url": false,
		"dg:poststaging-template": {{ dg.ps_name }}
	}
}"""


ps_template_body = """{
	"versanms.sdwan-template-workflow": {
		"templateName": "AUTO-IPC00012-BLR-PS-HS-LIB",
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
			}, {
				"subUnit": "{$v_vni-0-4_LAN2_Unit-1__unit}",
				"vlanId": "{$v_vni-0-4_LAN2_Unit-1__vlanId}",
				"networkName": "LAN2",
				"subOrganization": "IPC00012",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv4DhcpServer": false,
				"ip6Static": false,
				"ipv6Dhcp": false,
				"vrfName": "LAN2-VRF",
				"zoneName": ""
			}, {
				"subUnit": "{$v_vni-0-4_LAN3_Unit-2__unit}",
				"vlanId": "{$v_vni-0-4_LAN3_Unit-2__vlanId}",
				"networkName": "LAN3",
				"subOrganization": "IPC00012",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv4DhcpServer": false,
				"ip6Static": false,
				"ipv6Dhcp": false,
				"vrfName": "LAN3-VRF",
				"zoneName": ""
			}, {
				"subUnit": "{$v_vni-0-4_LAN4_Unit-3__unit}",
				"vlanId": "{$v_vni-0-4_LAN4_Unit-3__vlanId}",
				"networkName": "LAN4",
				"subOrganization": "IPC00012",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv4DhcpServer": false,
				"ip6Static": false,
				"ipv6Dhcp": false,
				"vrfName": "LAN4-VRF",
				"zoneName": ""
			}, {
				"subUnit": "{$v_vni-0-4_LAN5_Unit-4__unit}",
				"vlanId": "{$v_vni-0-4_LAN5_Unit-4__vlanId}",
				"networkName": "LAN5",
				"subOrganization": "IPC00012",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv4DhcpServer": false,
				"ip6Static": false,
				"ipv6Dhcp": false,
				"vrfName": "LAN5-VRF",
				"zoneName": ""
			}, {
				"subUnit": "{$v_vni-0-4_LAN6_Unit-5__unit}",
				"vlanId": "{$v_vni-0-4_LAN6_Unit-5__vlanId}",
				"networkName": "LAN6",
				"subOrganization": "IPC00012",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv4DhcpServer": false,
				"ip6Static": false,
				"ipv6Dhcp": false,
				"vrfName": "LAN6-VRF",
				"zoneName": ""
			}, {
				"subUnit": "{$v_vni-0-4_LAN7_Unit-6__unit}",
				"vlanId": "{$v_vni-0-4_LAN7_Unit-6__vlanId}",
				"networkName": "LAN7",
				"subOrganization": "IPC00012",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv4DhcpServer": false,
				"ip6Static": false,
				"ipv6Dhcp": false,
				"vrfName": "LAN7-VRF",
				"zoneName": ""
			}, {
				"subUnit": "{$v_vni-0-4_LAN8_Unit-7__unit}",
				"vlanId": "{$v_vni-0-4_LAN8_Unit-7__vlanId}",
				"networkName": "LAN8",
				"subOrganization": "IPC00012",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv4DhcpServer": false,
				"ip6Static": false,
				"ipv6Dhcp": false,
				"vrfName": "LAN8-VRF",
				"zoneName": ""
			}, {
				"subUnit": "{$v_vni-0-4_LAN9_Unit-8__unit}",
				"vlanId": "{$v_vni-0-4_LAN9_Unit-8__vlanId}",
				"networkName": "LAN9",
				"subOrganization": "IPC00012",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv4DhcpServer": false,
				"ip6Static": false,
				"ipv6Dhcp": false,
				"vrfName": "LAN9-VRF",
				"zoneName": ""
			}, {
				"subUnit": "{$v_vni-0-4_LAN10_Unit-9__unit}",
				"vlanId": "{$v_vni-0-4_LAN10_Unit-9__vlanId}",
				"networkName": "LAN10",
				"subOrganization": "IPC00012",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv4DhcpServer": false,
				"ip6Static": false,
				"ipv6Dhcp": false,
				"vrfName": "LAN10-VRF",
				"zoneName": ""
			}]
		}],
		"solutionTier": "standard-sdwan-plus-ngfw",
		"bandwidth": 1000,
		"customParams": [],
		"minimumImageVersion": "16.1R2-S2.2",
		"isAnalyticsEnabled": true,
		"isPrimary": true,
		"diaConfig": {
			"loadBalance": false
		},
		"splitTunnels": [{
			"vrfName": "LAN1-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}, {
			"vrfName": "LAN2-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}, {
			"vrfName": "LAN3-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}, {
			"vrfName": "LAN4-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}, {
			"vrfName": "LAN5-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}, {
			"vrfName": "LAN6-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}, {
			"vrfName": "LAN7-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}, {
			"vrfName": "LAN8-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}, {
			"vrfName": "LAN9-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}, {
			"vrfName": "LAN10-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}],
		"inBoundNats": []
	}
}"""





DG_template_body = """{
	"device-group": {
		"name": "AUTO-IPC00012-BLR-PS-HS-LIB-DG",
		"dg:organization": "IPC00012",
		"dg:enable-2factor-auth": false,
		"dg:enable-staging-url": false,
		"dg:poststaging-template": "AUTO-IPC00012-BLR-PS-HS-LIB"
	}
}"""

ps_template_body = """{
	"versanms.sdwan-template-workflow": {
		"templateName": "AUTO-IPC00012-BLR-PS-HS-LIB",
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
			}, {
				"subUnit": "{$v_vni-0-4_LAN2_Unit-1__unit}",
				"vlanId": "{$v_vni-0-4_LAN2_Unit-1__vlanId}",
				"networkName": "LAN2",
				"subOrganization": "IPC00012",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv4DhcpServer": false,
				"ip6Static": false,
				"ipv6Dhcp": false,
				"vrfName": "LAN2-VRF",
				"zoneName": ""
			}, {
				"subUnit": "{$v_vni-0-4_LAN3_Unit-2__unit}",
				"vlanId": "{$v_vni-0-4_LAN3_Unit-2__vlanId}",
				"networkName": "LAN3",
				"subOrganization": "IPC00012",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv4DhcpServer": false,
				"ip6Static": false,
				"ipv6Dhcp": false,
				"vrfName": "LAN3-VRF",
				"zoneName": ""
			}, {
				"subUnit": "{$v_vni-0-4_LAN4_Unit-3__unit}",
				"vlanId": "{$v_vni-0-4_LAN4_Unit-3__vlanId}",
				"networkName": "LAN4",
				"subOrganization": "IPC00012",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv4DhcpServer": false,
				"ip6Static": false,
				"ipv6Dhcp": false,
				"vrfName": "LAN4-VRF",
				"zoneName": ""
			}, {
				"subUnit": "{$v_vni-0-4_LAN5_Unit-4__unit}",
				"vlanId": "{$v_vni-0-4_LAN5_Unit-4__vlanId}",
				"networkName": "LAN5",
				"subOrganization": "IPC00012",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv4DhcpServer": false,
				"ip6Static": false,
				"ipv6Dhcp": false,
				"vrfName": "LAN5-VRF",
				"zoneName": ""
			}, {
				"subUnit": "{$v_vni-0-4_LAN6_Unit-5__unit}",
				"vlanId": "{$v_vni-0-4_LAN6_Unit-5__vlanId}",
				"networkName": "LAN6",
				"subOrganization": "IPC00012",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv4DhcpServer": false,
				"ip6Static": false,
				"ipv6Dhcp": false,
				"vrfName": "LAN6-VRF",
				"zoneName": ""
			}, {
				"subUnit": "{$v_vni-0-4_LAN7_Unit-6__unit}",
				"vlanId": "{$v_vni-0-4_LAN7_Unit-6__vlanId}",
				"networkName": "LAN7",
				"subOrganization": "IPC00012",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv4DhcpServer": false,
				"ip6Static": false,
				"ipv6Dhcp": false,
				"vrfName": "LAN7-VRF",
				"zoneName": ""
			}, {
				"subUnit": "{$v_vni-0-4_LAN8_Unit-7__unit}",
				"vlanId": "{$v_vni-0-4_LAN8_Unit-7__vlanId}",
				"networkName": "LAN8",
				"subOrganization": "IPC00012",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv4DhcpServer": false,
				"ip6Static": false,
				"ipv6Dhcp": false,
				"vrfName": "LAN8-VRF",
				"zoneName": ""
			}, {
				"subUnit": "{$v_vni-0-4_LAN9_Unit-8__unit}",
				"vlanId": "{$v_vni-0-4_LAN9_Unit-8__vlanId}",
				"networkName": "LAN9",
				"subOrganization": "IPC00012",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv4DhcpServer": false,
				"ip6Static": false,
				"ipv6Dhcp": false,
				"vrfName": "LAN9-VRF",
				"zoneName": ""
			}, {
				"subUnit": "{$v_vni-0-4_LAN10_Unit-9__unit}",
				"vlanId": "{$v_vni-0-4_LAN10_Unit-9__vlanId}",
				"networkName": "LAN10",
				"subOrganization": "IPC00012",
				"ipv4Static": true,
				"ipv4Dhcp": false,
				"ipv4DhcpServer": false,
				"ip6Static": false,
				"ipv6Dhcp": false,
				"vrfName": "LAN10-VRF",
				"zoneName": ""
			}]
		}],
		"solutionTier": "standard-sdwan-plus-ngfw",
		"bandwidth": 1000,
		"customParams": [],
		"minimumImageVersion": "16.1R2-S2.2",
		"isAnalyticsEnabled": true,
		"isPrimary": true,
		"diaConfig": {
			"loadBalance": false
		},
		"splitTunnels": [{
			"vrfName": "LAN1-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}, {
			"vrfName": "LAN2-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}, {
			"vrfName": "LAN3-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}, {
			"vrfName": "LAN4-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}, {
			"vrfName": "LAN5-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}, {
			"vrfName": "LAN6-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}, {
			"vrfName": "LAN7-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}, {
			"vrfName": "LAN8-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}, {
			"vrfName": "LAN9-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}, {
			"vrfName": "LAN10-VRF",
			"wanNetworkName": "INT-WAN",
			"dia": true,
			"gateway": false
		}],
		"inBoundNats": []
	}
}"""


device_tempalte_body = """{
	"versanms.sdwan-device-workflow": {
		"deviceName": "AUTO-CPE26",
		"siteId": "2396",
		"orgName": "IPC00012",
		"serialNumber": "KSA1811006",
		"deviceGroup": "AUTO-IPC00012-BLR-PS-HS-LIB-DG",
		"locationInfo": {
			"state": "karnataka",
			"country": "india",
			"longitude": "77.594563",
			"latitude": "12.971599",
			"city": "bangalore"
		},
		"postStagingTemplateInfo": {
			"templateName": "AUTO-IPC00012-BLR-PS-HS-LIB",
			"templateData": {
				"device-template-variable": {
					"template": "AUTO-IPC00012-BLR-PS-HS-LIB",
					"variable-binding": {
						"attrs": [{
							"name": "{$v_INT-WAN_IPv4__staticaddress}",
							"value": "172.16.3.98/30",
							"isAutogeneratable": false
						}, {
							"name": "{$v_vni-0-4_LAN6_Unit-5__vlanId}",
							"value": "736",
							"isAutogeneratable": false
						}, {
							"name": "{$v_IPC00012-Control-VR_16_Router_ID__vrRouteId}",
							"value": "20.20.16.26",
							"isAutogeneratable": true,
							"isOverwritten": false
						}, {
							"name": "{$v_IPC00012_NV-WC01-N2-BLR_Local_auth_email_key__IKELKey}",
							"value": "1234",
							"isAutogeneratable": true
						}, {
							"name": "{$v_IPC00012_NV-WC02-N2-BLR_Local_auth_email_key__IKELKey}",
							"value": "1234",
							"isAutogeneratable": true
						}, {
							"name": "{$v_LAN10_IPv4__staticaddress}",
							"value": "192.169.240.1/24",
							"isAutogeneratable": false
						}, {
							"name": "{$v_vni-0-4_LAN8_Unit-7__vlanId}",
							"value": "738",
							"isAutogeneratable": false
						}, {
							"name": "{$v_vni-0-4_LAN2_Unit-1__vlanId}",
							"value": "732",
							"isAutogeneratable": false
						}, {
							"name": "{$v_LAN9_IPv4__staticaddress}",
							"value": "192.169.239.1/24",
							"isAutogeneratable": false
						}, {
							"name": "{$v_LAN5_IPv4__staticaddress}",
							"value": "192.169.235.1/24",
							"isAutogeneratable": false
						}, {
							"name": "{$v_LAN1_IPv4__staticaddress}",
							"value": "192.169.231.1/24",
							"isAutogeneratable": false
						}, {
							"name": "{$v_vni-0-4_LAN4_Unit-3__vlanId}",
							"value": "734",
							"isAutogeneratable": false
						}, {
							"name": "{$v_LAN7_IPv4__staticaddress}",
							"value": "192.169.237.1/24",
							"isAutogeneratable": false
						}, {
							"name": "{$v_vni-0-4_LAN4_Unit-3__unit}",
							"value": "734",
							"isAutogeneratable": false
						}, {
							"name": "{$v_IPC00012_NV-WC02-N2-BLR_Local_auth_email_identifier__IKELIdentifier}",
							"value": "AUTO-CPE26@colt.net",
							"isAutogeneratable": true
						}, {
							"name": "{$v_vni-0-4_LAN10_Unit-9__unit}",
							"value": "740",
							"isAutogeneratable": false
						}, {
							"name": "{$v_vni-0-4_LAN9_Unit-8__unit}",
							"value": "739",
							"isAutogeneratable": false
						}, {
							"name": "{$v_vni-0-4_LAN1_Unit-0__unit}",
							"value": "731",
							"isAutogeneratable": false
						}, {
							"name": "{$v_vni-0-4_LAN3_Unit-2__unit}",
							"value": "733",
							"isAutogeneratable": false
						}, {
							"name": "{$v_Site_Id__siteSiteID}",
							"value": "2396",
							"isAutogeneratable": true
						}, {
							"name": "{$v_vni-0-4_LAN6_Unit-5__unit}",
							"value": "736",
							"isAutogeneratable": false
						}, {
							"name": "{$v_vni-0-4_LAN7_Unit-6__vlanId}",
							"value": "737",
							"isAutogeneratable": false
						}, {
							"name": "{$v_LAN6_IPv4__staticaddress}",
							"value": "192.169.236.1/24",
							"isAutogeneratable": false
						}, {
							"name": "{$v_IPC00012_NV-WC01-N2-BLR_Local_auth_email_identifier__IKELIdentifier}",
							"value": "AUTO-CPE26@colt.net",
							"isAutogeneratable": true
						}, {
							"name": "{$v_vni-0-4_LAN1_Unit-0__vlanId}",
							"value": "731",
							"isAutogeneratable": false
						}, {
							"name": "{$v_vni-0-4_LAN9_Unit-8__vlanId}",
							"value": "739",
							"isAutogeneratable": false
						}, {
							"name": "{$v_LAN2_IPv4__staticaddress}",
							"value": "192.169.232.1/24",
							"isAutogeneratable": false
						}, {
							"name": "{$v_vni-0-4_LAN10_Unit-9__vlanId}",
							"value": "740",
							"isAutogeneratable": false
						}, {
							"name": "{$v_vni-0-4_LAN5_Unit-4__unit}",
							"value": "735",
							"isAutogeneratable": false
						}, {
							"name": "{$v_vni-0-4_LAN2_Unit-1__unit}",
							"value": "732",
							"isAutogeneratable": false
						}, {
							"name": "{$v_LAN4_IPv4__staticaddress}",
							"value": "192.169.234.1/24",
							"isAutogeneratable": false
						}, {
							"name": "{$v_IPC00012_Site_Name__sitesSiteName}",
							"value": "AUTO-CPE26",
							"isAutogeneratable": true
						}, {
							"name": "{$v_vni-0-4_LAN3_Unit-2__vlanId}",
							"value": "733",
							"isAutogeneratable": false
						}, {
							"name": "{$v_latitude__IdLatitude}",
							"value": "12.971599",
							"isAutogeneratable": true
						}, {
							"name": "{$v_identification__IdName}",
							"value": "AUTO-CPE26",
							"isAutogeneratable": true
						}, {
							"name": "{$v_LAN3_IPv4__staticaddress}",
							"value": "192.169.233.1/24",
							"isAutogeneratable": false
						}, {
							"name": "{$v_INT-WAN-Transport-VR_IPv4__vrHopAddress}",
							"value": "172.16.3.97",
							"isAutogeneratable": false
						}, {
							"name": "{$v_vni-0-4_LAN7_Unit-6__unit}",
							"value": "737",
							"isAutogeneratable": false
						}, {
							"name": "{$v_tvi-0-32_-_Unit_0_Static_address__tunnelStaticAddress}",
							"value": "10.10.16.26/32",
							"isAutogeneratable": true,
							"isOverwritten": false
						}, {
							"name": "{$v_Chassis_Id__sitesChassisId}",
							"value": "KSA1811006",
							"isAutogeneratable": true
						}, {
							"name": "{$v_longitude__Idlongitude}",
							"value": "77.594563",
							"isAutogeneratable": true
						}, {
							"name": "{$v_LAN8_IPv4__staticaddress}",
							"value": "192.169.238.1/24",
							"isAutogeneratable": false
						}, {
							"name": "{$v_location__IdLocation}",
							"value": "bangalore,karnataka, india",
							"isAutogeneratable": true
						}, {
							"name": "{$v_vni-0-4_LAN5_Unit-4__vlanId}",
							"value": "735",
							"isAutogeneratable": false
						}, {
							"name": "{$v_IPC00012-Control-VR_16_Local_address__vrRouterAddress}",
							"value": "20.20.16.26",
							"isAutogeneratable": true,
							"isOverwritten": false
						}, {
							"name": "{$v_vni-0-4_LAN8_Unit-7__unit}",
							"value": "738",
							"isAutogeneratable": false
						}, {
							"name": "{$v_MPLS-WAN-Transport-VR_IPv4__vrHopAddress}",
							"value": "172.16.3.93",
							"isAutogeneratable": false
						}, {
							"name": "{$v_MPLS-WAN_IPv4__staticaddress}",
							"value": "172.16.3.94/30",
							"isAutogeneratable": false
						}, {
							"name": "{$v_tvi-0-33_-_Unit_0_Static_address__tunnelStaticAddress}",
							"value": "20.20.16.26/32",
							"isAutogeneratable": true,
							"isOverwritten": false
						}]
					}
				},
				"variableMetadata": [{
					"variable": "{$v_INT-WAN_IPv4__staticaddress}",
					"group": "Interfaces",
					"overlay": false,
					"type": "IPV4_MASK"
				}, {
					"variable": "{$v_vni-0-4_LAN6_Unit-5__vlanId}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_IPC00012-Control-VR_16_Router_ID__vrRouteId}",
					"group": "Virtual Routers",
					"overlay": true,
					"type": "IPV4"
				}, {
					"variable": "{$v_IPC00012_NV-WC01-N2-BLR_Local_auth_email_key__IKELKey}",
					"group": "IPSEC",
					"overlay": false
				}, {
					"variable": "{$v_IPC00012_NV-WC02-N2-BLR_Local_auth_email_key__IKELKey}",
					"group": "IPSEC",
					"overlay": false
				}, {
					"variable": "{$v_LAN10_IPv4__staticaddress}",
					"group": "Interfaces",
					"overlay": false,
					"type": "IPV4_MASK"
				}, {
					"variable": "{$v_vni-0-4_LAN8_Unit-7__vlanId}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_vni-0-4_LAN2_Unit-1__vlanId}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_LAN9_IPv4__staticaddress}",
					"group": "Interfaces",
					"overlay": false,
					"type": "IPV4_MASK"
				}, {
					"variable": "{$v_LAN5_IPv4__staticaddress}",
					"group": "Interfaces",
					"overlay": false,
					"type": "IPV4_MASK"
				}, {
					"variable": "{$v_LAN1_IPv4__staticaddress}",
					"group": "Interfaces",
					"overlay": false,
					"type": "IPV4_MASK"
				}, {
					"variable": "{$v_vni-0-4_LAN4_Unit-3__vlanId}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_LAN7_IPv4__staticaddress}",
					"group": "Interfaces",
					"overlay": false,
					"type": "IPV4_MASK"
				}, {
					"variable": "{$v_vni-0-4_LAN4_Unit-3__unit}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_IPC00012_NV-WC02-N2-BLR_Local_auth_email_identifier__IKELIdentifier}",
					"group": "IPSEC",
					"overlay": false
				}, {
					"variable": "{$v_vni-0-4_LAN10_Unit-9__unit}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_vni-0-4_LAN9_Unit-8__unit}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_vni-0-4_LAN1_Unit-0__unit}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_vni-0-4_LAN3_Unit-2__unit}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_Site_Id__siteSiteID}",
					"group": "SDWAN",
					"overlay": false
				}, {
					"variable": "{$v_vni-0-4_LAN6_Unit-5__unit}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_vni-0-4_LAN7_Unit-6__vlanId}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_LAN6_IPv4__staticaddress}",
					"group": "Interfaces",
					"overlay": false,
					"type": "IPV4_MASK"
				}, {
					"variable": "{$v_IPC00012_NV-WC01-N2-BLR_Local_auth_email_identifier__IKELIdentifier}",
					"group": "IPSEC",
					"overlay": false
				}, {
					"variable": "{$v_vni-0-4_LAN1_Unit-0__vlanId}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_vni-0-4_LAN9_Unit-8__vlanId}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_LAN2_IPv4__staticaddress}",
					"group": "Interfaces",
					"overlay": false,
					"type": "IPV4_MASK"
				}, {
					"variable": "{$v_vni-0-4_LAN10_Unit-9__vlanId}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_vni-0-4_LAN5_Unit-4__unit}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_vni-0-4_LAN2_Unit-1__unit}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_LAN4_IPv4__staticaddress}",
					"group": "Interfaces",
					"overlay": false,
					"type": "IPV4_MASK"
				}, {
					"variable": "{$v_IPC00012_Site_Name__sitesSiteName}",
					"group": "SDWAN",
					"overlay": false
				}, {
					"variable": "{$v_vni-0-4_LAN3_Unit-2__vlanId}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_latitude__IdLatitude}",
					"group": "SDWAN",
					"overlay": false
				}, {
					"variable": "{$v_identification__IdName}",
					"group": "SDWAN",
					"overlay": false
				}, {
					"variable": "{$v_LAN3_IPv4__staticaddress}",
					"group": "Interfaces",
					"overlay": false,
					"type": "IPV4_MASK"
				}, {
					"variable": "{$v_INT-WAN-Transport-VR_IPv4__vrHopAddress}",
					"group": "Virtual Routers",
					"overlay": false,
					"type": "IPV4_IPV6"
				}, {
					"variable": "{$v_vni-0-4_LAN7_Unit-6__unit}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_tvi-0-32_-_Unit_0_Static_address__tunnelStaticAddress}",
					"group": "Interfaces",
					"overlay": true,
					"type": "IPV4_IPV6_MASK"
				}, {
					"variable": "{$v_Chassis_Id__sitesChassisId}",
					"group": "SDWAN",
					"overlay": false
				}, {
					"variable": "{$v_longitude__Idlongitude}",
					"group": "SDWAN",
					"overlay": false
				}, {
					"variable": "{$v_LAN8_IPv4__staticaddress}",
					"group": "Interfaces",
					"overlay": false,
					"type": "IPV4_MASK"
				}, {
					"variable": "{$v_location__IdLocation}",
					"group": "SDWAN",
					"overlay": false
				}, {
					"variable": "{$v_vni-0-4_LAN5_Unit-4__vlanId}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_IPC00012-Control-VR_16_Local_address__vrRouterAddress}",
					"group": "Virtual Routers",
					"overlay": true,
					"type": "IPV4"
				}, {
					"variable": "{$v_vni-0-4_LAN8_Unit-7__unit}",
					"group": "Vlan Info",
					"overlay": false,
					"type": "INTEGER"
				}, {
					"variable": "{$v_MPLS-WAN-Transport-VR_IPv4__vrHopAddress}",
					"group": "Virtual Routers",
					"overlay": false,
					"type": "IPV4_IPV6"
				}, {
					"variable": "{$v_MPLS-WAN_IPv4__staticaddress}",
					"group": "Interfaces",
					"overlay": false,
					"type": "IPV4_MASK"
				}, {
					"variable": "{$v_tvi-0-33_-_Unit_0_Static_address__tunnelStaticAddress}",
					"group": "Interfaces",
					"overlay": true,
					"type": "IPV4_IPV6_MASK"
				}]
			}
		}
	}
}"""
