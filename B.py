import pandas as pd
from A import A
csv_data_read = pd.read_csv('Data.csv')
# print type(csv_data_read)
DUTs_list = csv_data_read['DUTs'].values
# print DUTs_list
# data_dict = {}
i = 'C1'
keyss = csv_data_read.loc[csv_data_read['DUTs'] == i]
# print keyss.to_dict()
# C1 = keyss.set_index('DUTs').T.to_dict()
data_dict =  keyss.set_index('DUTs').T.to_dict()


print data_dict.keys()
print data_dict.values()
print data_dict[i]['ip']
