# # import pandas as pd
# # from pyecharts.charts import Map
# # from pyecharts import options as opts
# # from pyecharts.globals import ThemeType
# # import re

# # data = pd.read_csv('GDP.csv')
# # province = list(data["province"])
# # pro_sta=[]  # 去除后缀
# # clss = list(data["class"])
# # list = [list(z) for z in zip(province, clss)]


# # for i in province:
# #     # 设置要替换的字符
# #     i=re.sub('省|市|自治区|壮族自治区|回族自治区|维吾尔自治区|特别行政区','',i)
# #     # print(i)
# #     pro_sta.append(i)

# # #
# # # maptype='china' 只显示全国直辖市和省级
# # map = Map(init_opts=opts.InitOpts(width="1500px", height="800px", theme=ThemeType.VINTAGE))  # 添加主题
# # map.set_global_opts(
# #     # 标题配置项
# #     title_opts=opts.TitleOpts(
# #         title="等级分布地图",
# #         pos_left="center"
# #     ),
# #     # 图例配置项
# #     legend_opts=opts.LegendOpts(
# #         is_show=True,
# #         pos_left="left",
# #     ),
# #     # 视觉影射配置项
# #     visualmap_opts=opts.VisualMapOpts(
# #         min_=0,  # 组件最小值
# #         max_=300,
# #         range_text = ['等级程度分布颜色区间:', ''],  # 两端文本名称
# #         is_piecewise=True,  # 定义图例为分段型，默认为连续的图例
# #         pos_top= "middle",  # 组件离容器左侧的距离
# #         pos_left="left",
# #         orient="vertical",  # 布局方式为垂直布局，水平为horizon
# #         split_number=5  # 分成5个区间
# #     )
# # )
# # map.add("程度", list, maptype="china")
# # map.render("全国.html")

# # for i in pro_sta:
# #     province_city = (
# #         Map(init_opts=opts.InitOpts(width="1500px", height="800px", theme=ThemeType.VINTAGE))
# #         .add("",
# #              list,  # 可以自己写一个字典写各个省份下的市所对应的数据，在这里只是一个range()
# #              i)
# #         .set_global_opts(
# #             title_opts=opts.TitleOpts(title=i + "地图"),
# #             visualmap_opts=opts.VisualMapOpts(
# #                 min_=0,
# #                 max_=300,
# #                 is_piecewise=True
# #             )
# #         )
# #         .render(path=i + "地图.html")
# #     )
# import numpy as np

# # 定义谷时段、平时段、峰时段的购电价和售电价
# valley_buy_price = 0.20
# valley_sell_price = 0.46
# normal_buy_price = 0.20
# normal_sell_price = 0.35
# peak_buy_price = 0.20
# peak_sell_price = 0.27

# # 初始化一个长度为 24 的数组来存储每个时刻的电价
# electricity_prices = np.zeros(24)

# # 根据时段划分给数组赋值
# for i in range(24):
#     if 0 <= i < 8 or i == 23:
#         # 谷时段
#         electricity_prices[i] = valley_sell_price
#     elif 8 <= i < 12 or 18 <= i < 23:
#         # 平时段
#         electricity_prices[i] = normal_sell_price
#     else:
#         # 峰时段
#         electricity_prices[i] = peak_sell_price

# print("每个时刻的售电价数组:", electricity_prices)
import cplex
print(cplex.__version__)  # 需要≥12.10