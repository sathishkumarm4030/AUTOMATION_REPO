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
import math
import logging
import logging.handlers
import errno
import csv
currtime = str(datetime.now())
currtime = currtime.replace(" ", "_").replace(":", "_").replace("-", "_").replace(".", "_")




if __name__ == "__main__":
    fileDir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))
else:
    fileDir = os.path.dirname(os.path.realpath('__file__'))

logfile_dir = os.path.dirname(os.path.dirname(os.path.realpath('__file__'))) + "/LOGS/"+ currtime + "/"
if not os.path.exists(os.path.dirname(logfile_dir)):
    try:
        os.mkdir(os.path.dirname(logfile_dir))
    except OSError as exc:  # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

# logger.info(fileDir, also_console=True)

def setup_logger(name, filename, level=logging.DEBUG):
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    formatter1 = logging.Formatter("%(message)s")
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter1)
    logging.getLogger('').addHandler(console)
    log_file = logfile_dir + filename  + ".log"
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger = logging.getLogger(name)
    return logger

def write_result_from_dict(results):
    data_header = ['Device_name', 'Config_Result']
    with open(logfile_dir + 'RESULT.csv', 'w') as file_writer:
        writer = csv.writer(file_writer)
        writer.writerow(data_header)
        for k, v in results.items():
            writer.writerow([k, v])
    print "Result stored in : " + logfile_dir + 'RESULT.csv'

file_loader = FileSystemLoader(fileDir +'/csit/libraries/J2_temps/PROD_CONFIG')
if __name__ == "__main__":
    file_loader = FileSystemLoader('./J2_temps')
env = Environment(loader=file_loader)



class VersaLib:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, device_name, **kwargs):
        if kwargs is not None:
            for k, v in kwargs.iteritems(): exec("self."+ k+'=v')
        if 'topofile' in self.__dict__:
            csv_data_read = pd.read_csv(self.topofile, dtype=object)
            self.device_name = device_name
            data = csv_data_read.loc[csv_data_read['DUTs'] == device_name]
            csv_dict = data.set_index('DUTs').T.to_dict()
            for k, v in csv_dict[self.device_name].iteritems():
                if isinstance(v, float):
                    if math.isnan(v):
                        continue
                exec("self."+ k+'=v')
            # print self.__dict__
            self.vlans = []
            if 'start_vlan' in self.__dict__:
                self.start_vlan = int(self.start_vlan)
                self.set_network_items(self.Start_lan_ip_subnet)
                self.set_peer_network_items(self.peer_Start_lan_ip_subnet)
            if 'ORG_ID' in self.__dict__:
                self.ORG_ID = int(self.ORG_ID)
                self.vxlan_tvi_interface = self.ORG_ID * 2
                self.esp_tvi_interface = self.ORG_ID * 2 +1
                self.start_vrf_id = self.ORG_ID * 10 + 120
                self.ptvi_intf_wc1 = "ptvi" + str(self.ORG_ID * 2)
                self.ptvi_intf_wc2 = "ptvi" + str(self.ORG_ID * 2 + 1)
            if 'Site_id' in self.__dict__:
                self.Site_id = int(self.Site_id)
            if 'LCC' in self.__dict__:
                self.LCC = int(self.LCC)
            print 'LCC' in self.__dict__
            if 'device_type' in self.__dict__:
                if self.device_type == 'versa_director':
                    self.vdhead = 'https://' + self.mgmt_ip + ':9182'
                else:
                    self.vddata = csv_data_read.loc[csv_data_read['device_type'] == 'versa_director']
                    self.vdcsv_dict = self.vddata.set_index('DUTs').T.to_dict()
                    self.vddata_dict = {}
                    for i, k  in self.vdcsv_dict['VD1'].iteritems():
                        self.vddata_dict[i] = k
                    self.vdhead = 'https://' + self.vddata_dict['mgmt_ip'] + ':9182'
        logger.info("intialized", also_console=True)

    def get_data_dict(self):
        return self.__dict__

    def set_vlan_items(self, start_vlan):
        self.lan_vlan = []
        # self.data_dict['lan_vlan'] = []
        self.lan = {}
        vlan_id_genr = (i for i in range(start_vlan, start_vlan+11))
        for i in range(1, 11):
            self.lan[i] = {}
            lan_value = next(vlan_id_genr)
            self.lan_vlan.append(lan_value)
            # self.data_dict['lan_vlan'].append(lan_value)
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
        # self.data_dict['lan_network'] = {}
        # self.data_dict['lan_first_host'] = {}
        # self.data_dict['lan_second_host'] = {}
        # self.data_dict['lan_netmask'] = {}
        # network = CalcIPv4Network(unicode(start_lan_ip_subnet))
        # network_address = (network + (i + 1) * network.size() for i in it.count())
        # nw_addr = network
        # for i in self.lan_vlan:
        #     self.data_dict['lan_network'][i] = nw_addr
        #     n = ipaddress.ip_network(nw_addr)
        #     self.data_dict['lan_first_host'][i] = str(n[1])
        #     self.data_dict['lan_second_host'][i] = str(n[2])
        #     self.data_dict['lan_netmask'][i] = str(n.netmask)
        #     nw_addr = next(network_address)
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
        # self.data_dict['peer_lan_network'] = {}
        # self.data_dict['peer_lan_first_host'] = {}
        # self.data_dict['peer_lan_second_host'] = {}
        # self.data_dict['peer_lan_netmask'] = {}
        # network = CalcIPv4Network(unicode(start_lan_ip_subnet))
        # network_address = (network + (i + 1) * network.size() for i in it.count())
        # nw_addr = network
        # for i in self.lan_vlan:
        #     self.data_dict['peer_lan_network'][i] = nw_addr
        #     n = ipaddress.ip_network(nw_addr)
        #     self.data_dict['peer_lan_first_host'][i] = str(n[1])
        #     self.data_dict['peer_lan_second_host'][i] = str(n[2])
        #     self.data_dict['peer_lan_netmask'][i] = str(n.netmask)
        #     nw_addr = next(network_address)
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
            device_dict= {
                    'device_type': 'versa',
                    'ip': self.vddata_dict['mgmt_ip'],
                    'username': self.vddata_dict['username'],
                    'password': self.vddata_dict['password'],
                    'port': '22',
                }
        elif self.device_type == 'versa_director':
            device_dict= {
                    'device_type': 'versa',
                    'ip': self.mgmt_ip,
                    'username': self.username,
                    'password': self.password,
                    'port': '22',
                }
        else:
            device_dict = {
                'device_type': 'versa',
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
        print self.shell_nc.send_command_expect('exit', expect_string='\$|#')
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
        self.cnc.write_channel("ssh " + self.username + "@" + self.ESP_IP + "\n")
        time.sleep(5)
        output = self.cnc.read_channel()
        print(output)
        if 'assword:' in output:
            self.cnc.write_channel(self.password + "\n")
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
            print("Not able to get router prompt from CPE" + self.ESP_IP + " CLI. please check")
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


    def put_operation(self, url, headers, body=""):
        print body
        if body != "":
            json_data = json.loads(body)
        else:
            json_data = ""
        response = requests.put(self.vdhead + url,
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
            #return "PASSED : " + str(task_result)
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
        #abc.get_operation(template_url+"/"+ PS_template_name, headers3)
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

    def get_interface_data_from_vd(self, interface_name):
        self.vni_interface_url = "/api/config/devices/device/" + self.Device_name + "/config/interfaces/vni/%22" + interface_name + "%22"
        data1 = self.get_operation(self.vni_interface_url, headers3)
        return data1



    def create_template(self, template_name):
        template = env.get_template(template_name)
        return template.render(self.__dict__)

    def device_config_commands(self, nc_handler, cmds):
        nc_handler.config_mode(config_command='config private')
        nc_handler.check_config_mode()
        for cmd in cmds.split("\n"):
            print nc_handler.send_command_expect(cmd, expect_string='%', strip_prompt=False, strip_command=False)
        print nc_handler.send_command_expect('commit and-quit', expect_string='>', strip_prompt=False, strip_command=False)

    def device_config_commands_wo_split(self, nc_handler, cmds):
        # nc_handler.config_mode(config_command='config private')
        # nc_handler.check_config_mode()
        return nc_handler.send_config_set(config_commands=cmds, strip_prompt=False, strip_command=False, \
                                          max_loops=5000, delay_factor=0.0001, exit_config_mode=False)


    def linux_device_config_commands(self, nc_handler, cmds, expect_string="\$"):
        for cmd in cmds.split("\n"):
            print cmd
            print nc_handler.send_command_expect(cmd, expect_string=expect_string, strip_prompt=False, strip_command=False)

    def cpe_onboard_call(self):
        cpe_shell_login = self.shell_login()
        # print cpe_shell_login.send_command_expect('sudo bash', expect_string='password', strip_prompt=False, strip_command=False)
        # print cpe_shell_login.send_command_expect('versa123', expect_string='#')
        # print cpe_shell_login.send_command_expect('exit', expect_string='\$')
        print cpe_shell_login.send_command_expect('vsh allow-cli', expect_string='password:', strip_prompt=False, strip_command=False)
        print cpe_shell_login.send_command_expect('versa123', expect_string='CLI now allowed', strip_prompt=False, strip_command=False)
        print cpe_shell_login.send_command_expect('cli', expect_string='>', strip_prompt=False, strip_command=False)
        print cpe_shell_login.send_command_expect('request erase running-config', expect_string='yes', strip_prompt=False, strip_command=False)
        print cpe_shell_login.send_command_expect('yes', expect_string='\$|#', strip_prompt=False, strip_command=False)
        op = cpe_shell_login.send_command_expect('vsh status', expect_string='\$|#', strip_prompt=False, strip_command=False)
        while "Stopped" in op or "Netconf traffic yet to be allowed" in op:
            print "process not up. Please wait for it to come up"
            op = cpe_shell_login.send_command_expect('vsh status', expect_string='\$|#', strip_prompt=False, strip_command=False)
            print op
            time.sleep(10)
        print "After breaking while"
        print cpe_shell_login.send_command_expect('vsh status', expect_string='\$|#')
        print cpe_shell_login.send_command_expect('vsh show-serialnum', expect_string='\$|#')
        print cpe_shell_login.send_command_expect('vsh set-serialnum ' + self.Serial_Number,
                                                  expect_string='\$|#')
        print cpe_shell_login.send_command_expect('vsh show-serialnum', expect_string='\$|#')
        print cpe_shell_login.send_command_expect(self.Staging_command_template, expect_string='\$|#')
        time.sleep(20)

    def create_PS_and_DG(self, Post_staging_template, Device_group_template, PS_main_template_modify):
        self.ps_template_body = self.create_template(Post_staging_template)
        self.DG_template_body = self.create_template(Device_group_template)
        print self.ps_template_body
        print self.DG_template_body
        self.post_operation(template_url, headers3, self.ps_template_body)
        time.sleep(5)
        assoc_template_url = sfw_template_assc_url + self.PS_TEMPLATE_NAME + "/associations"
        assc_body = '[{"organization":"'+ self.ORG_NAME + '","serviceTemplate":"COMMON-SFW-TEMPLATE10"}]'
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
        for vlan in self.lan_vlan:
            intf = str(self.LAN_INTF)
            ip = str(self.lan_second_host[vlan])
            gw = str(self.lan_first_host[vlan])
            nmask = str(self.lan_netmask[vlan])
            destination_nw = str(self.peer_lan_network[vlan])
            vlan = str(vlan)
            self.linux_device_config_commands(self.VM_nc, "sudo vconfig add " + intf + " " + vlan)
            self.linux_device_config_commands(self.VM_nc, "sudo ifconfig " + intf + "." + vlan + " up")
            self.linux_device_config_commands(self.VM_nc,
                                             "sudo ifconfig " + intf + "." + vlan + " " + ip + " netmask " + nmask)
            self.linux_device_config_commands(self.VM_nc, "sudo ip route add " + destination_nw + " via " + gw +" dev " + intf + "." + vlan)

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

    def ping(self,  dest_ip, **kwargs):
        cmd = "ping " + str(dest_ip)
        paramlist = ['count', 'df_bit', 'interface', 'packet_size', 'rapid', 'record-route', 'routing_instance',
                     'source']
        for element in paramlist:
            if element in kwargs.keys():
                cmd = cmd + " " + element.replace('_', '-') + " " + str(kwargs[element])
        print cmd
        output = self.cnc.send_command_expect(cmd, expect_string=">", strip_prompt=False, strip_command=False)
        print output
        return str(" 0% packet loss" in output)


    def get_interface_status(self, intf_name):
        cmd = "show interfaces brief | tab | match " + str(intf_name)
        output = self.cnc.send_command_expect(cmd, expect_string=">", strip_prompt=False, strip_command=False)
        return output

    def get_bgp_nbr_status(self, nbr_ip):
        cmd = "show bgp neighbor org " + self.ORG_NAME + " brief " + self.ORG_NAME+"-Control-VR | match " + nbr_ip
        output = self.cnc.send_command_expect(cmd, expect_string=">", strip_prompt=False, strip_command=False)
        return output


    def send_commands_and_expect(self, cmds, expect_string=">|%"):
        for cmd in cmds.split("\n"):
            print cmd
            output = self.cnc.send_command_expect(cmd, expect_string=expect_string, strip_prompt=False,
                                                 strip_command=False)
        logger.info(output, also_console=True)
        return output

    def shutdown_interface(self, intf_name):
        data = self.get_interface_data_from_vd(intf_name)
        data['vni']['enable'] = False
        data1 = json.dumps(data)
        self.put_operation(self.vni_interface_url, headers2, data1)

    def unshutdown_interface(self, intf_name):
        data = self.get_interface_data_from_vd(intf_name)
        data['vni']['enable'] = True
        data1 = json.dumps(data)
        self.put_operation(self.vni_interface_url, headers2, data1)

    def config_devices_template(self, nc, device_file, command_template_file):
        start_time = datetime.now()
        main_logger = setup_logger('Versa-director', 'Config_devices_template')
        # print device_file
        # print command_template_file
        curr_file_dir = os.path.dirname(command_template_file)
        curr_file_name = os.path.basename(command_template_file)
        curr_file_loader = FileSystemLoader(curr_file_dir)
        curr_env = Environment(loader=curr_file_loader)
        template = curr_env.get_template(curr_file_name)
        csv_data_read = pd.read_csv(device_file)
        result_dict = {}
        for idx, row in csv_data_read.iterrows():
            dev_dict = row.to_dict()
            if dev_dict['SITE_TYPE'] == 'mpls':
                continue
            # print Solution_type[dev_dict['SITE_TYPE']]
            device_cmds =  template.render(dev_dict, **Solution_type[dev_dict['SITE_TYPE']])
            main_logger.info(device_cmds)
            result = self.device_config_commands_wo_split(nc, device_cmds)
            main_logger.info(result)
            if "syntax error:" in result:
                res_check = "syntax error. please check the command variables in log file"
            else:
                commit_result = nc.send_command_expect("commit", \
                                                       expect_string='%', \
                                                       strip_prompt=False, strip_command=False, max_loops=5000)
                main_logger.info(commit_result)
                if "No modifications to commit." in commit_result:
                    res_check = "No modifications to commit."
                elif "Commit complete." in commit_result:
                    res_check =  "Commit success"
                else:
                    res_check = "commit failed"
            result_dict[dev_dict['DEVICE_NAME']] = res_check
            # main_logger.info(result_dict)
            main_logger.info("CONFIG_RESULT:")
            for k, v in result_dict.iteritems():
                main_logger.info([k , v])
        write_result_from_dict(result_dict)
        main_logger.info("Time elapsed: {}\n".format(datetime.now() - start_time))
        return


def main():
    print datetime.now()
    cpe1 = VersaLib('CPE100_MUM', fileDir + "/Topology/Devices.csv")
    # print cpe1.ESP_IP
    # val =  cpe1.get_data_dict()
    # print val['ORG_NAME']
    cpe1.create_PS_and_DG('Post_staging_template.j2', 'Device_group_template.j2', 'PS_main_template_modify.j2')
    cpe1.pre_onboard_work('Device_template.j2', 'Staging_server_config.j2', 'staging_cpe.j2')
    # cpe1.cpe_onboard_call()
    # cpe1_dev_info_on_vd =  cpe1.get_device_info()
    # print cpe1_dev_info_on_vd
    # cpe1.shutdown_interface(cpe1.MPLS_WAN_INTF)
    # time.sleep(5)
    # print cpe1.get_interface_data_from_vd(cpe1.MPLS_WAN_INTF)
    # time.sleep(20)
    # cpe1.unshutdown_interface(cpe1.MPLS_WAN_INTF)
    # time.sleep(5)
    # print cpe1.get_interface_data_from_vd(cpe1.MPLS_WAN_INTF)
    # cpe1_shell_nc =  cpe1.shell_login()
    # cpe1_vd_nc = cpe1.cross_login()
    # vd_nc = cpe1.login(vd_login='yes')
    # print cpe1_vd_nc
    # print cpe1_shell_nc.send_command_expect("cli", expect_string=">", strip_prompt=False, strip_command=False)
    # result = cpe1.ping(cpe1.data_dict['peer_lan_first_host'][cpe1.data_dict['lan_vlan'][0]], count=4, routing_instance=routing_instances[0], source=cpe1.data_dict['lan_first_host'][cpe1.data_dict['lan_vlan'][0]])
    # print "*" * 20 + "\n" +result
    # result = cpe1.send_commands_and_expect("show interfaces brief | match ptvi33 | tab")
    # print "*" * 20 + "\n" + result
    ##########################################
    # result = cpe1.ping(cpe1.data_dict['peer_lan_first_host'][cpe1.data_dict['lan_vlan'][0]], count=4, routing_instance=routing_instances[0], source=cpe1.data_dict['lan_first_host'][cpe1.data_dict['lan_vlan'][0]])
    # print "*" * 20 + "\n" +result
    # result = cpe1.send_commands_and_expect("show interfaces brief | match ptvi33 | tab")
    # print "*" * 20 + "\n" + result
    # ##############################################
    # cpe2 = VersaLib('C2_MUM', fileDir + "/Topology/Devices.csv")
    # cpe2.pre_onboard_work('Device_template.j2', 'Staging_server_config.j2', 'staging_cpe.j2')
    # cpe2.cpe_onboard_call()
    # cpe2_dev_info_on_vd =  cpe2.get_device_info()
    # print cpe2_dev_info_on_vd
    # VM1 = VersaLib('VM1_MUM', fileDir + "/Topology/Devices.csv")
    # VM2 = VersaLib('VM2_MUM', fileDir + "/Topology/Devices.csv")
    # VM1_data = VM1.get_data_dict()
    # print VM1_data
    # VM1.VM_nc = VM1.shell_login()
    # VM2.VM_nc = VM2.shell_login()
    # VM1.VM_pre_op()
    # VM2.VM_pre_op()
    # print VM1.shell_ping(VM1.data_dict['peer_lan_second_host'][VM1.data_dict['lan_vlan'][0]])
    # print VM2.shell_ping(VM2.data_dict['peer_lan_second_host'][VM2.data_dict['lan_vlan'][0]])
    print datetime.now()


if __name__ == "__main__":
    main()
