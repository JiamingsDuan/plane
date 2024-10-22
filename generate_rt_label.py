"""判别路径标签"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

# self define function load
from function_brt import determine_label
from function_label import find_sub_list

# Chinese
plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False
# palette
sns.set_style('darkgrid')


CheckInData = pd.read_csv('csv/20240331_class.csv')
# print(CheckInData.shape)


# obtain the slice result and slice index result
LabelSeries = CheckInData['business_label']
LabelList = LabelSeries.to_list()
result, result_index = find_sub_list(LabelList)
# print(len(result), len(result_index))


# calculate Inner counts of routes
total = 0
for sonList in result:
    # print(sonList)
    count = len(sonList)
    total = total + count

print('Total business_id total counts:', CheckInData.shape[0])
print('Inner business_id total counts:', total)
print('coverage:', total / CheckInData.shape[0])


# plot the pie figure
pie_label = ['Inner', 'Outer']
data = [total, CheckInData.shape[0] - total]
frame = {
    'label': pie_label,
    'data': data
}

# plt.figure(figsize=(10, 10))
plt.title('coverage of 20240331 dataset is:' + str(total / CheckInData.shape[0]))
plt.pie(x=data, labels=pie_label)
plt.show()


# slice the data and obtain the route label save into the LabelList
LabelList = []
for IndexSets in result_index:
    # print(IndexSets)
    startingNode = IndexSets[0]
    endingNode = IndexSets[-1]
    startingBusinessID = CheckInData.iloc[startingNode, :]['business_id']
    endingBusinessID = CheckInData.iloc[endingNode, :]['business_id']
    # print((startingNode, endingNode), (startingBusinessID, endingBusinessID))
    RouteLabel = determine_label(starting=startingBusinessID, ending=endingBusinessID)
    # print(RouteLabel)
    LabelList.append(RouteLabel)


# counter the LabelList
# print(LabelList)
StatisticalResults = Counter(LabelList)
# print(StatisticalResults)

for rt, ct in dict(StatisticalResults).items():
    print('Route %s count %d' % (rt, ct))

# unzipped the dictionary into the key_list and value_list
RouteLabels = dict(StatisticalResults).keys()
RouteCounts = dict(StatisticalResults).values()

# plot the bar
# plt.figure(figsize=(10, 10))
plt.title('20240331 Counts of Routes')
plt.barh(width=list(RouteCounts), y=list(RouteLabels), height=0.5)
plt.show()
