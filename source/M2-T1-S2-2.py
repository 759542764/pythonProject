import pandas as pd
da = pd.read_csv('/root/travel/hotel/hotel.txt',sep = '\t' )
a = da['起价']
a=list(a)
a = [a. replace("¥","").replace("起","") for a in a]
print(a)

a = pd.Series(a)
a.head()
d = pd.DataFrame({'最低价' : a})

result = pd.concat([da, d], axis=1)
result.head()
shuju=pd.DataFrame (result)
shuju.to_csv('/root/travel/hotel/hotel2_c2.csv')