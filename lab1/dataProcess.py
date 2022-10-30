import pandas as pd

with open('/home/ycwangtch/ssd1/111fall/111fall_data_mining/lab1/IBMGenerator-master/ids_C.data') as infile:

    # Read space-delimited file and replace all empty spaces by commas
    data = infile.read().replace(' ', ',')

    # Write the CSV data in the output file
    print(data, file=open('inputC.csv', 'w'))
