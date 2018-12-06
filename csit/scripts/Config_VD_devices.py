import sys
import os
import pandas as pd
import time
import getpass


if __name__ == "__main__":
    fileDir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))
else:
    fileDir = os.path.dirname(os.path.realpath('__file__'))

print fileDir
Par_Dir = os.path.dirname(fileDir)
print Par_Dir
sys.path.append(Par_Dir)

from csit.libraries.VersaLib import VersaLib

def get_vd_details():
    global cpe_list
    ip = raw_input("Enter Versa Director IP address:\n")
    print "Versa director IP:" + ip
    ldap_user = raw_input("Enter LDAP Username for making SSH connection to VD:\n")
    print "Versa director Username:" + ldap_user
    ldap_passwd = getpass.getpass("Enter LDAP Password:\n")
    # ip = '10.91.116.35'
    # ldap_user = 'admin'
    # ldap_passwd = 'versa123'
    # user = 'Sathish'
    # passwd = 'Jan*1234'
    # cpe_user = 'admin'
    # cpe_passwd = 'versa123'
    # node_user = 'admin'
    # node_passwd = 'versa123'
    return {'mgmt_ip' : ip, 'username' : ldap_user,\
            'password' : ldap_passwd}



def DO_config_in_VD_For_CPEs():
    vd_dict = get_vd_details()
    vd_dict['device_type'] = 'versa_director'
    VD1 = VersaLib('Versa_director', **vd_dict)
    # print VD1.get_data_dict()
    VD1.vdnc = VD1.login()
    # VD1.vdnc = "1234"
    VD1.config_devices_template(VD1.vdnc, fileDir + "/Topology/PROD_CPEs.csv", fileDir + "/libraries/J2_temps/PROD_CONFIG/devices_template_config.j2")
    VD1.close(VD1.vdnc)


DO_config_in_VD_For_CPEs()