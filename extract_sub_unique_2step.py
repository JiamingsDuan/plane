# 分别算滑窗长度为2-19时，每个长度滑窗的最高频词排序
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from tqdm import tqdm


# parameter
TABLE = 'HRB_151318_7d'
STEP = 10
SLICE = 19

connection = sqlite3.connect('E:/BaiduNetdiskDownload/database/CheckIndata.db')
query = f"SELECT business_id, class_name, subtraction from HRB_151318_7d_with_group_unique"

CheckInData = pd.read_sql_query(query, con=connection)

# average_list = []
# for index in range(0, CheckInData.shape[0], STEP):
#     business_time_slice = CheckInData.loc[index:index + 10, 'subtraction'].to_list()
#     average_list.append(round(sum(business_time_slice) / len(business_time_slice), 0))


# sorted_dict = dict(sorted(Counter(average_list).items(), key=lambda item: item[1]))
# for sec, count in sorted_dict.items():
#     print('%d行一组时间间隔平均数：%s; 出现次数：%s' % (STEP, sec, count))

triple_id_group = []
for index in range(0, CheckInData.shape[0]):
    business_id_slice = CheckInData.loc[index:index + SLICE, 'business_id'].to_list()
    # print(business_id_slice)
    triple_id_group.append('->'.join(business_id_slice))

statistic = Counter(triple_id_group)
sorted_dict = dict(sorted(statistic.items(), key=lambda item: item[1]))

operation_counts = {}
for group, count in sorted_dict.items():
    if count > 100:
        operation_counts[group] = count
        print('操作：%s;;次数：%d' % (group, count))

operation_counts_frame = pd.DataFrame(columns=['business_opt%s' % SLICE, 'business_count'])
operation_counts_frame['business_opt%s' % SLICE] = operation_counts.keys()
operation_counts_frame['business_count'] = operation_counts.values()
# operation_counts_frame.to_excel('xls/%s_opt%d_counts.xlsx' % (TABLE, SLICE), index=True)
