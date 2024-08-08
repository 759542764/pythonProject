import pandas as pd

da = pd.read_csv('/root/travel/hotel/district.csv')
da.columns = da.columns.str.strip()
print(da.columns)
a = da['起价']
a = list(a)
a = [int(a.replace("¥", "").replace("起", "")) for a in a]
a = pd.Series(a)
a.head()
d = pd.DataFrame({'最低价': a})
shu = pd.concat([da, d], axis=1)
shu.head()
area_counts = shu.groupby('商圏')['最低价'].mean().reset_index(name='平均最低价')
top_five = area_counts.sort_values('平均最低价').head(5)
print(top_five)
top_five.to_csv('/root/travel/hotel/price_mean.csv', index=None, encoding='UTF-8')
