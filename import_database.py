import sqlite3
import pandas as pd
import os
from openpyxl import load_workbook

DIR = 'xls/new/'


# load Excel and read sheet
xls_file_name_lst = os.listdir(DIR)
conn = sqlite3.connect('E:/BaiduNetdiskDownload/database/CheckIndata.db')

for filename in xls_file_name_lst:
    name = filename.split('.')[0]
    print('从Excel抽取 %s......' % filename)
    CheckInData_0 = pd.read_excel(DIR + '%s.xlsx' % name, dtype={'business_id': str})
    print('写入sqlite数据库 %s.sql......' % name)
    CheckInData_0.to_sql(name='travelsky_with_type',
                         con=conn,
                         if_exists='append',
                         index=False)

conn.close()
