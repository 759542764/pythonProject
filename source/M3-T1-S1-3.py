import pandas as pd

da = pd.read_csv('/root/travel/hotel/district.csv')  # 筛出5星级酒店
da_five_star = da[da['酒店类型'] == '五星级']  # 分数平均
score_mean = da_five_star['评分山'].mean()
print('五星级酒店平均分为:\n{}'.format(score_mean))
