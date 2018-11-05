import time
import pandas as pd
from netmiko import ConnectHandler
import os

if __name__ == "__main__":
    fileDir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))
else:
    fileDir = os.path.dirname(os.path.realpath('__file__'))

print fileDir

class VersaCommands:
    def __init__(self, device_name, topofile):
        csv_data_read = pd.read_csv(topofile)
        self.device_name = device_name
        # dut = csv_data_read.loc[csv_data_read['DUTs'] == arg1]
        self.data = csv_data_read.loc[csv_data_read['DUTs'] == device_name]
        self.data_dict = self.data.set_index('DUTs').T.to_dict()
        # print self.data_dict

    def print_args(self):
        # print(self.data_dict)
        # print self.data_dict
        return self.data_dict[self.device_name]


    def make_connection(self, a_device):
        net_connect = ConnectHandler(**a_device)
        net_connect.enable()
        print net_connect
        time.sleep(5)
        print "{}: {}".format(net_connect.device_type, net_connect.find_prompt())
        return net_connect

    def close_connection(self, net_connect):
        net_connect.disconnect()
        print str(net_connect) + " connection closed"


def  main():
    abc = VersaCommands('C1', "Devices.csv")
    print abc.print_args()

if __name__ == "__main__":
    main()