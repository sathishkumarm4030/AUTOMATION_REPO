#!/usr/bin/env python

from datetime import datetime
from netmiko import ConnectHandler
import time


def make_connection(a_device):
    net_connect = ConnectHandler(**a_device)
    net_connect.enable()
    print net_connect
    time.sleep(5)
    print "{}: {}".format(net_connect.device_type, net_connect.find_prompt())
    return net_connect

def close_connection(net_connect):
    net_connect.disconnect()
    print str(net_connect) + " connection closed"


def main():
    # device_list = [cpe19]
    start_time = datetime.now()
    # for a_device in device_list:
    #     #print type(a_device)
    #     net_connect = make_connection(a_device)
    #     Commands.ping(net_connect, dest_ip='127.0.0.1', source='127.0.0.1')
    #     close_connection(net_connect)

if __name__ == "__main__":
    main()