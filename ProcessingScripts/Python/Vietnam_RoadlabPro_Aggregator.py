import pandas as pd
import glob
import re
Path = 'C:\Users\charl\Documents\Vietnam\Fieldwork'
file_names_list = glob.glob(Path+'\\roadlab_bin'+'\\*'+'\\*'+'\\*intervals*.csv')
#print len(file_names_list)
#pd.Series(file_names_list).to_csv(Path+'\\list.csv')

dataframes=[]
for files in file_names_list:
    df = pd.DataFrame(pd.read_csv(files))
    df['Input_file'] = str(files)
    dataframes.append(df)
X = pd.concat(dataframes, ignore_index=True)
X['Line_Geometry'] = 'LINESTRING ('+X['start_lon'].map(str)+' '+X['start_lat'].map(str)+', '+X['end_lon'].map(str)+' '+X['end_lat'].map(str)+')'
X['Input_file'] = X['Input_file'].map(str).str.extract(('(bin.*\.csv)'), expand=False)
X['Input_file'] = X['Input_file'].map(str).str.replace('bin', '').str.replace('\.csv', '')
X['VPROMMS_ID'] = X['Input_file'].str.split('\\').str.get(1)
X.to_csv(Path+'\\'+'FOR_JOIN_INTS.csv')

file_names_list2 = glob.glob(Path+'\\roadlab_bin'+'\\*'+'\\*'+'\\*RoadPath'+'*.csv')
dataframes2=[]
for files in file_names_list2:
    df = pd.DataFrame(pd.read_csv(files))
    df['Input_file'] = str(files)
    dataframes2.append(df)
X = pd.concat(dataframes2, ignore_index=True)
X['Point_Geometry'] = 'POINT ('+X['longitude'].map(str)+' '+X['latitude'].map(str)+')'
X['Input_file'] = X['Input_file'].map(str).str.extract(('(bin.*\.csv)'), expand=False)
X['Input_file'] = X['Input_file'].map(str).str.replace('bin', '').str.replace('\.csv', '')
X['VPROMMS_ID'] = X['Input_file'].str.split('\\').str.get(1)
X.to_csv(Path+'\\'+'FOR_JOIN_PATHS.csv')
