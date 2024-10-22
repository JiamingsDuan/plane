import pandas as pd
import matplotlib.pyplot as plt
from function_label import find_sub_list
from function_brt import determine_label

# load the data
CheckInData = pd.read_csv('csv/20240331_class.csv',
                          encoding='utf-8',
                          dtype={'business_class': str, 'business_id': str})

CheckInData['business_id_num'] = ''


# 利用字典推导式讲一个列表去重后再进行枚举形成一个新的字典
def unique_and_index(lst):
    # 使用集合去重
    unique_lst = list(set(lst))
    # 按原顺序重新排序
    unique_lst.sort(key=lst.index)
    # 创建一个字典，将索引作为键，字符串作为值
    result_dict = {item: i for i, item in enumerate(unique_lst)}
    return result_dict


# 获取business_id的原始数据讲其整理成字典形式，用数字编码替换原始id字符集
# unique_dict = unique_and_index(CheckInData['business_id'].to_list())

# 遍历全部id字符集，讲id按照字典的k\v对应关系重新用数字替换
# for index in range(CheckInData.shape[0]):
#     for k, v in unique_dict.items():
#         if str(CheckInData.loc[index, 'business_id']) == k:
#             CheckInData.loc[index, 'business_id'] = unique_dict[k]
#         else:
#             pass

# 获取-1,0，1基础路径分割区间，切分基础路径
LabelList = CheckInData['business_label'].to_list()
result, result_index = find_sub_list(LabelList)

# 重新生成新的数据表
frame = pd.DataFrame(columns=['IDClass'])
LengthList = []

plt.figure(figsize=(18, 12))
for IndexTuple in result_index:
    RouteBusinessClass = CheckInData.loc[IndexTuple[0]:IndexTuple[-1], 'class_name'].to_list()
    RouteBusinessID = CheckInData.loc[IndexTuple[0]:IndexTuple[-1], 'business_id'].to_list()

    # 按id划分纵轴
    # filtered_list1 = [RouteBusinessID[i] for i in range(len(RouteBusinessID)) if
    #                   i == 0 or RouteBusinessID[i] != RouteBusinessID[i - 1]]
    # if len(filtered_list1) < 30 and filtered_list1[0] == '042E0115':
    #     filtered_dict1 = {i: item for i, item in enumerate(filtered_list1)}
    #     plt.plot(filtered_dict1.values())
    # else:
    #     pass

    # 按id组划分纵轴
    filtered_list1 = [RouteBusinessClass[i] for i in range(len(RouteBusinessClass)) if
                      i == 0 or RouteBusinessClass[i] != RouteBusinessClass[i - 1]]
    # if len(filtered_list1) < 30 and filtered_list1[0] == '02':
    if len(filtered_list1) < 30:
        filtered__dict = {i: item for i, item in enumerate(filtered_list1)}
        plt.plot(filtered__dict.values())

plt.grid()
plt.show()
# # CheckInData.to_csv('./csv/' + 'test.csv', index=False, encoding='utf-8')
# frame.to_excel('./xls/test.xlsx', index=False, encoding='utf-8')
# print(max(LengthList))
