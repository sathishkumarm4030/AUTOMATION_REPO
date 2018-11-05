from csit.libraries.VersaLib import VersaLib
import os

if __name__ == "__main__":
    fileDir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))
else:
    fileDir = os.path.dirname(os.path.realpath('__file__'))

#print fileDir
cpe1 = VersaLib('C1_MUM', fileDir + "/Topology/Devices.csv")
cpe1.create_PS_and_DG('Post_staging_template.j2', 'Device_group_template.j2', 'PS_main_template_modify.j2')
