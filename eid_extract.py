# 120DT柜台数据业务视角提取路径，并为business_id打上id组的标签
import pandas as pd
import sqlite3
from tqdm import tqdm
from collections import Counter

# parameter
eid_name = '014AO'
table_name = 'travelsky_%s_with_group' % eid_name
connection = sqlite3.connect('E:/BaiduNetdiskDownload/database/CheckIndata.db',
                             detect_types=sqlite3.PARSE_DECLTYPES,
                             check_same_thread=False)
connection.text_factory = str
query = f"SELECT business_id, business_time from travelsky_total where eid = '%s'" % eid_name

print('extract the data......')
CheckInData = pd.read_sql_query(query, con=connection)
