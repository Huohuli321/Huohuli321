# 评分分布状态
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas as pd

# 设置Pandas以显示所有列
pd.set_option('display.max_columns', None)
file_path = 'IMDB-Movie-Data.csv'
df = pd.read_csv(file_path)

# 取到Runtime (Minutes)这列的值
runtime_data = df['Rating'].values

plt.figure(figsize=(10, 8), dpi=80)

# 计算直方图的箱子数量   0.5=箱子宽度
num_bin = int((max(runtime_data) - min(runtime_data)) / 0.5)

# np.linspace 生成的是均匀分布的值，这里用于确保箱子边缘与X轴刻度对齐
# np.linspace 是 NumPy 库中的一个函数，用于在指定的区间内生成一个均匀分布的值的数组。这个函数非常有用，特别是在你需要创建一个具有固定步长的值的序列时。
"""
np.linspace(start, stop, num): 生成从 start 到 stop 的 num 个均匀间隔的值。
min(runtime_data): 计算 runtime_data 数组中的最小值，即电影时长的最小值。
max(runtime_data): 计算 runtime_data 数组中的最大值，即电影时长的最大值。
num_bin + 1: num_bin 是计算出的箱子数量，+1 是因为 linspace 函数会在指定的间隔内包含起始点和终点，所以总的箱子边界数比箱子数多一个。
"""
# 设置用作直方图的箱子（bins）的边界
bin_edges = np.linspace(min(runtime_data), max(runtime_data), num_bin + 1)
print(bin_edges)
# 绘制直方图
plt.hist(runtime_data, bins=bin_edges, edgecolor='black')

# 设置X轴刻度
plt.xticks(bin_edges)

# 网格
plt.grid()

# 添加描述信息
my_font = font_manager.FontProperties(fname='C:/Windows/Fonts/msyhl.ttc')
plt.xlabel('电影的时长 (分钟)', fontproperties=my_font)
plt.ylabel('电影数量', fontproperties=my_font)

# 显示图表
plt.show()