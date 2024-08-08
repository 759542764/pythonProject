import pandas as pd
da = pd.read_csv('/root/travel/hotel/district.csv')
print(da.columns)
area_counts = da.groupby('商圏').size().reset_index(name='酒店数量')
top_three_areas = area_counts.sort_values('酒店数量', ascending=False).head(3)['商圏'].tolist()
filtered_data = da[da['商圏'].isin(top_three_areas)]
hotel_type_counts = filtered_data.groupby(['商圏', '酒店类型']).size().reset_index(name='数量')
hotel_type_counts.to_csv('/root/travel/hotel/types.csv', index=None, encoding='UTF-8')
