import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']

plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

da = pd.read_csv('/root/travel/hotel/standard.csv')
tendencies = da['情感倾向'].value_counts()

plt.figure(figsize=(10, 6))
tendencies.plot(kind='bar', color='skyblue')
plt.title('情感倾向统计')
plt.xlabel('情感倾向')
plt.ylabel('计数')
plt.show()
plt.savefig('/root/travel/hotel/columnar.png')
