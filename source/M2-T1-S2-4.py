import pandas as pd

da = pd.read_csv('/root/travel/hotel/hotel.txt', sep='\t')
# 计算总平均评分
total_average_rating = round(da['评分'].mean(), 1)
print(total_average_rating)

# 将评分为空的数据设習为总平均评分
da['评分'].fillna(total_average_rating, inplace=True)

print(da['评分'])

file_name = '/root/travel/hotel/hotel2_c4_' + str(total_average_rating) + '.csv'
# 存储处理后的数据
da.to_csv(file_name, index=False)
