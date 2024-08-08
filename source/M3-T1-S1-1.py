import pandas as pd

da = pd.read_csv('/root/travel/hotel/district.csv', encoding='utf-8-sig', sep='\s*,\s*', engine='python')
da.columns = da.columns.str.strip()
print(da.columns)
group_da = da.groupby(6)
hotel_sum = group_da.size().reset_index(name='酒店数量')
# 按照酒店数量逬行降序排序
top5_hotel = hotel_sum.sort_values('酒店数量', ascending=False).head(5)
print(top5_hotel)
top5_hotel.to_csv('/root/travel/hotel/hotel_sum.csv', index=None, encoding='UTF-8')
