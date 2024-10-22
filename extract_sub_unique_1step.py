# 为HRB_151318_7d数据集打标签，计算时间间隔，去掉相邻两个操作完全一样的重复数据只保留一个
import sqlite3
import pandas as pd
from tqdm import tqdm


# parameter
TABLE = 'HRB_151318_7d'
connection = sqlite3.connect('E:/BaiduNetdiskDownload/database/CheckIndata.db')
query = f"SELECT * from HRB_151318_7d"


print('extract the data')
CheckInData = pd.read_sql_query(query, con=connection)
# checking None
# print(CheckInData.isnull().sum())

print('delete the same business_id')
duplicate_indices = CheckInData[CheckInData['business_id'].shift() == CheckInData['business_id']].index
CheckInData = CheckInData.drop(duplicate_indices).reset_index(drop=True)


print('mark business_class、class_name......')
CheckInData[['business_class', 'class_name']] = ''
query1 = "SELECT class_name, business_id, business_class from BusinessClass1016"
BusinessIdClassData = pd.read_sql_query(query1, con=connection, dtype={'business_id': 'str',
                                                                       'business_class': 'str',
                                                                       })

# Business_Part:mark 'business_class', 'class_name'
for index in tqdm(range(CheckInData.shape[0])):
    business_id = CheckInData.loc[index, 'business_id']
    if business_id in BusinessIdClassData['business_id'].to_list():
        class_index = BusinessIdClassData[BusinessIdClassData['business_id'] == business_id].index[0]
        series = BusinessIdClassData.loc[class_index, ['business_class', 'class_name']]
        CheckInData.loc[index, ['business_class', 'class_name']] = series
    else:
        CheckInData.loc[index, ['business_class', 'class_name']] = None


# Business_Time_Distance:mark 'subtraction' first index is 0
print('calculate the business_time subtraction')
subtractions = [0, ]
# second index to last index
for index in tqdm(range(CheckInData.shape[0])):
    if index < CheckInData.shape[0] - 1:
        subtraction = pd.to_datetime(CheckInData.loc[index + 1, 'business_time']) \
                      - pd.to_datetime(CheckInData.loc[index, 'business_time'])
        subtractions.append(round(subtraction.total_seconds() % 60, 3))
    else:
        pass

CheckInData['subtraction'] = subtractions
CheckInData.to_sql(name=TABLE + '_with_group_unique',
                   con=connection,
                   if_exists='replace',
                   index=False,
                   )

# CheckInData.to_excel('xls/HRB_151318_7d_subtraction.xlsx', index=False)
