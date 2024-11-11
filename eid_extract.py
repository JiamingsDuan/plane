# 120DT柜台数据业务视角提取路径，并为business_id打上id组的标签
import pandas as pd
import sqlite3
from tqdm import tqdm

# parameter
'''
07089,088OJ,0904C,0904H,0904Q,0904U,09053,09058,09059,0905E,
094D9,094DI,094DC,094HR,094HU,094HY,120CG,120DT,120IK,120IN,120IQ,
120IX,12101,130CC,132FH,1348V,1348X,13490,13493,13496,13498,
144GR,198IB,198IE,198IH,198IK,198IL,198IN,198IT,198IW,198IZ
'''

# eid_name = '09058'

eid_list = [
    '07089', '0904C', '0904H', '0904Q', '0904U', '09053', '09059', '0905E', '094D9',
    '094DI', '094DC', '094HR', '094HU', '094HY', '120CG', '120DT', '120IK', '120IN',
    '120IQ', '120IX', '12101', '130CC', '1348V', '1348X', '13490', '13493', '13498',
    '144GR', '198IE', '198IH', '198IL', '198IN', '198IT', '198IW', '198IZ',
]

for eid_name in eid_list:

    table_name = 'travelsky_%s_with_group' % eid_name
    connection = sqlite3.connect('E:/BaiduNetdiskDownload/database/CheckIndata.db',
                                 detect_types=sqlite3.PARSE_DECLTYPES,
                                 check_same_thread=False)
    connection.text_factory = str

    print('extract the data......')
    query = f"SELECT business_id, business_time from travelsky_total_with_type where eid = '%s'" % eid_name
    CheckInData = pd.read_sql_query(query, con=connection)

    # print(CheckInData.isnull().sum())
    print('extract the Business Id Class')
    query1 = "SELECT class_name, business_id, business_class, business_short from BusinessClass1108"
    BusinessIdClassData = pd.read_sql_query(query1, con=connection, dtype={'business_id': 'str',
                                                                           'business_class': 'str',
                                                                           'class_name': 'str',
                                                                           })

    print('mark business_class、class_name......')
    CheckInData[['business_class', 'class_name', 'business_short']] = ''

    # Business_Part:mark 'business_class', 'class_name'
    for index in tqdm(range(CheckInData.shape[0])):
        business_id = CheckInData.loc[index, 'business_id']
        if business_id in BusinessIdClassData['business_id'].to_list():
            class_index = BusinessIdClassData[BusinessIdClassData['business_id'] == business_id].index[0]
            series = BusinessIdClassData.loc[class_index, ['business_class', 'class_name', 'business_short']]
            CheckInData.loc[index, ['business_class', 'class_name', 'business_short']] = series
        else:
            CheckInData.loc[index, ['business_class', 'class_name', 'business_short']] = None

    # initialize the starting node and ending node
    start_list = ['042E0102', '042E0105', '042E0115',
                  '042E0200', '042E0201', '042E0211',
                  '042E0212', '042E0219', '162R0300',
                  '16200100', '16200101', '16240100', '162R0101']
    end_list = ['042E0117', '042E0223', '01010915',
                '01010916', '01010917', '01010903',
                '042E0224', '01010600', 'nav']

    print('marker the business_id label')
    label_list = []
    for index in range(CheckInData.shape[0]):

        Record = CheckInData.loc[index, 'business_id']
        if index == 0:
            label_list.append('0')
        else:
            Record_Last = CheckInData.loc[index - 1, 'business_id']
            if Record in start_list:
                label_list.append('1')
                # Record['business_label'] = 1

            elif Record in end_list:
                label_list.append('-1')
                # Record['business_label'] = -1

            elif Record == '042E0200' and CheckInData.iloc[index + 1, 'business_id'] == '042E0112':
                label_list.append('1')
                # Record['business_label'] = 1

            elif Record == '042E0224' and Record_Last == '042E0200':
                label_list.append('-1')
                # Record['business_label'] = -1

            elif Record == '042E0200' and CheckInData.loc[index + 1, 'business_id'] != '042E0112' \
                    and CheckInData.loc[index + 1, 'business_id'] != '042E0224':
                label_list.append('1')
                # Record['business_label'] = 1
            else:
                label_list.append('0')
                # Record['business_label'] = 0

    # slice the data and obtain the route label save into the LabelList
    print('slice the basic route')
    CheckInData['business_label'] = label_list

    print('write the data to Sqlite......')
    CheckInData.to_sql(name=table_name,
                       con=connection,
                       if_exists='replace',
                       index=False,
                       )
