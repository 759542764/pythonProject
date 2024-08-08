import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] # 设置中文显示plt.rcParams['axes,unicode minus']= False # 解决负号’'显示为方块的问题
#读取数据
da = pd.read_csv('/root/travel/hotel/district.csv', encoding='utf-8')

# 数据处理
average = da.groupby('酒店类型')['评分'].mean().reset_index(name='平均评分')

#绘制折线图
plt.plot(average['酒店类型'],average['平均评分'], marker='o')

#添加标题和标签
plt.title('各类型酒店平均评分走势')
plt.xlabel('酒店类型')
plt.ylabel('平均评分')
plt.show( )
plt.savefig('/root/travel/hotel/plot.png')