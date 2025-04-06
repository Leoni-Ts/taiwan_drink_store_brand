import pandas as pd
import os

file_path = os.path.join('drink_store/data', '全台七間連鎖飲料店門市.csv')
file_path2 = os.path.join('drink_store/data', '縣市特徵.csv')
drink_store_df = pd.read_csv(file_path, encoding='utf-8')
county_df = pd.read_csv(file_path2, encoding = 'utf-8')
tw_county_df = pd.merge(drink_store_df, county_df, on='county', how='outer')
tw_county_df['每萬人飲料店數'] = tw_county_df['總飲料店數']/(tw_county_df['人口數']/10000)
order = ['county', '清心福全', '50嵐', '茶的魔手', '麻古', '可不可', '得正', 'COMEBUY', '總飲料店數',
         '人均可支配所得', '每萬人飲料店數', '10~24歲人口數', '25~45歲人口數', '旅宿業房間數']
tw_county_df = tw_county_df.reindex(columns = order)

tw_county_df.to_csv('drink_store_county_data.csv', index=False, encoding="utf-8-sig")

