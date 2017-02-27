import pandas as pd
import openpyxl.utils as xl
import urllib2, httplib

##Variables##
Path = "C:\Users\charl\Documents\Vietnam\Bridge Data"
File = "Phuc luc phan chia du an Lramp tinh Thanh Hoa"

##Import##
raw = pd.read_excel(Path+'\\'+File+'.xlsx')

df = pd.DataFrame(raw)
print "\n-------GoogleMaps Script-------\n\nWelcome to the GoogleMaps extract script for VBMS.\n"
column_str_maplinks = str(raw_input("Please input the column letter code for the column including the googlemaps links: "))
column_str_pics = str(raw_input("\nPlease input the column letter code for the column containing the links to the picture folders on googledrive: "))
column_str_names = str(raw_input("\nPlease input the column letter code for the column including the bridge names: "))
Colnum_links = xl.cell.column_index_from_string(column_str_maplinks)
Colnum_pics = xl.cell.column_index_from_string(column_str_pics)
Colnum_names = xl.cell.column_index_from_string(column_str_names)
links = pd.Series(df['Unnamed: %d' % (Colnum_links-1)])
pics = pd.Series(df['Unnamed: %d' % (Colnum_pics-1)])
names = pd.Series(df['Unnamed: %d' % (Colnum_names-1)])

longlinks = []
test = int(raw_input('\nIf safe to search for expanded links, 1, if not 0: '))
for link in links:
    if test == 0:
        longlinks.append('test')
    else:
        try:
            fp = urllib2.urlopen(link)
            a = fp.geturl()
            longlinks.append(a)
        except:
            longlinks.append('error')
df['longlinks'] = pd.Series(longlinks)
X = pd.concat([names, pics,links,df['longlinks']],axis =1)
X.columns = ('names','pics','links','longlinks')
a = X['longlinks'].str.extract('([search/][0-9]{2,3}[.][0-9]{5,7}[,][0-9]{2,3}[.][0-9]{5,7})', expand=False)
b = a.str.split('/').str.get(1)
c = b.str.split(',')
X['Lat'] = c.str.get(0)
X['Lon'] = c.str.get(1)

d = X['longlinks'].str.extract('(/@[0-9]{2,3}[.][0-9]{5,7}[,][0-9]{2,3}[.][0-9]{5,7})', expand=False)
e = d.str.split('@').str.get(1)
f = e.str.split(',')
X['Lat1'] = f.str.get(0)
X['Lon1'] = f.str.get(1)

X['Latitude'] = X['Lat'].fillna('') + X['Lat1'].fillna('')
X['Longitude'] = X['Lon'].fillna('') + X['Lon1'].fillna('')
X = X.drop(['Lat', 'Lon', 'Lat1', 'Lon1'], axis = 1)
answer = int(raw_input("Delete 'spare rows' for missing links? 1 = yes, 0 = no:"))
if answer == 1:
    X = X[X.longlinks != 'error']
else:
    pass
X.to_excel(Path+'\\output.xlsx')
