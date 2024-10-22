import pandas as pd
import seaborn as sns
import time
# self define function load
from function_brt import determine_label
from function_kc4 import determine_KC_ID
from function_label import find_sub_list
from collections import Counter
sns.set_style('darkgrid')

start = time.process_time()
# load the data
CheckInData = pd.read_csv('csv/20240331_label.csv')
# print(CheckInData.shape)


# obtain the slice result and slice index result
LabelSeries = CheckInData['business_label']
LabelList = LabelSeries.to_list()
result, result_index = find_sub_list(LabelList)
# print(len(result), len(result_index))

s_list = []
s = 0
for IndexSets in result_index:
    s = s + 1
    startingIndex = IndexSets[0]
    endingIndex = IndexSets[-1]

    BasicBS_RT = CheckInData.iloc[startingIndex: endingIndex + 1, :]
    BasicBS_ID = BasicBS_RT['business_id'].tolist()
    RouteLabel = determine_label(starting=BasicBS_ID[0], ending=BasicBS_ID[-1])
    deter_result = determine_KC_ID(BasicBS_ID, RouteLabel)
    s_list.append(deter_result)
    # print(s, deter_result, BasicBS_ID[0], BasicBS_ID[-1])
    name = str(deter_result) + '{' + str(startingIndex) + '_' + str(endingIndex) + '}_' + 'no.' + str(s)
    BasicBS_RT.to_csv('htm/' + name + '.csv', index=False, encoding='utf-8')

print(Counter(s_list))
end = time.process_time()
print(end - start)
