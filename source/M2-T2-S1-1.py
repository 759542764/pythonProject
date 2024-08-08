from snownlp import SnowNLP
import pandas as pd
data = pd. read_csv('/root/travel/hotel/hotel_comment.csv')
#定义情感倾向标注函数
def get_sentiment_label (sentiment):
    if sentiment >= 0.7:
        return '正向'
    elif sentiment > 0.4:
        return '中性'
    else:
        return '负向'

standard_data = pd.DataFrame (columns=['编号','酒店名称','最热评价','情感倾向','备注'])
for index, row in data.iterrows():
    comment = row['最热评价']
    sentiment = SnowNLP(comment).sentiments
    label = get_sentiment_label (sentiment)
    standard_data. loc[index] = [index+1,row['酒店名称'],comment, label,'']
# 存储标注结果
print(standard_data. head())
standard_data.to_csv('/root/travel/hotel/standard.csv', index=False, encoding='utf8')