cpe2_data = {
    'NAME': 'cpe20',
    'MPLS_WAN_INTERFACE' : 'vni-0/1.0',
    'MPLS_WAN_INTERFACE_IP': '172.16.3.21/30',
    'INTERNET_WAN_INTERFACE': 'vni-0/2.0',
    'INTERNET_WAN_INTERFACE_IP': '172.16.2.146/29',
    'LAN1_INTERFACE': 'vni-0/4.31',
    'LAN1_INTERFACE_IP': '192.120.31.1',
    'LAN1_INTERFACE_IP_WITH_MASK' : '192.120.31.1/24',
    'LAN2_INTERFACE': 'vni-0/4.32',
    'LAN2_INTERFACE_IP': '192.120.32.1/24',
    'ORG_NAME': 'TEST-PRAVIN-BLR',
    'BGP_NBR_IP': '10.60.64.2',
    'WC1_VPN_PROFILE': 'NV-WC01-N2-BLR-Profile',
    'WC1_VXLAN_IP': '10.60.0.1',
}

status_up = 'up'
established = 'Established'
zero = '0'
routing_instances = ['LAN1-VRF']
protocols = ['BGP']
indirect = 'Indirect'

cpe1_data = {
    'LAN1_ROUTE': '192.119.31.0/24',
    'LAN1_INTERFACE_IP': '192.119.31.1',
    'LAN1_INTERFACE_IP_WITH_MASK': '192.119.31.1/24',
    'ESP_IP': '10.60.68.36',
}

cmd1 = 'set interfaces vni-0/1 unit 0 enable false'
cmd2 = 'delete interfaces vni-0/1 unit 0 enable false'
cmd3 = 'set interfaces vni-0/2 unit 0 enable false'
cmd4 = 'delete interfaces vni-0/2 unit 0 enable false'