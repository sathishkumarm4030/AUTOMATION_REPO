import pandas as pd

class A(object):
    def __init__(self, arg1):
        csv_data_read = pd.read_csv('Data.csv')
        self.arg1 = arg1
        # dut = csv_data_read.loc[csv_data_read['DUTs'] == arg1]
        self.data = csv_data_read.loc[csv_data_read['DUTs'] == arg1]
        self.data_dict = self.data.set_index('DUTs').T.to_dict()
        # print self.data_dict[self.arg1]['ip']

    def print_args(self):
        # print(self.data_dict)
        print self.data_dict[self.arg1]['ip']
        return "PASS"

def main():
    ABC = A('C1')
    print ABC.print_args()

if __name__ == "__main__":
    main()