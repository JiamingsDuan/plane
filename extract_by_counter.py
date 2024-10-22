# 120DT柜台数据业务视角提取路径
import sqlite3
import pandas as pd
from tqdm import tqdm
from collections import Counter
from function_adjacent2 import find_adjacent_duplicates
from function_brt import determine_label
from function_label import find_segments


COUNTER = '120DT'

connection = sqlite3.connect('E:/BaiduNetdiskDownload/database/CheckIndata.db')

query = f"SELECT business_id, business_time from travelsky_total where eid = '120DT'"

print('extract the data')
CheckInData = pd.read_sql_query(query, con=connection).head(300000)
# print(CheckInData.isnull().sum())
counter = dict(Counter(CheckInData['business_id']))

# initialize the starting node and ending node
start_list = ['042E0102', '042E0105', '042E0115',
              '042E0200', '042E0201', '042E0211',
              '042E0212', '042E0219', '162R0300',
              '16200100', '16200101', '16240100', '162R0101']
end_list = ['042E0117', '042E0223', '01010915',
            '01010916', '01010917', '01010903',
            '042E0224', '01010600', 'nav']

print('marker the business_id label')
label_list = []
for index in range(CheckInData.shape[0]):

    Record = CheckInData.loc[index, 'business_id']
    if index == 0:
        label_list.append('0')
    else:
        Record_Last = CheckInData.loc[index - 1, 'business_id']
        if Record in start_list:
            label_list.append('1')
            # Record['business_label'] = 1

        elif Record in end_list:
            label_list.append('-1')
            # Record['business_label'] = -1

        elif Record == '042E0200' and CheckInData.iloc[index + 1, 'business_id'] == '042E0112':
            label_list.append('1')
            # Record['business_label'] = 1

        elif Record == '042E0224' and Record_Last == '042E0200':
            label_list.append('-1')
            # Record['business_label'] = -1

        elif Record == '042E0200' and CheckInData.loc[index + 1, 'business_id'] != '042E0112' \
                and CheckInData.loc[index + 1, 'business_id'] != '042E0224':
            label_list.append('1')
            # Record['business_label'] = 1
        else:
            label_list.append('0')
            # Record['business_label'] = 0


# slice the data and obtain the route label save into the LabelList
print('slice the basic route')
CheckInData['business_label'] = label_list
ls = CheckInData['business_label'].to_list()
result_index = find_segments(ls)

print('new a new dataframe')
frame = pd.DataFrame(columns=counter.keys())
frame.insert(0, '路径标签', ['total'])
frame.loc[0, :] = counter
frame.loc[0, '路径标签'] = '总计'


print('write into frame')
for IndexSets in tqdm(result_index):
    # print(IndexSets)
    startingNode = IndexSets[0]
    endingNode = IndexSets[-1]
    startingBusinessID = CheckInData.loc[startingNode, 'business_id']
    endingBusinessID = CheckInData.loc[endingNode, 'business_id']
    RouteLabel = determine_label(starting=startingBusinessID, ending=endingBusinessID)
    Route = CheckInData.loc[startingNode: endingNode, 'business_id'].to_list()
    Route = find_adjacent_duplicates(Route)
    route_counter = dict(Counter(Route))
    route_counter['路径标签'] = RouteLabel
    frame.loc[frame.shape[0], :] = route_counter


print('save frame to the excel')
frame.to_excel('xls/s1.xlsx', index=True)
