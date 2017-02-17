import pandas as pd
import glob
path = 'C:\Users\charl\Documents\Vietnam\CVTS data'
file_names_list = glob.glob(path+'\*.xls')
dataframes=[]
for files in file_names_list:
    df = pd.DataFrame(pd.read_excel(files))
    dataframes.append(df)
newframe = pd.concat(dataframes, ignore_index=True)
print '---Describe Output---\n', newframe.dtypes, '\n', newframe.describe(), '\n---end---'
newframe.to_csv(path+'\output.csv')
