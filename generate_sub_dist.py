import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statistics import median
from function_database import query
from pyecharts.charts import Bar, Boxplot, Grid
from pyecharts import options as opts


# palette
sns.set_style('darkgrid')
plt.rcParams['font.family'] = 'sans-serif'  # Win
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


# parameter
TABLE = 'travelsky0726'
# TABLE = 'HUZ_199165_C'
hex_chars = '0123456789abcdef'
# Loading the datasets
CheckInData = query(table=TABLE)
CheckInData = CheckInData.fillna('nav')
print('读取数据。。。。。。')


def slice_data(refer_col, slice_col, ids):
    index_list = CheckInData[CheckInData[refer_col] == ids].index.to_list()
    business_time_list = CheckInData.loc[index_list, slice_col].to_list()
    return sorted(business_time_list)


unique_business_id = list(set(CheckInData['business_id'].to_list()))

# Business_Time_Distance:mark 'SUB'
subtractions = [0, ]
# second index to last index
for index in range(CheckInData.shape[0]):
    if index < CheckInData.shape[0] - 1:
        subtraction = pd.to_datetime(CheckInData.loc[index + 1, 'business_time']) \
                      - pd.to_datetime(CheckInData.loc[index, 'business_time'])
        subtractions.append(round(subtraction.total_seconds() % 60, 3))
        # print(round(subtraction.total_seconds() % 60, 3))
    else:
        pass

CheckInData['subtraction'] = subtractions
print('计算时间间隔。。。。。。')


distribution_frame = pd.DataFrame(columns=['business_id', 'max', 'min', 'mid', 'avg', '25', '75', 'frq'])


for uid in unique_business_id:
    subtraction_lst = slice_data('business_id', 'subtraction', uid)
    statistically = {
        'business_id': uid,
        'max': max(subtraction_lst),
        'min': min(subtraction_lst),
        'mid': round(median(subtraction_lst), 3),
        'avg': round(sum(subtraction_lst) / len(subtraction_lst), 3),
        '25': np.percentile(subtraction_lst, 25),
        '75': np.percentile(subtraction_lst, 75),
        'frq': len(subtraction_lst),
    }
    distribution_frame.loc[distribution_frame.shape[0], :] = statistically

    # if uid == '042E0115':
    #     print(statistically, subtraction_dict[uid])

    # box plot
    # if len(subtraction_lst) > 0:
    #     plot_data.append(subtraction_lst)
    #     plot_label.append(uid)
    # else:
    #     pass

print('填表。。。。。。')

distribution_frame.to_excel('xls/%s_distribute.xlsx' % TABLE, index=False)
# unique_business_class = []
# unique_business_Cname = []
# for uid in unique_business_id:
#     for index in range(BusinessClassData.shape[0]):
#         business_id = BusinessClassData.loc[index, 'business_id']
#         if uid == business_id:
#             unique_business_class.append(BusinessClassData.loc[index, 'business_class'])
#             unique_business_Cname.append(BusinessClassData.loc[index, 'class_name'])
#         else:
#             pass

# 创建箱线图对象
# box1 = (
#     Boxplot()
#         .add_xaxis(plot_label[:30])
#         .add_yaxis('时间间隔数据', plot_data[:30])
#         .set_global_opts(title_opts=opts.TitleOpts(title='相同 business_id 时间间隔分布图'),
#                          xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-60)))
# )
#
# box2 = (
#     Boxplot()
#         .add_xaxis(plot_label[30:60])
#         .add_yaxis('时间间隔数据', plot_data[30:60])
#         .set_global_opts(title_opts=opts.TitleOpts(title='相同 business_id 时间间隔分布图'),
#                          xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-60)))
# )
#
# box3 = (
#     Boxplot()
#         .add_xaxis(plot_label[60:90])
#         .add_yaxis('时间间隔数据', plot_data[60:90])
#         .set_global_opts(title_opts=opts.TitleOpts(title='相同 business_id 时间间隔分布图'),
#                          xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-60)))
# )
#
# box4 = (
#     Boxplot()
#         .add_xaxis(plot_label[90:])
#         .add_yaxis('时间间隔数据', plot_data[90:])
#         .set_global_opts(title_opts=opts.TitleOpts(title='相同 business_id 时间间隔分布图'),
#                          xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-60))
#                          )
# )
#
# grid = (Grid()
#         .add(box4, grid_opts=opts.GridOpts(pos_bottom='5%', pos_top='75%'))
#         .add(box3, grid_opts=opts.GridOpts(pos_bottom='25%', pos_top='50%'))
#         .add(box2, grid_opts=opts.GridOpts(pos_bottom='50%', pos_top='25%'))
#         .add(box1, grid_opts=opts.GridOpts(pos_bottom='75%', pos_top='0%'))
#         )
#
# grid.width = '2480px'
# grid.height = '1280px'
# grid.render('htm/boxplot_%s.html' % FILE)
#
# distribution_frame.to_excel('xls/%s_distribution.xlsx' % FILE, index=False, encoding='utf-8')
# medians = distribution_frame.loc[:, ['uid', 'min']]
# medians.sort_values(by='min', inplace=True)
# bar = Bar()
# bar.add_xaxis(medians['uid'].to_list())
# bar.add_yaxis('最小时间差', medians['min'].to_list())
# bar.width = '2560px'
# bar.height = '1440px'
# bar.set_global_opts(title_opts=opts.TitleOpts(title="最小时间差"),
#                     xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-60))
#                     )
# bar.render('htm/bar_%s.html' % FILE)
