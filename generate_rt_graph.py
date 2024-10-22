# 按路径切分组
import pandas as pd
from py2neo import Graph
from py2neo import Node
from py2neo import Relationship
from py2neo.matching import NodeMatcher, RelationshipMatcher
from function_label import find_sub_list
from collections import Counter

# link and clean the old node
graph = Graph('bolt://localhost:7687', auth=('neo4j', 'duan9595'))
graph.delete_all()
# load the data
CheckInData = pd.read_csv('csv/20240331_digit.csv',
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
    ClassList = [RouteBusinessClass[i] for i in range(len(RouteBusinessClass)) if
                 i == 0 or RouteBusinessClass[i] != RouteBusinessClass[i - 1]]
    # 为不相邻且相同的元素编号
    # ClassList = number_duplicates(filtered_list)
    # print(ClassList)
    # 把去重后的元素无差别再去重
    nodes = list(set([item for sublist in (nodes, ClassList) for item in sublist]))
    # 将路径中相邻两个节点提取出组成二元列表
    relate_tuple_list = [(ClassList[i], ClassList[i + 1]) for i in range(len(ClassList) - 1)]
    relates = [item for sublist in (relates, relate_tuple_list) for item in sublist]

print(len(nodes), len(relates))

# 创建节点
for i in range(len(nodes)):
    node = Node(nodes[i], name=nodes[i])
    graph.create(node)

node_matcher = NodeMatcher(graph)
relationship_matcher = RelationshipMatcher(graph)

# op = relationship_matcher.match('值机接收').where(name='值机接收').first()
# print(op)
time = 1
counter = dict(Counter(relates))
relates = list(set(relates))
print(len(nodes), len(relates))

for i in range(len(relates)):
    # 根据节点属性查找节点
    name1 = relates[i][0]
    name2 = relates[i][-1]
    # print(counter[(name1, name2)])
    node1 = node_matcher.match(name1).where(name=name1).first()
    node2 = node_matcher.match(name2).where(name=name2).first()

    if counter[(name1, name2)] > 20:

        if relationship_matcher.match((node1, node2), r_type=None).exists():
            pass
        else:
            relate = Relationship(node1, str(counter[(name1, name2)]), node2)
            graph.create(relate)
    else:
        pass
