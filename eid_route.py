import csv
import sqlite3
import pandas as pd
from tqdm import tqdm
from function_label import find_segments
from function_brt import determine_label

# parameter
'''
07089,088OJ,0904C,0904H,0904Q,0904U,09053,09058,09059,0905E,
094D9,094DI,094DC,094HR,094HU,094HY,120CG,120DT,120IK,120IN,120IQ,
120IX,12101,130CC,132FH,1348V,1348X,13490,13493,13496,13498,
144GR,198IB,198IE,198IH,198IK,198IL,198IN,198IT,198IW,198IZ
'''

# eid = '07089'

eid_list = [
    '07089', '0904C', '0904H', '0904Q', '0904U', '09053', '09059', '0905E', '094D9',
    '094DI', '094DC', '094HR', '094HU', '094HY', '120DT', '120CG', '120IK', '120IN',
    '120IQ', '120IX', '12101', '130CC', '1348V', '1348X', '13490', '13493', '13498',
    '144GR', '198IE', '198IH', '198IL', '198IN', '198IT', '198IW', '198IZ',
]
with open('rate.csv', mode='w', newline='', encoding='gbk') as file:
    wr = csv.DictWriter(file, fieldnames=['柜台编号', '未覆盖率'])
    wr.writeheader()

    for eid in eid_list:
        print('slice the %s' % eid)
        TABLE = 'travelsky_%s_with_group' % eid
        FILE = 'csv/travelsky_%s_with_group.csv' % eid
        connection = sqlite3.connect('E:/BaiduNetdiskDownload/database/CheckIndata.db')
        query = f"SELECT business_id, business_class, business_label, class_name from {TABLE}"

        CheckInData = pd.read_sql_query(query, con=connection, dtype={'business_class': 'str',
                                                                      'class_name': 'str',
                                                                      'business_id': str,
                                                                      })
        print(CheckInData.isnull().sum())

        # obtain the slice result and slice index result
        LabelList = CheckInData['business_label'].to_list()
        result_index = find_segments(LabelList)

        length = [i for i in range(0, CheckInData.shape[0])]
        index = []
        for IndexSets in tqdm(result_index):
            index_list = length[IndexSets[0]: IndexSets[-1]]
            index = index + index_list

            # with open(FILE, mode='w', newline='', encoding='gbk') as file:
            #     wr = csv.DictWriter(file, fieldnames=['路径编号', '业务ID', '业务组名称', '路径编码'])
            #     wr.writeheader()
            #     row = 1
            #
            #     for IndexSets in tqdm(result_index):
            #         # generate basic route label
            #         startingBusinessID = CheckInData.iloc[IndexSets[0], :]['business_id']
            #         endingBusinessID = CheckInData.iloc[IndexSets[-1], :]['business_id']
            #         RouteLabel = determine_label(starting=startingBusinessID, ending=endingBusinessID)
            #         LabelList.append(RouteLabel)
            #         # generate basic route business_id
            #         RouteBusinessID = CheckInData.loc[IndexSets[0]:IndexSets[-1], 'business_id'].to_list()
            #         # generate basic route business_class
            #         RouteBusinessName = CheckInData.loc[IndexSets[0]:IndexSets[-1], 'class_name'].to_list()
            #         BusinessIdFrame = '\n'.join(RouteBusinessID)
            #         BusinessIdClassNameFrame = '\n'.join(RouteBusinessName)
            #         route_dict = {
            #             '路径编号': row,
            #             '业务ID': BusinessIdFrame,
            #             '业务组名称': BusinessIdClassNameFrame,
            #             '路径编码': RouteLabel,
            #         }
            #
            #         wr.writerow(rowdict=route_dict)
            #         row = row + 1
            #
            #     file.close()
        except_index = list(set(length) - set(index))
        rate = round(len(except_index) / len(length), 4)
        print('%s未覆盖率: %s' % (eid, rate))
        route_dict = {
                    '柜台编号': str(eid),
                    '未覆盖率': str(rate),
                }
        wr.writerow(rowdict=route_dict)
        ExceptData = CheckInData.loc[sorted(except_index), :]
        ExceptData.to_excel('csv/xls/travelsky_%s_except.xlsx' % eid)