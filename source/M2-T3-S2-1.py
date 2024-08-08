import pandas as pd

da = pd.read_csv('/root/travel/hotel/hotel.txt', sep='\t')
localtion = da['位置信息']
localtion = [localtion.replace("·", ",") for localtion in localtion]
delimiter = ','
df = pd.DataFrame(localtion, columns=['Column1'])['Column1'].str.split(delimiter, expand=True)
df = df.rename(columns={0: '商圈', 1: '景点'})
sss = pd.concat([da, df], axis=1)
shu = pd.DataFrame(sss)
print(sss.head(10))
wenben = shu.to_csv('/root/travel/hotel/district.csv', index=None, encoding='UTF-8')
