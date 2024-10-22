"""有向图"""
import pandas as pd
from function_label import find_sub_list
from function_brt import determine_label

# load the data
CheckInData = pd.read_csv('csv/20240331_class.csv',
                          encoding='utf-8',
                          dtype={'business_class': str, 'business_id': str})

# obtain the slice result and slice index result
LabelList = CheckInData['business_label'].to_list()
result, result_index = find_sub_list(LabelList)

frame = pd.DataFrame(columns=['路径编号', '业务ID', '业务组ID', '业务组名称', '路径编码', '路径时间间隔'])

LabelList = []
TimeIntervalList = []
for IndexTuple in result_index:
    # print(IndexTuple)
    # location Class and ID
    startingNode = IndexTuple[0]
    endingNode = IndexTuple[-1]
    startingBusinessID = CheckInData.iloc[startingNode, :]['business_id']
    endingBusinessID = CheckInData.iloc[endingNode, :]['business_id']
    # print((startingNode, endingNode), (startingBusinessID, endingBusinessID))
    RouteLabel = determine_label(starting=startingBusinessID, ending=endingBusinessID)
    LabelList.append(RouteLabel)
    RouteBusinessClass = CheckInData.loc[IndexTuple[0]:IndexTuple[-1], 'business_class'].to_list()
    RouteBusinessID = CheckInData.loc[IndexTuple[0]:IndexTuple[-1], 'business_id'].to_list()
    RouteBusinessName = CheckInData.loc[IndexTuple[0]:IndexTuple[-1], 'class_name'].to_list()
    subtraction = pd.to_datetime(CheckInData.loc[startingNode, 'business_time']) \
                  - pd.to_datetime(CheckInData.loc[startingNode - 1, 'business_time'])
    spl = round(subtraction.total_seconds() % 60, 4)
    TimeIntervalList.append(spl)
    ClassFrame = '\n'.join(RouteBusinessClass)
    IDFrame = '\n'.join(RouteBusinessID)
    NameFrame = '\n'.join(RouteBusinessName)
    frame.loc[frame.shape[0], :] = [str(frame.shape[0] + 1), IDFrame, ClassFrame, NameFrame, '', '']

frame['路径编码'] = LabelList
frame['路径时间间隔'] = TimeIntervalList
frame.to_excel('./xls/20240331.xlsx', index=False, encoding='utf-8')
