import random
from function_database import query
from pyvis.network import Network
from collections import Counter
from function_adjacent2 import find_adjacent_duplicates


# parameter
TABLE = 'travelsky0726'

# TABLE = 'HUZ_199165_C'
hex_chars = '0123456789abcdef'

# Loading the datasets
CheckInData = query(table=TABLE)
# print(CheckInData.isnull().sum())
CheckInData = CheckInData.fillna('nav')

print('business_id 总量', CheckInData.shape)

# 统计business_id种类数量
counter = dict(Counter(CheckInData['business_id'].to_list()))
print('business_id 唯一数量', len(counter))

# 创建一个Network对象
net = Network(
    # notebook=True,
    # directed=True
)

net.width = 2560
net.height = 1440
net.repulsion(500)
print('创建画布')

# 添加节点
for uid, count in counter.items():
    color = '#' + ''.join(random.choice(hex_chars) for _ in range(6))
    net.add_node(uid, label=uid, color=color, size=round(pow(count, 0.5), 2))
    # typing_index = CheckInData[CheckInData['business_id'] == uid].index.to_list()[0]
    # typing_label = CheckInData.loc[typing_index, 'type_id']
    # if typing_label == 'W':
    #     color_w = '#' + ''.join(random.choice(hex_chars) for _ in range(6))
    #     net.add_node(uid, label=uid, color=color_w, size=pow(counter[uid], 0.5))
    # elif typing_label == 'R':
    #     color_r = '#' + ''.join(random.choice(hex_chars) for _ in range(6))
    #     net.add_node(uid, label=uid, color=color_r, size=pow(counter[uid], 0.5))
    # else:
    #     pass

print('添加节点')

# 寻找关系
business_ids = CheckInData['business_id'].to_list()
unique_business_ids = find_adjacent_duplicates(business_ids)
print('去除重复操作')

relate_tuple_list = [(unique_business_ids[index], unique_business_ids[index + 1])
                     for index in range(len(unique_business_ids) - 1)]
# 统计关系
counter_tuple = dict(Counter(relate_tuple_list))
print('统计关系')


# 生成颜色编码表

for link, size in counter_tuple.items():
    # 根据节点属性查找节点
    name1 = link[0]
    name2 = link[-1]
    color = '#' + ''.join(random.choice(hex_chars) for _ in range(6))
    net.add_edge(name1,
                 name2,
                 value=size,
                 color=color,
                 title=size,
                 width=round(pow(size, 0.5), 2)
                 )

print('添加关系')
net.show('htm/graph_%s.html' % TABLE, notebook=False)
