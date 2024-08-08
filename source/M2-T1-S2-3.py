import pandas as pd
da = pd.read_csv('/root/travel/hotel/hotel.txt',sep = '\t')
# 将评分为空的数据设置为 0
da['评分'].fillna(0, inplace=True)
# 存储处理后的数据
da.to_csv('/root/travel/hotel/hotel2_c3.csv', index=False)