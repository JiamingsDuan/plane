import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
plt.rcParams['font.family'] = 'sans-serif'  # Win
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


FILE = 'csv/travelsky_120DT_id1.csv'
CheckInData_f = pd.read_csv(FILE, encoding='gbk')

CheckInData_w = CheckInData_f.loc[:, [col for col in CheckInData_f.columns if col != '结束']].fillna(0)
# 计算相关系数矩阵
corr_matrix = CheckInData_w.corr().round(3) * 100

plt.figure(figsize=(20, 16))
sns.heatmap(corr_matrix.to_numpy(), annot=True)
plt.yticks(ticks=range(0, 58), labels=list(corr_matrix.index), rotation=0)
plt.xticks(ticks=range(0, 58), labels=list(corr_matrix.columns), rotation=-90)
plt.title('Similarity Matrix')
plt.savefig('fig/matrix.pdf')
