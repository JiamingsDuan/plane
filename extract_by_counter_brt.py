# 业务视角，统计business_id组的频次，以频次为特征使用Kmeans聚类，并为特征设置权重
import csv
import sqlite3
import pandas as pd
from tqdm import tqdm
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from collections import Counter
from function_brt import determine_label
from function_label import find_segments

# parameter
W1 = {'检索提取': 5, '重打牌': 40, '行李交运': 40, '返回': 5,
      '旅客拉下': 40, '下一步值机': 5, '值机接收': 40, '客票详情': 15,
      '管理旅客备注': 40, '旅客详情': 15, '值机员综合办理统计': 15, '航班详情': 15,
      '座位锁放': 40, '旅客升降舱': 40, '办理历史': 15, '座位处理': 40, '航班值机情况查询': 5}

W2 = {'检索提取': 5, '重打牌': 40, '行李交运': 40, '返回': 5,
      '旅客拉下': 40, '下一步值机': 5, '值机接收': 40, '客票详情': 15,
      '管理旅客备注': 80, '旅客详情': 15, '值机员综合办理统计': 15, '航班详情': 15,
      '座位锁放': 80, '旅客升降舱': 80, '办理历史': 15, '座位处理': 80, '航班值机情况查询': 5}

N_CLUSTER = 10
COUNTER = '120DT'
FILE = 'csv/travelsky_120DT_id.csv'
connection = sqlite3.connect('E:/BaiduNetdiskDownload/database/CheckIndata.db')

query = f"SELECT business_id, business_class, business_label, class_name from travelsky_120DT_with_group"
print('extract the data')
CheckInData = pd.read_sql_query(query, con=connection, dtype={'business_class': 'str'})
# print(CheckInData.isnull().sum())
counter = dict(Counter(CheckInData['class_name']))
counter_2 = dict(Counter(CheckInData['business_id']))

result_index = find_segments(CheckInData['business_label'].to_list())
print('write into frame')

route_label_list = []
route_array_list = []
with open(FILE, mode='w', newline='', encoding='gbk') as file:
    wr = csv.DictWriter(file, fieldnames=counter.keys())
    wr.writeheader()

    for IndexSets in tqdm(result_index):
        RoutingBusinessClass = CheckInData.loc[IndexSets[0]: IndexSets[-1], 'class_name'].to_list()
        RoutingBusinessId = CheckInData.loc[IndexSets[0]: IndexSets[-1], 'business_id'].to_list()
        Id_array = '\n'.join(RoutingBusinessId)
        route_array_list.append(Id_array)
        RouteLabel = determine_label(
            CheckInData.loc[IndexSets[0], 'business_id'],
            CheckInData.loc[IndexSets[-1], 'business_id'],
        )
        # RoutingBusinessId = find_adjacent_duplicates(RoutingBusinessId)
        route_counter = dict(Counter(RoutingBusinessClass))
        route_label_list.append(RouteLabel)
        wr.writerow(rowdict=route_counter)

    file.close()

CheckInData_f = pd.read_csv(FILE, encoding='gbk')
description = CheckInData_f.describe()
choose_cols = []
for group, count in description.loc['count', :].to_dict().items():
    if count > 200:
        choose_cols.append(group)
    else:
        pass

# delete '结束' and fill None
CheckInData_w = CheckInData_f.loc[:, [col for col in choose_cols if col != '结束']].fillna(0)
# multiple weights: W
for col in choose_cols:
    if col in W1.keys():
        CheckInData_w[col] = CheckInData_w[col] * round(W1[col] / sum(W1.values()) * 100, 0)
        # CheckInData_w[col] = CheckInData_w[col] * W[col]
    else:
        pass


# CheckInData_w.to_excel('xls/kmeans_120DT_id_group_withW.xlsx', index=False)


# sc = StandardScaler()
# mm = MinMaxScaler()
# norm = Normalizer(norm='l1')
# StandardFrame = pd.DataFrame(columns=CheckInData_f.columns)


# for index in tqdm(range(CheckInData_f.shape[0])):
#     arr = np.array(CheckInData_f.loc[index, :].to_list())
#     normalized_array = norm.transform(arr.reshape(-1, 1))
#     StandardFrame.loc[index, :] = normalized_array[:, 0]


agg = AgglomerativeClustering(n_clusters=N_CLUSTER)
kms = KMeans(n_clusters=N_CLUSTER)

labels_pred = agg.fit_predict(CheckInData_w.to_numpy())
print(labels_pred)
CheckInData_w['聚类'] = labels_pred
CheckInData_w['路径'] = route_array_list
CheckInData_w['BRT'] = route_label_list
CheckInData_w.to_excel('xls/agg_120DT_id_group_cluster%s_w1.xlsx' % N_CLUSTER, index=False)

# cols = CheckInData_mul.columns
# df = CheckInData_mul.loc[:, cols]
# df.replace(0, '', inplace=True)
# df.replace(to_replace=np.nan, value='✔', inplace=True)
# df['聚类'] = labels_pred
# df['路径'] = route_array_list
# df['BRT'] = route_label_list
# df.to_excel('xls/true_120DT_id_group_cluster.xlsx', index=False)
