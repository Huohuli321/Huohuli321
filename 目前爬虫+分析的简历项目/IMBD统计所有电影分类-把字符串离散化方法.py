"""
统计所有电影分类情况
"""
from matplotlib import pyplot as plt
from matplotlib import font_manager
import pandas as pd
import numpy as np

my_font = font_manager.FontProperties(fname='C:/Windows/Fonts/msyhl.ttc')

# 设置Pandas以显示所有列
pd.set_option('display.max_columns', None)
file_path = '../Pandas用法/IMDB-Movie-Data.csv'
df = pd.read_csv(file_path)

# 统计分类的列表
temp_list = df['Genre'].str.split(',').tolist()  # [[], [], []] 将1000部电影的分类情况统计到temp_list里

# 将temp_list里的列表拆分出来
genre_list = list(set([i for j in temp_list for i in j]))

# 构造全部为0的数组
zeros_df = pd.DataFrame(np.zeros((df.shape[0], len(genre_list))), columns=genre_list)

# 给每部电影的分类地方赋值为1
for i in range(df.shape[0]):
    # zeros_df.loc[0-999, ['Action', 'Adventure', 'Sci-Fi']] = 1
    # 查找第i行，第temp_list[i]列的位置，赋值为1， zeros_df的列名就是temp_list拿出来的
    zeros_df.loc[i, temp_list[i]] = 1
# 求每个分类都有多少部电影
genre_count = zeros_df.sum(axis=0)

# 排序
genre_count = genre_count.sort_values()
# 取genre_count索引 (分类名)
_x = genre_count.index
# 取值 (分类数量)
_y = genre_count.values

# 画图
plt.figure(figsize=(20, 8), dpi=80)
# 条形图
plt.bar(range(len(_x)), _y, width=0.4, color='r')
# x刻度
plt.xticks(range(len(_x)), _x)
plt.grid()

plt.show()