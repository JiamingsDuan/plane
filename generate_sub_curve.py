import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statistics import median
# from pyecharts.charts import Bar, Boxplot, Grid
# from pyecharts import options as opts

# palette
sns.set_style('darkgrid')
plt.rcParams['font.family'] = 'sans-serif'  # Win
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# parameter
FILE = 'HRB_151318-7d_Sheet1'
START = 0
END = 65
STEP = 5
STEP2 = 1


bins = [step for step in range(START, END, STEP)]
labels = ['%d秒~%d秒' % (step, step + STEP) for step in range(START, END - STEP, STEP)]

# load Excel and read sheet
FileName = 'csv/%s.csv' % FILE
# Loading the datasets
CheckInData = pd.read_csv(FileName, dtype={'business_id': str})[['business_id', 'business_time']]
unique_business_id = list(set(CheckInData['business_id'].to_list()))


def slice_data(refer_col, slice_col, ids):
    index_list = CheckInData[CheckInData[refer_col] == ids].index.to_list()
    business_time_list = CheckInData.loc[index_list, slice_col].to_list()
    return {ids: sorted(business_time_list)}


def slice_subtraction_list(lst):
    groups = {}
    for ls in range(len(labels2)):
        groups[labels2[ls]] = len([num for num in lst if bins2[ls] < num <= bins2[ls + 1]])

    return groups


# Business_Time_Distance:mark 'SUB'
subtractions = [0.001, ]
# second index to last index
for index in range(CheckInData.shape[0]):
    if index < CheckInData.shape[0] - 1:
        subtraction = pd.to_datetime(CheckInData.loc[index + 1, 'business_time']) \
                      - pd.to_datetime(CheckInData.loc[index, 'business_time'])
        subtractions.append(round(subtraction.total_seconds() % 60, 3))
    else:
        pass

CheckInData['subtraction'] = subtractions

distribution_frame = pd.DataFrame(columns=['business_id', 'max', 'min', 'mid', 'avg', 'list'])
for uid in unique_business_id:
    subtraction_dict = slice_data('business_id', 'subtraction', uid)
    statistically = {
        'business_id': uid,
        'max': max(subtraction_dict[uid]),
        'min': min(subtraction_dict[uid]),
        'mid': round(median(subtraction_dict[uid]), 3),
        'avg': round(sum(subtraction_dict[uid]) / len(subtraction_dict[uid]), 3),
        'list': subtraction_dict[uid],
        'len': len(subtraction_dict[uid]),
    }
    distribution_frame.loc[distribution_frame.shape[0], :] = statistically

distribution_frame['max_group'] = pd.cut(distribution_frame['max'], bins=bins, labels=labels)
distribution_frame.to_csv('csv/%s_distribute.csv' % FILE, encoding='utf-8', index=False)
for min_max in bins[:-1]:
    MIN = min_max
    MAX = min_max + STEP
    bins2 = [x1 for x1 in range(START, MAX + STEP2, STEP2)]
    labels2 = ['%d秒~%d秒' % (step, step + 1) for step in range(START, MAX, STEP2)]
    cutting_index = distribution_frame[distribution_frame['max_group'] == '%d秒~%d秒' % (MIN, MAX)].index.to_list()
    cutting_frame = distribution_frame.loc[cutting_index, :]

    plt.figure(figsize=(16, 9))
    plt.title('时间间隔最大值在%d秒~%d秒之间' % (MIN, MAX))

    for index2 in cutting_index:
        subtraction_list = cutting_frame.loc[index2, 'list']
        group = slice_subtraction_list(subtraction_list)
        plt.plot(group.keys(), group.values(), label=cutting_frame.loc[index2, 'business_id'])

    plt.xlabel('时间间隔')
    plt.ylabel('频次')
    plt.xticks(rotation=90)
    plt.legend()
    plt.savefig('pdf/10seconds/%s_%d秒~%d秒.pdf' % (FILE, MIN, MAX))
    # plt.show()
