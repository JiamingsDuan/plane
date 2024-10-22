# 业务视角，统计business_id组的频次，以频次为特征使用Kmeans聚类
import csv
import sqlite3
import pandas as pd
from tqdm import tqdm
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from collections import Counter
from function_adjacent2 import find_adjacent_duplicates_index
from function_brt import determine_label
from function_label import find_segments


# parameter
N_CLUSTER = 10
COUNT = 200
FILE = 'csv/travelsky_120DT_class_prob.csv'
connection = sqlite3.connect('E:/BaiduNetdiskDownload/database/CheckIndata.db')
query = f"SELECT business_id, business_class, business_label, class_name from travelsky_120DT_with_group"

# extract the data
print('extract the data')
CheckInData = pd.read_sql_query(query, con=connection, dtype={'business_class': 'str'})
# print(CheckInData.isnull().sum())
counter = dict(Counter(CheckInData['class_name']))

result_index = find_segments(CheckInData['business_label'].to_list())
print('write into frame')


route_label_list = []
route_array_list = []
with open(FILE, mode='w', newline='', encoding='gbk') as file:

    wr = csv.DictWriter(file, fieldnames=counter.keys())
    wr.writeheader()

    for IndexSets in tqdm(result_index):

        RoutingBusinessId = CheckInData.loc[IndexSets[0]: IndexSets[-1], 'business_id'].to_list()
        RoutingBusinessIdUniqueIndex = find_adjacent_duplicates_index(RoutingBusinessId)
        RoutingBusinessClass = CheckInData.loc[IndexSets[0]: IndexSets[-1], 'class_name'].to_list()
        RoutingBusinessClassUnique = [RoutingBusinessClass[i] for i in RoutingBusinessIdUniqueIndex]
        route_length = len(RoutingBusinessClassUnique)
        route_counter = dict(Counter(RoutingBusinessClassUnique))
        probabilities = {key: round(value / route_length, 2) for key, value in route_counter.items()}
        Id_array = '\n'.join(RoutingBusinessId)
        route_array_list.append(Id_array)
        RouteLabel = determine_label(
            CheckInData.loc[IndexSets[0], 'business_id'],
            CheckInData.loc[IndexSets[-1], 'business_id'],
        )
        route_label_list.append(RouteLabel)

        wr.writerow(rowdict=probabilities)

    file.close()

CheckInData_f = pd.read_csv(FILE, encoding='gbk')
description = CheckInData_f.describe()
choose_cols = [group for group, count in description.loc['count', :].to_dict().items() if count > COUNT]
CheckInData_f = CheckInData_f.loc[:, choose_cols].fillna(0)

agg = AgglomerativeClustering(n_clusters=N_CLUSTER)
kms = KMeans(n_clusters=N_CLUSTER)

labels_pred = kms.fit_predict(CheckInData_f.to_numpy())
print(labels_pred)
CheckInData_f['聚类'] = labels_pred
CheckInData_f['路径'] = route_array_list
CheckInData_f['BRT'] = route_label_list
CheckInData_f.to_excel('xls/kmeans_120DT_group_prob_%d_%d.xlsx' % (N_CLUSTER, COUNT), index=False)
