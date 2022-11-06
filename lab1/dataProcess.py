import pandas as pd
import csv
# with open('/home/ycwangtch/ssd1/111fall/111fall_data_mining/lab1/IBMGenerator-master/ids_C.data') as infile:

#     # Read space-delimited file and replace all empty spaces by commas
#     data = infile.read().replace(' ', ',')
    
#     # data.to_csv('inputA.csv', sep = ',')
#     # Write the CSV data in the output file
#     print(data, file=open('inputC.csv', 'w'))
# df = pd.read_csv('inputA.csv', sep = 'delimiter', header = None)
# print(df.shape)
# print(df.info())
# df[0]= df[0].astype('|S')
# print(df[0][2].str[5:])
with open('inputA.csv') as csvfile:
    
    for line in csvfile:
        line = line.split(',')
        line = line[3:]
        print(line) 
        

