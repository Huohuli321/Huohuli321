"""
统计出911-数据中"不同月份""不同类型"的电话的"次数"的变化情况
"""

import pandas as pd
from matplotlib import pyplot as plt
pd.set_option('display.max_columns', None)

df = pd.read_csv('../Pandas用法/911.csv')

# 添加列，表示分类
temp_list = df['title'].str.split(': ')
cate_list = [i[0] for i in temp_list]
df["cata"] = cate_list

# 把时间字符串传换成时间类型
df['timeStamp'] = pd.to_datetime(df['timeStamp'])
# set_index应该放到后面，新建列cate_list的索引是数字，df的索引是时间戳，所以放后面才不会为NaN值
# set_index修改了索引，结果赋值就不可以了
df.set_index('timeStamp', inplace=True)

# 绘图
plt.figure(figsize=(16, 8), dpi=80)

_x = []
# 分组

# group_name=分组的名称（cata里面有三个不一样的元素，按照它们分组，三个名称）
# group_data=每个分组之后的名称包含的DataFrame数据
for group_name, group_data in df.groupby(by='cata'):
    # resample 是Pandas中用于时间序列数据重采样的方法,将数据重新组织到以每月开始为间隔的时间序列上
    # 例如，如果你的原始数据包含了每一天的事件，resample('M') 会将数据重新组织为每个月的事件，
    count_by_month = group_data.resample('ME')['title'].count()
    # 画图
    _x = count_by_month.index
    _y = count_by_month.values
    plt.plot(_x, _y, label=group_name)  # 使用 group_name 作为标签

plt.xticks(_x, rotation=45)
plt.legend(loc='best')
plt.show()
