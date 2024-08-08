import pandas as pd

da = pd.read_csv('/root/travel/hotel/hotels.txt', sep='\t')
print(da.head(10))
