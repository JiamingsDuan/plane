"""按照编码聚类"""
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

# self define function load
from function_brt import determine_label
from function_label import find_sub_list


CheckInData = pd.read_csv('../csv/20240331_feature.csv')


# obtain the slice result and slice index result
LabelSeries = CheckInData['business_label']
LabelList = LabelSeries.to_list()
result, result_index = find_sub_list(LabelList)

# slice the data and obtain the route label save into the LabelList


DicList = []
for IndexSets in result_index:
    startingNode = IndexSets[0]
    endingNode = IndexSets[-1]
    # BusinessID_12 = CheckInData.iloc[IndexSets[0]: endingNode, :]['BP'].to_list()
    BusinessID_34 = CheckInData.iloc[IndexSets[0]: endingNode, :]['KC'].to_list()
    # print('12', [BusinessID_12])
    KC_dict = dict(Counter(BusinessID_34))
    DicList.append(KC_dict)


feature_map = pd.DataFrame(DicList)
features = feature_map.fillna(0)
# print(features)

# 创建 TSNE 对象并拟合数据
# tsne = TSNE(n_components=2, init='random', learning_rate='auto', random_state=42)
# data_transformed = tsne.fit_transform(features.values)
#
# # 可视化结果
# plt.scatter(data_transformed[:, 0], data_transformed[:, 1])
# plt.show()

N_CLUSTER = 3
Cluster_classifier = KMeans(n_clusters=N_CLUSTER,
                            init='k-means++',
                            n_init=10,
                            max_iter=300,
                            tol=0.0001,
                            random_state=0,
                            )

# Cluster_classifier.fit(features.values)
y_predict = Cluster_classifier.fit_predict(features.values)
data = features.values[:, :2]
plt.figure(figsize=(9, 6))
plt.scatter(data[:, :2][y_predict == 0, 0],
            data[:, :2][y_predict == 0, 1],
            c='Blue',
            s=15,
            marker='o',
            alpha=1,
            label='cluster-1'
            )
plt.scatter(data[:, :2][y_predict == 1, 0],
            data[:, :2][y_predict == 1, 1],
            c='Grey',
            s=15,
            marker='h',
            alpha=1,
            label='cluster-2'
            )
plt.scatter(data[:, :2][y_predict == 2, 0],
            data[:, :2][y_predict == 2, 1],
            c='Green',
            s=15,
            marker='s',
            alpha=1,
            label='cluster-3'
            )
# plt.scatter(data[:, :2][y_predict == 3, 0],
#             data[:, :2][y_predict == 3, 1],
#             c='Orange',
#             s=15,
#             marker='v',
#             alpha=1,
#             label='cluster-4'
#             )
# plt.scatter(data[:, :2][y_predict == 4, 0],
#             data[:, :2][y_predict == 4, 1],
#             c='Purple',
#             s=15,
#             marker='H',
#             alpha=1,
#             label='cluster-5'
#             )
plt.scatter(Cluster_classifier.cluster_centers_[:, 0],
            Cluster_classifier.cluster_centers_[:, 1],
            s=50,
            c='red',
            marker='*',
            label='centroids'
            )

plt.title('Clustering Effect of Binary Group', fontsize=12)
plt.xlabel('Time-Distance', fontsize=12)
plt.ylabel('ID-Distance', fontsize=12)
plt.savefig('fig/Cluster.pdf')
plt.legend()
plt.show()
