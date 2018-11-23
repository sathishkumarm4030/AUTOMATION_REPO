#!/usr/bin/env python

# from os.path import dirname, realpath, sep, pardir
# import sys
# import os
# print "*" * 20
# # print dirname(realpath(__file__))
# # sys.path.append(dirname(realpath(__file__)))
# # sys.path.append(realpath(__file__))
# sys.path.append(os.getcwd())
# print sys.path
import time
import pandas as pd
from netmiko import redispatch
from netmiko import ConnectHandler
import os
import requests
import sys
from Variables import *
# from csit.libraries.Variables import *
import json
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
import ipaddress
import ipcalc
import itertools as it
from StringIO import StringIO
import re
from datetime import datetime
from CalcIPV4Network import CalcIPv4Network
from robot.api import logger

if __name__ == "__main__":
    fileDir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))
else:
    fileDir = os.path.dirname(os.path.realpath('__file__'))

logger.info(fileDir, also_console=True)

file_loader = FileSystemLoader(fileDir + '/csit/libraries/J2_temps')
if __name__ == "__main__":
    file_loader = FileSystemLoader('./J2_temps')
env = Environment(loader=file_loader)


class LinuxLib:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, device_name, topofile):
        logger.info('intializing', also_console=True)
        csv_data_read = pd.read_csv(topofile, dtype=object)
        self.device_name = device_name
        self.data = csv_data_read.loc[csv_data_read['DUTs'] == device_name]
        self.csv_dict = self.data.set_index('DUTs').T.to_dict()
        for k, v in self.csv_dict[self.device_name].iteritems(): exec("self."+ k+'=v')
        self.vlans = []
        self.start_vlan = int(self.start_vlan)
        # for vlan in range(self.start_vlan'], self.start_vlan']+10):
        #     print vlan
        self.data_dict = {}
        for i, k  in self.csv_dict[self.device_name].iteritems():
            self.data_dict[i] = k
        self.set_network_items(self.Start_lan_ip_subnet)
        self.set_peer_network_items(self.peer_Start_lan_ip_subnet)
        if self.device_type == 'versa':
            self.ORG_ID = int(self.ORG_ID)
            self.Site_id = int(self.Site_id)
            self.LCC = int(self.LCC)
            self.vxlan_tvi_interface = self.ORG_ID * 2
            self.esp_tvi_interface = self.ORG_ID * 2 +1
            self.start_vrf_id = self.ORG_ID * 10 + 120
            self.vddata = csv_data_read.loc[csv_data_read['DUTs'] == 'VD1']
            self.vdcsv_dict = self.vddata.set_index('DUTs').T.to_dict()
            self.vddata_dict = {}
            for i, k  in self.vdcsv_dict['VD1'].iteritems():
                self.vddata_dict[i] = k
            self.vdhead = 'https://' + self.vddata_dict['mgmt_ip'] + ':9182'
        # print self.data_dict
        self.data_dict['vlans'] = []
        self.data_dict['start_vlan'] = int(self.data_dict['start_vlan'])
        if self.data_dict['device_type'] == 'versa':
            self.data_dict['ORG_ID'] = int(self.data_dict['ORG_ID'])
            self.data_dict['Site_id'] = int(self.data_dict['Site_id'])
            self.data_dict['LCC'] = int(self.data_dict['LCC'])
            self.data_dict['vxlan_tvi_interface'] = self.data_dict['ORG_ID'] * 2
            self.data_dict['esp_tvi_interface'] = self.data_dict['ORG_ID'] * 2 +1
            self.data_dict['start_vrf_id'] = self.data_dict['ORG_ID'] * 10 + 120
        logger.info("intialized", also_console=True)

    def get_data_dict(self):
        return self.__dict__

    def set_vlan_items(self, start_vlan):
        self.lan_vlan = []
        self.data_dict['lan_vlan'] = []
        self.lan = {}
        vlan_id_genr = (i for i in range(start_vlan, start_vlan + 11))
        for i in range(1, 11):
            self.lan[i] = {}
            lan_value = next(vlan_id_genr)
            self.lan_vlan.append(lan_value)
            self.data_dict['lan_vlan'].append(lan_value)
            self.lan[i]['vlan'] = lan_value
        return

    # def set_vlan_items(self, start_vlan):
    #     self.data_dict['lan_vlan'] = []
    #     vlan_id_genr = (i for i in range(start_vlan, start_vlan+11))
    #     for i in range(1, 11):
    #         nw_addr = next(vlan_id_genr)
    #         self.data_dict['lan_vlan'].append(nw_addr)
    #     return


    def set_network_items(self, start_lan_ip_subnet):
        self.set_vlan_items(self.start_vlan)
        self.data_dict['lan_network'] = {}
        self.data_dict['lan_first_host'] = {}
        self.data_dict['lan_second_host'] = {}
        self.data_dict['lan_netmask'] = {}
        network = CalcIPv4Network(unicode(start_lan_ip_subnet))
        network_address = (network + (i + 1) * network.size() for i in it.count())
        nw_addr = network
        for i in self.lan_vlan:
            self.data_dict['lan_network'][i] = nw_addr
            n = ipaddress.ip_network(nw_addr)
            self.data_dict['lan_first_host'][i] = str(n[1])
            self.data_dict['lan_second_host'][i] = str(n[2])
            self.data_dict['lan_netmask'][i] = str(n.netmask)
            nw_addr = next(network_address)
        network = CalcIPv4Network(unicode(start_lan_ip_subnet))
        network_address = (network + (i + 1) * network.size() for i in it.count())
        nw_addr = network
        for i in range(1, 11):
            self.lan[i]['nw'] = nw_addr
            n = ipaddress.ip_network(nw_addr)
            self.lan[i]['first_host'] = str(n[1])
            self.lan[i]['second_host'] = str(n[2])
            self.lan[i]['netmask'] = str(n.netmask)
            nw_addr = next(network_address)
        return


    # def set_network_items(self, start_lan_ip_subnet):
    #     self.set_vlan_items(self.start_vlan)
    #     self.lan_network = {}
    #     self.lan_first_host = {}
    #     self.lan_second_host = {}
    #     self.lan_netmask = {}
    #     network = CalcIPv4Network(unicode(start_lan_ip_subnet))
    #     network_address = (network + (i + 1) * network.size() for i in it.count())
    #     nw_addr = network
    #     for i in range(1, 11):
    #         self.lan[i]['nw'] = nw_addr
    #         n = ipaddress.ip_network(nw_addr)
    #         self.lan[i]['first_host'] = str(n[1])
    #         self.lan[i]['second_host'] = str(n[2])
    #         self.lan[i]['netmask'] = str(n.netmask)
    #         nw_addr = next(network_address)
    #     return


    def set_peer_network_items(self, start_lan_ip_subnet):
        #self.set_vlan_items(self.start_vlan)
        self.data_dict['peer_lan_network'] = {}
        self.data_dict['peer_lan_first_host'] = {}
        self.data_dict['peer_lan_second_host'] = {}
        self.data_dict['peer_lan_netmask'] = {}
        network = CalcIPv4Network(unicode(start_lan_ip_subnet))
        network_address = (network + (i + 1) * network.size() for i in it.count())
        nw_addr = network
        for i in self.lan_vlan:
            self.data_dict['peer_lan_network'][i] = nw_addr
            n = ipaddress.ip_network(nw_addr)
            self.data_dict['peer_lan_first_host'][i] = str(n[1])
            self.data_dict['peer_lan_second_host'][i] = str(n[2])
            self.data_dict['peer_lan_netmask'][i] = str(n.netmask)
            nw_addr = next(network_address)
        network = CalcIPv4Network(unicode(start_lan_ip_subnet))
        network_address = (network + (i + 1) * network.size() for i in it.count())
        nw_addr = network
        for i in range(1, 11):
            self.lan[i]['peer_nw'] = nw_addr
            n = ipaddress.ip_network(nw_addr)
            self.lan[i]['peer_first_host'] = str(n[1])
            self.lan[i]['peer_second_host'] = str(n[2])
            self.lan[i]['peer_netmask'] = str(n.netmask)
            nw_addr = next(network_address)
        return

    # def set_peer_network_items(self, start_lan_ip_subnet):
    #     self.set_vlan_items(self.start_vlan)
    #     self.peer_lan_network = {}
    #     self.peer_lan_first_host = {}
    #     self.peer_lan_second_host = {}
    #     self.peer_lan_netmask = {}
    #     network = CalcIPv4Network(unicode(start_lan_ip_subnet))
    #     network_address = (network + (i + 1) * network.size() for i in it.count())
    #     nw_addr = network
    #     for i in self.lan_vlan:
    #         self.peer_lan_network[i] = nw_addr
    #         n = ipaddress.ip_network(nw_addr)
    #         self.peer_lan_first_host[i] = str(n[1])
    #         self.peer_lan_second_host[i] = str(n[2])
    #         self.peer_lan_netmask[i] = str(n.netmask)
    #         nw_addr = next(network_address)
    #     return



    def print_args(self):
        # print(self.data_dict)
        # print self.data_dict
        return self.data_dict

    def login(self, **kwargs):
        if 'vd_login' in kwargs and kwargs['vd_login'] == 'yes':
            device_dict = {
                'device_type': 'versa',
                'ip': self.vddata_dict['mgmt_ip'],
                'username': self.vddata_dict['username'],
                'password': self.vddata_dict['password'],
                'port': '22',
            }
        else:
            device_dict = {
                'device_type': self.device_type,
                'ip': self.ESP_IP,
                'username': self.username,
                'password': self.password,
                'port': '22',
            }
        self.nc = ConnectHandler(**device_dict)
        if self.device_type != 'linux':
            self.nc.enable()
        print self.nc
        time.sleep(5)
        print "{}: {}".format(self.nc.device_type, self.nc.find_prompt())
        return self.nc

    def shell_login(self, **kwargs):
        device_dict = {
            'device_type': 'linux',
            'ip': self.mgmt_ip,
            'username': self.username,
            'password': self.password,
            'port': '22',
        }
        self.shell_nc = ConnectHandler(**device_dict)
        print self.shell_nc
        print self.shell_nc.send_command_expect('sudo bash', expect_string='password')
        print self.shell_nc.send_command_expect('versa123', expect_string='#')
        print self.shell_nc.send_command_expect('exit', expect_string='\$')
        # ur = self.shell_nc.send_command_expect('ls -ltr')
        # print ur
        # time.sleep(5)
        print "{}: {}".format(self.shell_nc.device_type, self.shell_nc.find_prompt())
        return self.shell_nc

    def close(self, nc):
        nc.disconnect()
        print str(nc) + " connection closed"

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
        print response

        if response.status_code == '200':
            return 'PASS'
        else:
            print response.content
            return 'FAIL'
            # data = response.json()
            # print data
            # taskid = str(data['output']['result']['task']['task-id'])
            # return taskid

    def rest_operation_ret_task_id(self, url, headers, body=""):
        if body != "":
            json_data = json.loads(body)
        else:
            json_data = ""
        response = requests.post(self.vdhead + url,
                                 auth=(self.vddata_dict['GUIusername'], self.vddata_dict['GUIpassword']),
                                 headers=headers,
                                 json=json_data,
                                 verify=False)

        print response.text
        data = response.json()
        taskid = str(data['TaskResponse']['task-id'])
        return taskid

    def check_task_status(self, taskid):
        response1 = requests.get(self.vdhead + task_url + taskid,
                                 auth=(self.vddata_dict['GUIusername'], self.vddata_dict['GUIpassword']),
                                 headers=headers3,
                                 verify=False)
        data1 = response1.json()
        print data1
        percent_completed = data1['versa-tasks.task']['versa-tasks.percentage-completion']
        task_result = data1['versa-tasks.task']['versa-tasks.task-status']
        print percent_completed
        # if task_result == 'FAILED':
        #     error_info = data1['versa-tasks.errormessages']['versa-tasks.errormessage']['versa-tasks.error-message']
        print "Sleeping for 5 seconds"
        time.sleep(5)
        # return data1['task']['task-status']
        return str(percent_completed)

    def get_task_result(self, taskid):
        response1 = requests.get(self.vdhead + task_url + taskid,
                                 auth=(self.vddata_dict['GUIusername'], self.vddata_dict['GUIpassword']),
                                 headers=headers3,
                                 verify=False)
        print response1.text
        data1 = response1.json()
        task_result = data1['versa-tasks.task']['versa-tasks.task-status']
        if task_result == 'FAILED':
            error_info = data1['versa-tasks.task']['versa-tasks.errormessages']['versa-tasks.errormessage'][
                'versa-tasks.error-message']
            task_result_cons = task_result + " : " + error_info
            task_desc = data1['versa-tasks.task']['versa-tasks.task-description']
            try:
                get_CPE_name = re.search('Upgrade Appliance: (\S+)', task_desc).group(1)
                print get_CPE_name
            except AttributeError as AE:
                print AE
                get_CPE_name = ""
            print get_CPE_name
            return "FAILED : " + str(task_result_cons)
        else:
            # return "PASSED : " + str(task_result)
            return "PASS"

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

    def get_device_info(self):
        # abc.get_operation(template_url+"/"+ PS_template_name, headers3)
        data1 = self.get_operation(appliance_url, headers3)
        self.dev_dict = {}
        self.dev_present = 'false'
        for i in data1['versanms.ApplianceStatusResult']['appliances']:
            if i['name'] == self.Device_name and i['ipAddress'] == self.ESP_IP:
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
                    print "sleeping 10 secs"
                    # time.sleep(10)
                    # self.get_device_info()
        if self.dev_present == 'false':
            print "sleeping 20 secs"
            time.sleep(20)
            self.get_device_info()
        return self.dev_dict

    def create_template(self, template_name):
        template = env.get_template(template_name)
        return template.render(self.data_dict)

    def device_config_commands(self, nc_handler, cmds):
        nc_handler.config_mode(config_command='config private')
        nc_handler.check_config_mode()
        for cmd in cmds.split("\n"):
            print nc_handler.send_command_expect(cmd, expect_string='%', strip_prompt=False, strip_command=False)
        nc_handler.send_command_expect('commit and-quit', expect_string='>', strip_prompt=False, strip_command=False)

    def linux_device_config_commands(self, nc_handler, cmds, expect_string="\$"):
        for cmd in cmds.split("\n"):
            print cmd
            print nc_handler.send_command_expect(cmd, expect_string=expect_string, strip_prompt=False,
                                                 strip_command=False)

    def cpe_onboard_call(self):
        cpe_shell_login = self.shell_login()
        # print cpe_shell_login.send_command_expect('sudo bash', expect_string='password', strip_prompt=False, strip_command=False)
        # print cpe_shell_login.send_command_expect('versa123', expect_string='#')
        # print cpe_shell_login.send_command_expect('exit', expect_string='\$')
        print cpe_shell_login.send_command_expect('vsh allow-cli', expect_string='password:', strip_prompt=False,
                                                  strip_command=False)
        print cpe_shell_login.send_command_expect('versa123', expect_string='CLI now allowed', strip_prompt=False,
                                                  strip_command=False)
        print cpe_shell_login.send_command_expect('cli', expect_string='>', strip_prompt=False, strip_command=False)
        print cpe_shell_login.send_command_expect('request erase running-config', expect_string='yes',
                                                  strip_prompt=False, strip_command=False)
        print cpe_shell_login.send_command_expect('yes', expect_string='\$', strip_prompt=False, strip_command=False)
        op = cpe_shell_login.send_command_expect('vsh status', expect_string='\$', strip_prompt=False,
                                                 strip_command=False)
        while "Stopped" in op or "Netconf traffic yet to be allowed" in op:
            print "process not up. Please wait for it to come up"
            op = cpe_shell_login.send_command_expect('vsh status', expect_string='\$', strip_prompt=False,
                                                     strip_command=False)
            print op
            time.sleep(10)
        print "After breaking while"
        print cpe_shell_login.send_command_expect('vsh status', expect_string='\$')
        print cpe_shell_login.send_command_expect('vsh show-serialnum', expect_string='\$')
        print cpe_shell_login.send_command_expect('vsh set-serialnum ' + self.Serial_Number,
                                                  expect_string='\$')
        print cpe_shell_login.send_command_expect('vsh show-serialnum', expect_string='\$')
        print cpe_shell_login.send_command_expect(self.Staging_command_template, expect_string='\$')
        time.sleep(20)

    def create_PS_and_DG(self, Post_staging_template, Device_group_template, PS_main_template_modify):
        self.ps_template_body = self.create_template(Post_staging_template)
        self.DG_template_body = self.create_template(Device_group_template)
        print self.ps_template_body
        print self.DG_template_body
        self.post_operation(template_url, headers3, self.ps_template_body)
        time.sleep(5)
        assoc_template_url = sfw_template_assc_url + self.PS_TEMPLATE_NAME + "/associations"
        assc_body = '[{"organization":"' + self.ORG_NAME + '","serviceTemplate":"COMMON-SFW-TEMPLATE10"}]'
        print assc_body
        self.post_operation(assoc_template_url, headers3, assc_body)
        time.sleep(5)
        self.post_operation(template_url + "/deploy/" + self.PS_TEMPLATE_NAME + "?verifyDiff=true", headers3,
                            self.ps_template_body)
        time.sleep(5)
        self.get_operation(template_url + "/" + self.PS_TEMPLATE_NAME, headers3)
        self.get_operation(assoc_template_url, headers3)
        time.sleep(5)
        self.Modify_main_template(PS_main_template_modify)
        self.post_operation(device_grp_url, headers3, self.DG_template_body)
        time.sleep(5)

    def Modify_main_template(self, PS_main_template_modify):
        self.ps_main_template_modify = self.create_template(PS_main_template_modify)
        print self.ps_main_template_modify
        self.vdnc = self.login(vd_login='yes')
        self.device_config_commands(self.vdnc, self.ps_main_template_modify)
        self.close(self.vdnc)

    def pre_onboard_work(self, Device_template, Staging_server_config_template, Staging_cpe_config_template):
        self.DEVICE_template_body = self.create_template(Device_template)
        self.Staging_config_template = self.create_template(Staging_server_config_template)
        self.Staging_command_template = self.create_template(Staging_cpe_config_template)
        print self.Staging_command_template
        print self.DEVICE_template_body
        self.post_operation(device_template_url, headers3, self.DEVICE_template_body)
        time.sleep(5)
        task_id = self.rest_operation_ret_task_id(device_template_url + "/deploy/" + self.Device_name,
                                                  headers3)
        time.sleep(5)
        print task_id
        task_state = "0"
        while task_state != "100":
            task_state = self.check_task_status(task_id)
        task_result = self.get_task_result(task_id)
        if task_result == "PASS":
            print "Device deployed"
        else:
            print "Device deployment failed"
            exit()
        get_device_data = self.get_operation(device_template_url + "/" + self.Device_name, headers3)
        print get_device_data
        time.sleep(5)
        self.vdnc = self.login(vd_login='yes')
        self.device_config_commands(self.vdnc, self.Staging_config_template)
        self.close(self.vdnc)

    def VM_pre_op(self):
        self.VM_nc = self.shell_login()
        self.linux_device_config_commands(self.VM_nc, "sudo bash", expect_string=":")
        self.linux_device_config_commands(self.VM_nc, "versa123", expect_string="#")
        self.linux_device_config_commands(self.VM_nc, "exit", expect_string="\$")
        self.linux_device_config_commands(self.VM_nc, "sudo ifconfig " + self.LAN_INTF + " up")
        intf = str(self.LAN_INTF)
        for i in range(1, 11):
            ip = str(self.lan[i]['second_host'])
            gw = str(self.lan[i]['first_host'])
            nmask = str(self.lan[i]['netmask'])
            destination_nw = str(self.lan[i]['peer_nw'])
            vlan = str(self.lan[i]['vlan'])
            self.linux_device_config_commands(self.VM_nc, "sudo vconfig add " + intf + " " + vlan)
            self.linux_device_config_commands(self.VM_nc, "sudo ifconfig " + intf + "." + vlan + " up")
            self.linux_device_config_commands(self.VM_nc,
                                              "sudo ifconfig " + intf + "." + vlan + " " + ip + " netmask " + nmask)
            self.linux_device_config_commands(self.VM_nc,
                                              "sudo ip route add " + destination_nw + " via " + gw + " dev " + intf + "." + vlan)

    def shell_ping(self, dest_ip, count=5, **kwargs):
        cmd = "sudo ping " + str(dest_ip) + " -c " + str(count)
        paramlist = ['count', 'df_bit', 'interface', 'packet_size', 'rapid', 'record-route', 'routing_instance',
                     'source']
        for element in paramlist:
            if element in kwargs.keys():
                cmd = cmd + " " + element.replace('_', '-') + " " + str(kwargs[element])
        print cmd

        output = self.VM_nc.send_command_expect(cmd, strip_prompt=False, strip_command=False)
        print output
        # logger.info(output, also_console=True)
        return str(" 0% packet loss" in output)

    def ping(self, dest_ip, **kwargs):
        cmd = "ping " + str(dest_ip)
        paramlist = ['count', 'df_bit', 'interface', 'packet_size', 'rapid', 'record-route', 'routing_instance',
                     'source']
        for element in paramlist:
            if element in kwargs.keys():
                cmd = cmd + " " + element.replace('_', '-') + " " + str(kwargs[element])
        print cmd
        output = self.shell_nc.send_command_expect(cmd, expect_string=">", strip_prompt=False, strip_command=False)
        print output
        return str(" 0% packet loss" in output)

    def send_commands_and_expect(self, cmds, expect_string="\$"):
        for cmd in cmds.split("\n"):
            print cmd
            output = self.shell_nc.send_command_expect(cmd, expect_string=expect_string, strip_prompt=False,
                                                       strip_command=False)
        logger.info(output, also_console=True)
        return output




def main():
    print datetime.now()
    VM1 = LinuxLib('VM1_MUM', fileDir + "/Topology/Devices.csv")
    VM2 = LinuxLib('VM2_MUM', fileDir + "/Topology/Devices.csv")
    #VM1_data = VM1.get_data_dict()
    #print VM1_data
    VM1.VM_nc = VM1.shell_login()
    VM2.VM_nc = VM2.shell_login()
    VM2.send_commands_and_expect("pkill iperf3 &")
    VM1.VM_pre_op()
    VM2.VM_pre_op()
    print VM1.shell_ping(VM2.lan[1]['first_host'])
    print VM1.shell_ping(VM2.lan[1]['second_host'])
    print VM2.shell_ping(VM1.lan[1]['first_host'])
    print VM2.shell_ping(VM1.lan[1]['second_host'])
    # print VM1.shell_ping(VM2[])
    print datetime.now()


if __name__ == "__main__":
    main()
