import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import sqlite3

df = pd.read_csv('drink_store_county_data.csv')
df = df.iloc[:19,:]

#寬轉長
df_long = df.melt(id_vars = ['county', '總飲料店數', '人均可支配所得', '每萬人飲料店數', '10~24歲人口數', '25~45歲人口數', '旅宿業房間數'],
                  var_name = 'brand', value_name = '店數')
column_order = ['county', 'brand', '店數', '總飲料店數', '人均可支配所得', '每萬人飲料店數', '10~24歲人口數', '25~45歲人口數', '旅宿業房間數']
df_long = df_long[column_order]
#加入品牌變數
brand_info = pd.DataFrame({
    'brand':['清心福全', '50嵐', '茶的魔手', '麻古', '可不可', '得正', 'COMEBUY'],
    'tea_price':[30, 35, 30, 35, 40, 30, 40],
    'main_product':[0, 0, 1, 2, 1, 1, 1]
})
df_brand = df_long.merge(brand_info, on = 'brand', how = 'left')
#調整部分品牌北部價格
def update_price(row):
    if row['county'] in ['台北市', '新北市', '基隆市', '新竹市', '桃園市', '新竹縣', '宜蘭縣']:
        if row['brand'] == '清心福全':
            return 35
        elif row['brand'] == '50嵐':
            return 40
    return row['tea_price']
df_brand['tea_price'] = df_brand.apply(update_price, axis=1)
df_brand['店數'] = pd.to_numeric(df_brand['店數'], errors='coerce')
df_brand = df_brand[df_brand['店數'] != 0]
df_brand = df_brand.reset_index(drop = True)


features = ['店數', '總飲料店數', '人均可支配所得', '每萬人飲料店數', '10~24歲人口數', '25~45歲人口數', 'tea_price', 'main_product']

X = df_brand[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#sse = []
#K_range = range(1, 6)
#for k in K_range:
#    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
#    kmeans.fit(X_scaled)
#    sse.append(kmeans.inertia_)

#plt.plot(K_range, sse, marker='o')
#plt.xlabel('K 值')
#plt.ylabel('SSE 誤差平方和')
#plt.title('找出最佳 K 值')
#plt.show()

best_k = 3
kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
df_brand['品牌分群'] = kmeans.fit_predict(X_scaled)

df_brand.to_excel('brand_clusters_0327.xlsx', index=False)

conn = sqlite3.connect('brand_clusters.db')
df_brand.to_sql('brand_data', conn, if_exists = 'replace', index = False)
conn.close()
