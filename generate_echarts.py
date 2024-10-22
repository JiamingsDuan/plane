import pandas as pd
from collections import Counter

from function_database import query
from function_kc1 import generate_hex_colors
from function_kc1 import generate_random_coordinates
from function_adjacent2 import find_adjacent_duplicates
from pyecharts import options as opts
from pyecharts.charts import Graph

# parameter
FREQ = 10
TABLE = 'travelsky0726'
hex_chars = '0123456789abcdef'

# Loading the datasets
CheckInData = query(table=TABLE)
CheckInData = CheckInData.fillna('nav')

print('business_id 总量', CheckInData.shape)

# 统计business_id种类数量
counter = dict(Counter(CheckInData.loc[:, 'business_id'].to_list()))
print('amount of business_id', len(counter))

# 初始化坐标
node_coordinates = generate_random_coordinates(len(counter), x1=0, x2=2480, y1=0, y2=1280)
coordinates_index = 0
node_color = generate_hex_colors(len(counter))

# 添加节点
nodes = []
for uid, size in counter.items():
    typing_index = CheckInData[CheckInData['business_id'] == uid].index.to_list()[0]
    # typing_label = CheckInData.loc[typing_index, 'type_id']
    typing_label = 'W'
    if typing_label == 'W':
        nodes.append({'name': uid,
                      'value': size,
                      'x': node_coordinates[coordinates_index][0],
                      'y': node_coordinates[coordinates_index][-1],
                      'symbolSize': pow(size, 0.25),
                      'symbol': 'diamond',
                      'categories': 'class1',
                      'itemStyle': {'normal': {'color': node_color[coordinates_index]}},
                      })
    else:
        nodes.append({'name': uid,
                      'value': size,
                      'x': node_coordinates[coordinates_index][0],
                      'y': node_coordinates[coordinates_index][-1],
                      'symbolSize': pow(size, 0.25),
                      'symbol': 'circle',
                      'categories': 'class2',
                      'itemStyle': {'normal': {'color': node_color[coordinates_index]}}
                      })
    coordinates_index = coordinates_index + 1

# nodes = [
#     {
#         'x': [x0[0] for x0 in node_coordinates],
#         'y': [y0[-1] for y0 in node_coordinates],
#         'id': [uid for uid in list(counter.keys())],
#         'name': [uid for uid in list(counter.keys())],
#         'symbolSize': [size for size in list(counter.values())],
#         'itemStyle': {'normal': {'color': node['color']}},
#     }
#     for node in data['nodes']
# ]


business_ids = CheckInData['business_id'].to_list()
unique_business_ids = find_adjacent_duplicates(business_ids)

relate_tuple_list = [(unique_business_ids[index], unique_business_ids[index + 1])
                     for index in range(len(unique_business_ids) - 1)]

counter_tuple = dict(Counter(relate_tuple_list))
link_color = generate_hex_colors(len(counter_tuple))
color_index = 0

links = []
for link, size in counter_tuple.items():
    # 根据节点属性查找节点
    name1 = link[0]
    name2 = link[-1]
    # print(name1, name2)
    links.append({
        'source': name1,
        'target': name2,
        'value': size,
        'symbolSize': size,
        # 'width': size,
        'lineStyle': {'normal': {'color': link_color[color_index]}},
        'is_disabled_emphasis': True,
    })
    color_index = color_index + 1

graph = (
    Graph()
        .add(series_name='',
             nodes=nodes,
             links=links,
             layout='none',
             is_roam=True,
             is_focusnode=True,
             gravity=0,
             linestyle_opts=opts.LineStyleOpts(curve=0.3, opacity=0.7),
             label_opts=opts.LabelOpts(position='middle'),
             edge_label=opts.LabelOpts(is_show=False, position='middle', formatter='{c}'),
             )
        .set_global_opts(
        title_opts=opts.TitleOpts(title=''),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%"),
    )
)
graph.width = '2560px'
graph.height = '1280px'

# 渲染图表
graph.render('htm/echarts_%s.html' % TABLE)

'''
0808会议待办
1、（无业务的操作图）继续完成可视化路径图（操作数据从开始到结束不间断生成，有方向指向；点与点之间线段按照数量多少展示不同的粗细程度；每个点按照出现的次数多少展示不同的大小；每个节点ID根据读写属性，展示不同的颜色）
2、统计一下每个ID时间间隔的规律，最大值、最小值、均值、中值，画出直方图，看看有没有什么规律，例如同类业务ID之间的操作可能相似
3、（已经业务截取出的路径操作图）每条路径生成的图中，算一下路径在图上的覆盖度，找到尽可能多的在图上能显示的路径，可以评价业务是否集中
4、（已经业务截取出的路径操作图）有了图后，计算两条路径在图上的距离
'''
