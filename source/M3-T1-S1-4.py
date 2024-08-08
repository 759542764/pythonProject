import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文显示
plt.rcParams['axes.unicode_minus'] = False  # 解决负号’'显示为方块的问题
# 读取数据
da = pd.read_csv('/root/travel/hotel/district.csv', encoding='utf-8')
print(da.columns)
hotel_sum = da.groupby('商圈').size().reset_index(name='酒店数量')
# 按照酒店数量进行降序排序a
top5_hotel = hotel_sum.sort_values('酒店数量', ascending=False).head(10)
# 创建柱状图

plt.figure(figsize=(20, 10))
plt.bar(top5_hotel['商圈'], top5_hotel['酒店数量'], color='skyblue')
plt.title('酒店数排名前十的商圈')
plt.xlabel('商圈')
plt.ylabel('酒店数量')
plt.show()
plt.savefig('/root/travel/hotel/bar.png')
