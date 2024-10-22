import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statistics import median
from pyecharts.charts import Bar, Boxplot, Grid
from pyecharts import options as opts

# palette
sns.set_style('darkgrid')
plt.rcParams['font.family'] = 'sans-serif'  # Win
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# parameter
FILE = 'HRB_151318-7d_Sheet1'

# load Excel and read sheet
FileName = 'csv/%s.csv' % FILE

# Loading the datasets
CheckInData = pd.read_csv(FileName, dtype={'business_id': str})[['business_id', 'business_time']]
unique_business_id = list(set(CheckInData['business_id'].to_list()))


def slice_data(refer_col, slice_col, ids):
    index_list = CheckInData[CheckInData[refer_col] == ids].index.to_list()
    business_time_list = CheckInData.loc[index_list, slice_col].to_list()
    return {ids: sorted(business_time_list)}


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
    }
    distribution_frame.loc[distribution_frame.shape[0], :] = statistically

bins = [step for step in range(0, 65, 5)]
labels = ['%d秒~%d秒' % (step, step + 5) for step in range(0, 60, 5)]
distribution_frame['max_group'] = pd.cut(distribution_frame['max'], bins=bins, labels=labels)

distribution_frame.to_excel('./ss.xlsx', index=False, encoding='utf-8')
index_list = distribution_frame[distribution_frame['max_group'] == '%d秒~%d秒' % (0, 5)].index.to_list()
second_frame = distribution_frame.loc[index_list, :]
plt.figure(figsize=(10, 4))
plt.hist(x=second_frame['list'].to_list(),
         label=second_frame['business_id'].to_list(),
         bins=range(0, 7, 1))
plt.title('最大值在%d秒~%d秒' % (0, 5))
plt.xlabel('间隔')
plt.ylabel('数量')
plt.legend()
plt.show()
