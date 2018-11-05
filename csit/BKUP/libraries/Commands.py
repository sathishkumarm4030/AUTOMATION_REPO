#!/usr/bin/env python
import time

def get_interface_status(net_connect, intf_name):
    """Get interface status. Return LAN VRF name and subnet"""
    cmd = 'show interfaces brief ' + str(intf_name) + ' | tab'
    print cmd
    output = net_connect.send_command_expect(cmd)
    output_string = str(output)
    print output_string
    output_list = output_string.split("\n")
    intf_dict = {}
    keys = output_list[0].split()
    values = output_list[2].split()
    for i in xrange(len(keys)):
        intf_dict[keys[i]] = values[i]
    return intf_dict


def get_bgp_neighbor(net_connect, org):
    cmd = 'show bgp neighbor org ' + org + " brief | match ^[0-9]+"
    output = net_connect.send_command_expect(cmd)
    output_string = str(output)
    dict1 = {}
    for i in output_string.split("\n"):
        k = i.split()
        dict1[k[0]] = k[1:]
    return dict1


def get_ipsec_sa(net_connect, org, vpn_profile):
    cmd = 'show orgs org-services '+ org + ' ipsec vpn-profile ' + \
          vpn_profile + ' security-associations brief'
    output = net_connect.send_command_expect(cmd)
    output_string = str(output)
    print output_string
    dict1 = {}
    for i in output_string.split("\n"):
        k = i.split()
        dict1[k[0]] = k[1:]
    return dict1


def get_route(net_connect, routing_instance, protocol):
    cmd = "show route routing-instance " + routing_instance
    output = net_connect.send_command(cmd)
    #print  output
    routes = []
    for route in output.split("\n"):
        if protocol in route:
            routes.append(route)
    return routes


def check_route(routes_list, dest_address, next_hop, intf_name):
    """check_route(routes_list, '192.168.111.0/24', '10.60.68.31', 'Indirect')
    """
    for route in routes_list:
        list1 = route.split()
        if '+' + dest_address in list1:
            if next_hop in list1:
                if intf_name in list1:
                    print "-" * 20
                    print route
                    print "-" * 20
                    return True
    return False


def ping(net_connect, dest_ip, **kwargs):
    cmd = "ping " + str(dest_ip)
    paramlist = ['count', 'df_bit', 'interface', 'packet_size', 'rapid', 'record-route', 'routing_instance', 'source']
    for element in paramlist:
        if element in kwargs.keys():
            cmd =  cmd + " " + element.replace('_', '-') + " "+ str(kwargs[element])
    print cmd
    output = net_connect.send_command_expect(cmd)
    print output
    return str(" 0% packet loss" in output)


def config_commands(net_connect, cmd):
    net_connect.config_mode()
    net_connect.check_config_mode()
    net_connect.send_command(cmd)
    net_connect.commit()
    net_connect.exit_config_mode()
    time.sleep(10)
