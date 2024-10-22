"""聚类"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

sns.set_style('darkgrid')
# palette
plt.rcParams['font.family'] = 'sans-serif'  # Win
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

CheckInData = pd.read_csv('../csv/20240331_feature.csv')
# dtype={'BP': 'str', 'KC': 'str', 'PG': 'str', 'BT': 'str', 'SUB': 'str', }
# print(CheckInData.shape, CheckInData.columns, CheckInData.head(10))


plt.figure(figsize=(9, 6))
plt.scatter(x=CheckInData['SUB'],
            y=CheckInData['DIST'],
            c='Blue',
            s=15,
            marker='o',
            alpha=1,
            linewidths=0.5,
            edgecolors='white'
            )
plt.title('Two-dimensional spatial projection of Time-Distance and BusinessId-Distance', fontsize=12)
plt.xlabel('Time-Distance', fontsize=12)
plt.ylabel('ID-Distance', fontsize=12)
plt.savefig('fig/distance.pdf')

N_CLUSTER = 5
Cluster_classifier = KMeans(n_clusters=N_CLUSTER,
                            init='k-means++',
                            n_init=10,
                            max_iter=300,
                            tol=0.0001,
                            random_state=0,
                            )

features = CheckInData[['SUB', 'DIST']].values
Cluster_classifier.fit(features)
y_predict = Cluster_classifier.fit_predict(features)
# label_predict = []
# for pr in y_predict:
#     if pr == 0:
#         label_predict.append('cluster-1')
#     elif pr == 1:
#         label_predict.append('cluster-2')
#     elif pr == 2:
#         label_predict.append('cluster-3')
#     elif pr == 3:
#         label_predict.append('cluster-4')
#     elif pr == 4:
#         label_predict.append('cluster-5')
#     else:
#         pass

CheckInData['target'] = y_predict
CheckInData.to_excel('./csv/' + '20240331_cluster.xlsx', index=False, encoding='utf-8')

plt.figure(figsize=(9, 6))
plt.scatter(features[y_predict == 0, 0],
            features[y_predict == 0, 1],
            c='Blue',
            s=15,
            marker='o',
            alpha=1,
            label='cluster-1'
            )
plt.scatter(features[y_predict == 1, 0],
            features[y_predict == 1, 1],
            c='Grey',
            s=15,
            marker='h',
            alpha=1,
            label='cluster-2'
            )
plt.scatter(features[y_predict == 2, 0],
            features[y_predict == 2, 1],
            c='Green',
            s=15,
            marker='s',
            alpha=1,
            label='cluster-3'
            )
plt.scatter(features[y_predict == 3, 0],
            features[y_predict == 3, 1],
            c='Orange',
            s=15,
            marker='v',
            alpha=1,
            label='cluster-4'
            )
plt.scatter(features[y_predict == 4, 0],
            features[y_predict == 4, 1],
            c='Purple',
            s=15,
            marker='H',
            alpha=1,
            label='cluster-5'
            )
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

ClusteringData = CheckInData[['business_class', 'class_name', 'target']]
Clustering_1data = ClusteringData[ClusteringData['target'] == 0]['class_name'].to_list()
Clustering_2data = ClusteringData[ClusteringData['target'] == 1]['class_name'].to_list()
Clustering_3data = ClusteringData[ClusteringData['target'] == 2]['class_name'].to_list()
Clustering_4data = ClusteringData[ClusteringData['target'] == 3]['class_name'].to_list()
Clustering_5data = ClusteringData[ClusteringData['target'] == 4]['class_name'].to_list()


# 统计每个元素的出现次数
def count(cluster):
    element_count = {}
    for item in cluster:
        if item in element_count:
            element_count[item] += 1
        else:
            element_count[item] = 1
    filtered_items = {key: value for key, value in element_count.items() if value > 30}
    labels = filtered_items.keys()
    sizes = filtered_items.values()
    colors = plt.cm.Paired(range(len(labels)))
    return labels, sizes, colors


picture = plt.figure(figsize=(9, 6))
ax1 = picture.add_subplot(2, 3, 1)
plt.title('Cluster-1')
plt.pie(count(Clustering_1data)[1],
        labels=count(Clustering_1data)[0],
        colors=count(Clustering_1data)[2],
        autopct='%1.1f%%',
        startangle=90)
plt.axis('equal')

ax2 = picture.add_subplot(2, 3, 2)
plt.title('Cluster-2')
plt.pie(count(Clustering_2data)[1],
        labels=count(Clustering_2data)[0],
        colors=count(Clustering_2data)[2],
        autopct='%1.1f%%', startangle=90)
plt.axis('equal')

ax3 = picture.add_subplot(2, 3, 3)
plt.title('Cluster-3')
plt.pie(count(Clustering_3data)[1],
        labels=count(Clustering_3data)[0],
        colors=count(Clustering_3data)[2],
        autopct='%1.1f%%', startangle=90)
plt.axis('equal')

ax4 = picture.add_subplot(2, 3, 4)
plt.title('Cluster-4')
plt.pie(count(Clustering_4data)[1],
        labels=count(Clustering_4data)[0],
        colors=count(Clustering_4data)[2],
        autopct='%1.1f%%', startangle=90)
plt.axis('equal')

ax5 = picture.add_subplot(2, 3, 5)
plt.title('Cluster-5')
plt.pie(count(Clustering_5data)[1],
        labels=count(Clustering_5data)[0],
        colors=count(Clustering_5data)[2],
        autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.savefig('fig/Cluster-pie.pdf')
plt.show()
