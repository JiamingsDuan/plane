# 按路径切分组
import pandas as pd
import matplotlib.pyplot as plt
from pyecharts.charts import Bar
from pyecharts import options as opts
from function_label import find_sub_list
from collections import Counter

# parameter
FREQ = 30

# load data
CheckInData = pd.read_csv('csv/20240331_label.csv',
                          encoding='utf-8',
                          dtype={'business_class': str, 'business_id': str})

# 获取-1,0，1基础路径分割区间，切分基础路径
LabelList = CheckInData['business_label'].to_list()
result, result_index = find_sub_list(LabelList)


def number_duplicates(lst):
    seen = {}
    results = []
    for item in lst:
        if item not in seen:
            seen[item] = 1
            results.append(item)
        else:
            seen[item] += 1
            results.append(f'{item}_{seen[item]}')
    return results


nodes = []
relates = []
for IndexTuple in result_index:
    RouteBusinessClass = CheckInData.loc[IndexTuple[0]:IndexTuple[-1], 'business_id'].to_list()
    # RouteBusinessID = CheckInData.loc[IndexTuple[0]:IndexTuple[-1], 'business_id'].to_list()
    # 按Class划分纵轴

    # 去掉相邻相同的元素
    filtered_list = [RouteBusinessClass[i] for i in range(len(RouteBusinessClass)) if
                     i == 0 or RouteBusinessClass[i] != RouteBusinessClass[i - 1]]
    # 为不相邻且相同的元素编号
    ClassList = number_duplicates(filtered_list)
    # print(ClassList)
    # 把去重后的元素无差别再去重
    nodes = list(set([item for sublist in (nodes, ClassList) for item in sublist]))
    # 将路径中相邻两个节点提取出组成二元列表
    relate_tuple_list = [(ClassList[i], ClassList[i + 1]) for i in range(len(ClassList) - 1)]
    relates = [item for sublist in (relates, relate_tuple_list) for item in sublist]

# print(len(nodes), len(relates))
id_counter = dict(Counter(CheckInData['business_id'].to_list()))
link_counter = dict(Counter(relates))


def calculate_percentage(lst, element):
    return (lst.count(element) / len(lst)) * 100


step = range(20, 420, 20)
rates_list = []
for FREQ in step:
    high_freq = []
    for k, v in link_counter.items():
        if v > FREQ:
            high_freq.append(k[0])
            high_freq.append(k[-1])
        else:
            pass

    rates_list.append(round(len(list(set(high_freq))) / len(list(id_counter.keys())), 3))

    # covered_times = []
    # for IndexTuple in result_index:
    #     RouteBusinessClass = CheckInData.loc[IndexTuple[0]:IndexTuple[-1], 'business_id'].to_list()
    #     filtered_list = [RouteBusinessClass[i] for i in range(len(RouteBusinessClass)) if
    #                      i == 0 or RouteBusinessClass[i] != RouteBusinessClass[i - 1]]
    #     # 为不相邻且相同的元素编号
    #     ClassList = number_duplicates(filtered_list)
    #     if set(ClassList).issubset(high_freq):
    #         covered_times.append('True')
    #     else:
    #         covered_times.append('False')
    #
    # rates_list.append(round(calculate_percentage(covered_times, 'True'), 4))

    # print(Counter(covered_times))

bar = Bar()

# 添加数据到柱状图
bar.add_xaxis([str(i) for i in step])
bar.add_yaxis('数据', rates_list)
bar.width = '2560px'
bar.height = '1440px'
# 设置全局配置项
bar.set_global_opts(title_opts=opts.TitleOpts(title='高频连续ID占ID总数（%）'),
                    xaxis_opts=opts.AxisOpts(name='频次', axislabel_opts=opts.LabelOpts(rotate=0)),
                    yaxis_opts=opts.AxisOpts(name='覆盖率'),
                    )

# 渲染图表
bar.render('htm/bar_covered_rate.html')
