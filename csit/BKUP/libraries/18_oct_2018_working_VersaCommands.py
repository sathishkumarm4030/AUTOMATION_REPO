#!/usr/bin/env python

import time
import pandas as pd
from netmiko import redispatch
from netmiko import ConnectHandler
import os
import requests
import sys
from Variables import *
import json

if __name__ == "__main__":
    fileDir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))
else:
    fileDir = os.path.dirname(os.path.realpath('__file__'))

# variables_path =  fileDir + "/Variables/"
#
# print variables_path
# sys.path.insert(0, variables_path)
# import Variables


class VersaCommands:
    def __init__(self, device_name, topofile):
        csv_data_read = pd.read_csv(topofile)
        self.device_name = device_name
        self.data = csv_data_read.loc[csv_data_read['DUTs'] == device_name]
        self.csv_dict = self.data.set_index('DUTs').T.to_dict()
        self.data_dict = {}
        for i, k  in self.csv_dict[self.device_name].iteritems():
            # print i
            # print k
            self.data_dict[i] = k
        # print self.data_dict
        self.vddata = csv_data_read.loc[csv_data_read['DUTs'] == 'VD1']
        self.vdcsv_dict = self.vddata.set_index('DUTs').T.to_dict()
        self.vddata_dict = {}
        for i, k  in self.vdcsv_dict['VD1'].iteritems():
            # print i
            # print k
            self.vddata_dict[i] = k
        # print self.vddata_dict
        self.vdhead = 'https://' + self.vddata_dict['mgmt_ip'] + ':9182'

    def print_args(self):
        # print(self.data_dict)
        # print self.data_dict
        return self.data_dict


    def login(self, **kwargs):
        if 'vd_login' in kwargs and kwargs['vd_login'] == 'yes':
            device_dict= {
                    'device_type': 'versa',
                    'ip': self.vddata_dict['mgmt_ip'],
                    'username': self.vddata_dict['username'],
                    'password': self.vddata_dict['password'],
                    'port': '22',
                }
        else:
            device_dict = {
                'device_type': self.data_dict['device_type'],
                'ip': self.data_dict['esp_ip'],
                'username': self.data_dict['username'],
                'password': self.data_dict['password'],
                'port': '22',
            }
        self.nc = ConnectHandler(**device_dict)
        if self.data_dict['device_type'] != 'linux':
            self.nc.enable()
        print self.nc
        time.sleep(5)
        print "{}: {}".format(self.nc.device_type, self.nc.find_prompt())
        return self.nc

    def shell_login(self, **kwargs):
        device_dict = {
            'device_type': 'linux',
            'ip': self.data_dict['mgmt_ip'],
            'username': self.data_dict['username'],
            'password': self.data_dict['password'],
            'port': '22',
        }
        self.nc = ConnectHandler(**device_dict)
        print self.nc
        # ur = self.nc.send_command_expect('ls -ltr')
        # print ur
        time.sleep(5)
        print "{}: {}".format(self.nc.device_type, self.nc.find_prompt())
        return self.nc


    def close(self):
        self.nc.disconnect()
        print str(self.nc) + " connection closed"

    def cross_login(self):
        self.cnc = self.login(vd_login='yes')
        self.cnc.write_channel("ssh " + self.data_dict["username"] + "@" + self.data_dict["ip"] + "\n")
        time.sleep(5)
        output = self.cnc.read_channel()
        print(output)
        if 'assword:' in output:
            self.cnc.write_channel(self.data_dict["password"] + "\n")
            time.sleep(5)
            output = self.cnc.read_channel()
            print(output)
        elif 'yes' in output:
            print "am in yes condition"
            self.cnc.write_channel("yes\n")
            time.sleep(5)
            output = self.cnc.read_channel()
            print(output)
            time.sleep(1)
            self.cnc.write_channel(self.data_dict["password"] + "\n")
            time.sleep(5)
            output = self.cnc.read_channel()
            print(output)
        else:
            # cpe_logger.info(output)
            return "VD to CPE " + self.data_dict["ip"] + "ssh Failed."
        # self.cnc.write_channel("cli\n")
        # time.sleep(2)
        # output1 = self.cnc.read_channel()
        # print(output1)
        # time.sleep(2)
        try:
            print("doing redispatch")
            redispatch(self.cnc, device_type='versa')
        except ValueError as Va:
            print(Va)
            print("Not able to get router prompt from CPE" + self.data_dict["ip"] + " CLI. please check")
            return "Redispatch not Success"
        time.sleep(2)
        return self.cnc


    def post_operation(self, url, headers, body=""):
        if body != "":
            json_data = json.loads(body)
        else:
            json_data = ""
        response = requests.post(self.vdhead + url,
                                 auth=(self.vddata_dict['GUIusername'], self.vddata_dict['GUIpassword']),
                                 headers=headers,
                                 json=json_data,
                                 verify=False)
        print response.content

        if response.status_code == '200':
            return 'PASS'
        else:
            # print response.content
            return 'FAIL'
        # data = response.json()
        # print data
        # taskid = str(data['output']['result']['task']['task-id'])
        # return taskid


    def get_operation(self, url, headers):
        response = requests.get(self.vdhead + url,
                                 auth=(self.vddata_dict['GUIusername'], self.vddata_dict['GUIpassword']),
                                 headers=headers,
                                 verify=False)
        print response
        return response.json()

    def delete_operation(self, url, headers):
        response = requests.delete(self.vdhead + url,
                                 auth=(self.vddata_dict['GUIusername'], self.vddata_dict['GUIpassword']),
                                 headers=headers,
                                 verify=False)
        print response
        return response

    def check_vsh_status(self):
        pass

    def get_device_info(self, name):
        #abc.get_operation(template_url+"/"+ PS_template_name, headers3)
        data1 = self.get_operation(appliance_url, headers3)
        self.dev_dict = {}
        self.dev_present = 'false'
        for i in data1['versanms.ApplianceStatusResult']['appliances']:
            if i['name'] == name and i['ipAddress'] == self.data_dict['espip']:
                # print i
                if i['ping-status'] != 'REACHABLE':
                    return "Device Ping failed"
                if i['sync-status'] != 'IN_SYNC':
                    return "Device not in Sync"
                self.dev_present = 'true'
                self.dev_dict['name'] = i['name']
                self.dev_dict['uuid'] = i['uuid']
                self.dev_dict['ipAddress'] = i['ipAddress']
                self.dev_dict['ownerOrg'] = i['ownerOrg']
                self.dev_dict['type'] = i['type']
                self.dev_dict['ping_status'] = i['ping-status']
                self.dev_dict['sync_status'] = i['sync-status']
                try:
                    if i['controllers'] != "":
                        self.dev_dict['controllers'] = i['controllers']
                except KeyError as ke:
                    print "Controller Info NIL"
                    self.dev_present = 'false'
                    break
                self.dev_dict['softwareVersion'] = i['softwareVersion']
                try:
                    if i['Hardware'] != "":
                        self.dev_dict['serialNo'] = i['Hardware']['serialNo']
                        self.dev_dict['model'] = i['Hardware']['model']
                        self.dev_dict['packageName'] = i['Hardware']['packageName']
                except KeyError as ke:
                    print i['name']
                    print "Hardware Info NIL"
                    #self.get_device_info(name)
        if self.dev_present == 'false':
            print "sleeping 200 secs"
            time.sleep(20)
            self.get_device_info(name)
        return self.dev_dict


def  main():
    abc = VersaCommands('C1', fileDir + "/Topology/Devices.csv")
    # print abc.print_args()
    # abc.cross_login()
    # abc.close()
    #post_operation(self, url, headers, json_data)
    # print template_url
    # print ps_template_body
    # json_data = json.loads(ps_template_body)
    # print type(json_data)
    # raw_input()
    # abc.post_operation(template_url, headers3, ps_template_body)
    # time.sleep(5)
    # abc.post_operation(template_url+"/deploy/" + PS_template_name + "?verifyDiff=true", headers3, ps_template_body)
    # time.sleep(5)
    # abc.get_operation(template_url+"/"+ PS_template_name, headers3)
    # time.sleep(5)
    # abc.post_operation(device_grp_url, headers3, DG_template_body)
    # time.sleep(5)
    # abc.post_operation(device_template_url, headers3, device_tempalte_body)
    # time.sleep(5)
    # abc.post_operation(device_template_url + "/deploy/" + Device_name, headers3)
    # time.sleep(5)
    # abc.get_operation(device_template_url + "/" + Device_name, headers3)
    # time.sleep(5)
    # abc.delete_operation(device_template_url + "/" + Device_name + "?time=0", headers3)
    # time.sleep(5)
    # abc.delete_operation(template_url + "/" + PS_template_name + "?time=0", headers3)
    # abc.get_operation(template_url+"/"+ PS_template_name, headers3)

    # vdnc = abc.login(vd_login='yes')
    # print vdnc.send_command_expect('dir', expect_string='>')
    # print vdnc.send_command_expect('configure', expect_string='>')
    # print vdnc.send_command_expect('dir', expect_string='>')
    # print vdnc.send_command_expect('dir', expect_string='>')
    # print vdnc.send_command_expect('dir', expect_string='>')


    ##Cpe Login and actions

    cpe_shell_login = abc.shell_login()
    print cpe_shell_login.send_command_expect('sudo bash', expect_string='password')
    print cpe_shell_login.send_command_expect('versa123', expect_string='#')
    print cpe_shell_login.send_command_expect('exit', expect_string='\$')

    print cpe_shell_login.send_command_expect('vsh allow-cli', expect_string='password:')
    print cpe_shell_login.send_command_expect('versa123', expect_string='CLI now allowed')
    print cpe_shell_login.send_command_expect('cli', expect_string = '>')
    print cpe_shell_login.send_command_expect('request erase running-config', expect_string='yes')
    print cpe_shell_login.send_command_expect('yes', expect_string='\$')
    # print cpe_shell_login.send_command_expect('vsh status', expect_string='\$')
    op = cpe_shell_login.send_command_expect('vsh status', expect_string='\$')
    while "Stopped" in op or "Netconf traffic yet to be allowed" in op:
        #print "process not up. Please wait for it to come up"
        op = cpe_shell_login.send_command_expect('vsh status', expect_string='\$')
        print op
        time.sleep(10)
    print "After breaking while"
    print cpe_shell_login.send_command_expect('vsh status', expect_string='\$')

    print cpe_shell_login.send_command_expect('sudo /opt/versa/scripts/staging.py -w 1 -c 10.63.151.90 -s 172.16.3.94/30 -g 172.16.3.93 -l AUTO-CPE26@colt.net  -r NV-WC02-N2-BLR@colt.net -rk NV-WC02-N2-BLR', expect_string = '\$')
    # print cpe_shell_login.send_comm13s-and_expect('sudo /opt/versa/scripts/staging.py --help', expect_string = '\$')
    # op1 = cpe_shell_login.send_command_expect('versa123', expect_string = 'The system is going down for reboot NOW')
    # print op1

    #getdevice_details
    print " device detail on Versa Director"
    print abc.get_device_info("AUTO-CPE26")


if __name__ == "__main__":
    main()
