# from py2neo import Node
# from py2neo import Graph
# from py2neo import NodeMatcher
# from py2neo import RelationshipMatcher
# from py2neo import Relationship

import pandas as pd
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import Sankey
from function_adjacent2 import find_adjacent_duplicates
from function_label import find_sub_list

# parameter
FILE = 'HRB_151318'
SHEET = 0

CheckInData = pd.read_csv('../csv/20240331_label.csv',
                          encoding='utf-8',
                          dtype={'business_class': str, 'business_id': str})

# 获取-1,0，1基础路径分割区间，切分基础路径
LabelList = CheckInData['business_label'].to_list()
result, result_index = find_sub_list(LabelList)


# 再次出现的元素编号
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


between = []
bar = []
for IndexTuple in result_index[:1]:
    RouteBusinessID = CheckInData.loc[IndexTuple[0]:IndexTuple[-1], 'business_id'].to_list()
    unique_list = find_adjacent_duplicates(RouteBusinessID)
    # unique_list = number_duplicates(filtered_list)
    bar.extend(unique_list)
    relate_tuple_list = [(unique_list[i], unique_list[i + 1]) for i in range(len(unique_list) - 1)]
    between.extend(relate_tuple_list)

# between = [x for i, x in enumerate(between) if between.index(x) == i]

# delete(-1, 1)
new_LINKS = []
for tu in between:
    if (tu[-1], tu[0]) in new_LINKS:
        pass
    else:
        new_LINKS.append(tu)

count = dict(Counter(new_LINKS))


# {"name": "category1"}
NODES = []
for n in range(len(NODES)):
    node = {'name': NODES[n]}
    NODES.append(node)

# {'source': 'category1', 'target': 'category2', 'value': 10}
LINKS = []
for li in range(len(count.keys())):
    link = {'source': new_LINKS[li][0],
            'target': new_LINKS[li][-1],
            'value': count[(new_LINKS[li][0], new_LINKS[li][-1])]}
    if link in LINKS:
        pass
    else:
        LINKS.append(link)

# LINKS = [x for i, x in enumerate(LINKS) if LINKS.index(x) == i]

# Sankey
c = (
    Sankey(init_opts=opts.InitOpts(width="1920px", height="1080px"))
        .add(
        'sankey',
        NODES,
        LINKS,
        linestyle_opt=opts.LineStyleOpts(opacity=0.2, curve=0.5, color='source'),
        label_opts=opts.LabelOpts(position='bottom'),
        # orient='vertical',
    )
        .set_global_opts(title_opts=opts.TitleOpts(title='Sankey-基本示例'))
        .render('htm/business_sankey.html')
)
