import pandas as pd
import os
from functools import reduce

def load_store_data(file_path):
    df = pd.read_csv(file_path)
    brand_name = os.path.basename(file_path).split('_')[0]
    store_counts = df['county'].value_counts().reset_index()
    store_counts.columns = ['county', brand_name]
    return store_counts

def merge_store_data(file_list, folder_path):
    store_dfs = [load_store_data(os.path.join(folder_path, file)) for file in file_list]
    result = reduce(lambda left, right: pd.merge(left, right, on='county', how='outer'), store_dfs)
    result.iloc[:, 1:] = result.iloc[:, 1:].fillna(0).astype(int)
    result["總飲料店數"] = result.iloc[:, 1:].sum(axis=1)
    return result

import drink_store_analysis as dsa
folder_path = 'drink_store/data/'
file_list = ['清心福全_全台門市資訊.csv',
             '50嵐_全台門市資訊.csv',
             '茶的魔手_門市資訊.csv',
             '麻古_全台門市資訊.csv',
             '可不可_全台門市資訊.csv',
             '得正_全台門市資訊.csv',
             'COMEBUY_全台門市資訊.csv']

if __name__ == '__main__':
    drink_store_df = dsa.merge_store_data(file_list, folder_path)
    drink_store_df.to_csv('全台七間連鎖飲料店門市.csv', index=False, encoding="utf-8-sig")
