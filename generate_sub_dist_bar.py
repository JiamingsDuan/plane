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
CheckInData = pd.read_excel(FileName, dtype={'business_id': str})


def slice_data(refer_col, slice_col, ids):
    index_list = CheckInData[CheckInData[refer_col] == ids].index.to_list()
    business_time_list = CheckInData.loc[index_list, slice_col].to_list()
    return {ids: sorted(business_time_list)}


unique_business_id = list(set(CheckInData['business_id'].to_list()))

# Business_Time_Distance:mark 'SUB'
subtractions = [0, ]
# second index to last index
for index in range(CheckInData.shape[0]):
    if index < CheckInData.shape[0] - 1:
        subtraction = pd.to_datetime(CheckInData.loc[index + 1, 'business_time']) \
                      - pd.to_datetime(CheckInData.loc[index, 'business_time'])
        subtractions.append(round(subtraction.total_seconds() % 60, 3))
    else:
        pass

CheckInData['SUB'] = subtractions

distribution_frame = pd.DataFrame(columns=['uid', 'max', 'min', 'mid', 'avg'])


for uid in unique_business_id:
    subtraction_dict = slice_data('business_id', 'SUB', uid)
    statistically = {
        'uid': uid,
        'max': max(subtraction_dict[uid]),
        'min': min(subtraction_dict[uid]),
        'mid': round(median(subtraction_dict[uid]), 3),
        'avg': round(sum(subtraction_dict[uid]) / len(subtraction_dict[uid]), 3),
    }
    distribution_frame.loc[distribution_frame.shape[0], :] = statistically

x1 = distribution_frame.loc[:, 'uid'].to_list()
y1 = distribution_frame.loc[:, 'min'].to_list()
y2 = distribution_frame.loc[:, 'mid'].to_list()
y3 = distribution_frame.loc[:, 'avg'].to_list()
y4 = distribution_frame.loc[:, 'max'].to_list()


bar = Bar()
bar.add_xaxis(x1)
bar.add_yaxis('最小值', y1, stack='stack1')
bar.add_yaxis('中位数', y2, stack='stack1')
bar.add_yaxis('平均值', y3, stack='stack1')
bar.add_yaxis('最大值', y4, stack='stack1')
bar.set_series_opts(
    label_opts=opts.LabelOpts(
        position='right',
    )
)
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
    title_opts=opts.TitleOpts(title='相同 business_id 的 business_time间隔最小值、中位数、最大值分布图'),
    brush_opts=opts.BrushOpts(),
    datazoom_opts=opts.DataZoomOpts(),
)
bar.height = '1080px'
bar.width = '1920px'
bar.render('htm/bar1_%s.html' % FILE)
# bar.render_notebook()
