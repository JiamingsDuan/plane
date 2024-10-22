import sqlite3
import random
import pandas as pd
from collections import Counter
from pyvis.network import Network
from tqdm import tqdm
from function_adjacent2 import find_adjacent_duplicates


# parameter
COUNTER = '120DT'
FREQ = 1
hex_chars = '0123456789abcdef'
connection = sqlite3.connect('E:/BaiduNetdiskDownload/database/CheckIndata.db')
query = f"SELECT business_id, business_time, type, user_id from travelsky_with_type where eid = '120DT'"

print('extract the data')
CheckInData = pd.read_sql_query(query, con=connection).head(300000)
print(CheckInData.isnull().sum())
counter_node = dict(Counter(CheckInData['business_id']))

# 创建一个Network对象
net = Network(
    notebook=False,
    directed=True,
    # select_menu=True
)
# net.show_buttons(filter_=['physics'])

# 添加节点
for uid, count in tqdm(counter_node.items()):
    # net.add_node(uid, label=uid, color='grey', size=pow(count, 0.5))
    typing_index = CheckInData[CheckInData['business_id'] == uid].index.to_list()[0]
    typing_label = CheckInData.loc[typing_index, 'type']
    if typing_label == 'W':
        net.add_node(uid,
                     label=uid,
                     color='#' + ''.join(random.choice(hex_chars) for _ in range(6)),
                     size=pow(count, 0.33))
    elif typing_label == 'R':
        net.add_node(uid,
                     label=uid,
                     color='#' + ''.join(random.choice(hex_chars) for _ in range(6)),
                     size=pow(count, 0.33))
    else:
        net.add_node(uid,
                     label=uid,
                     color='#' + ''.join(random.choice(hex_chars) for _ in range(6)),
                     size=pow(count, 0.33))

business_ids = CheckInData['business_id'].to_list()
unique_business_ids = find_adjacent_duplicates(business_ids)

relate_tuple_list = [(unique_business_ids[index], unique_business_ids[index + 1])
                     for index in range(len(unique_business_ids) - 1)]

counter_tuple = dict(Counter(relate_tuple_list))

for link, size in tqdm(counter_tuple.items()):
    # 根据节点属性查找节点
    name1 = link[0]
    name2 = link[-1]
    if counter_tuple[(name1, name2)] < FREQ:
        pass
    else:
        net.add_edge(name1,
                     name2,
                     value=size,
                     color='#' + ''.join(random.choice(hex_chars) for _ in range(6)),
                     title='%s' % size,
                     )

net.width = 2560
net.height = 1440

# 设置边的宽度与权重成正比
for edge in net.edges:
    edge['width'] = edge['value'] * 0.5

net.repulsion(300)

# 显示图形
net.show('htm/graph_%s.html' % COUNTER, notebook=False)
