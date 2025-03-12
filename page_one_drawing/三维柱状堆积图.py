import os
import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar3D
from pyecharts.commons.utils import JsCode
import json

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.realpath(__file__))
output_file = os.path.join(script_dir, "energy_balance_3d.html")

# 定义时间和能源类型
hours = list(range(24))
energy_types = ["火电", "风电", "太阳能", "抽水蓄能", "电化学储能", "压缩空气储能", "氢储能", "用户用电"]

# 生成模拟数据（单位：MW）
np.random.seed(42)
data = pd.DataFrame({
    "火电": np.random.uniform(50, 100, 24),
    "风电": np.random.uniform(0, 60, 24),
    "太阳能": [0] * 6 + list(np.random.uniform(20, 80, 12)) + [0] * 6,
    "抽水蓄能": np.random.uniform(-20, 20, 24),
    "电化学储能": np.random.uniform(-15, 15, 24),
    "压缩空气储能": np.random.uniform(-10, 10, 24),
    "氢储能": np.random.uniform(-5, 5, 24),
    "用户用电": np.random.uniform(80, 150, 24)
}, index=hours)

# 转换为 Bar3D 所需格式：[x, y, z]
data_list = []
for hour in hours:
    for energy_idx, energy in enumerate(energy_types):
        value = data.loc[hour, energy]
        data_list.append([hour, energy_idx, value])

    # Bar3D(init_opts=opts.InitOpts(width="1400px", height="750px"))
# 创建三维柱状图
c = (
    Bar3D(init_opts=opts.InitOpts(width="1400px", height="750px"))
    .add(
        series_name="",
        data=data_list,
        xaxis3d_opts=opts.Axis3DOpts(type_="category", data=hours, name="时间 (小时)"),
        yaxis3d_opts=opts.Axis3DOpts(
            type_="category",
            data=energy_types,
            name="能源类型",
            axislabel_opts=opts.LabelOpts(interval=0, rotate=45),  # 显示所有标签并旋转
        ),
        zaxis3d_opts=opts.Axis3DOpts(type_="value", name="功率 (MW)"),
        grid3d_opts=opts.Grid3DOpts(width=100, depth=100, rotate_speed=150),

    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            min_=-20,
            max_=150,
            range_color=["#14517b", "#5282b0", "#d7f3ff"],  # 颜色渐变
        ),
        title_opts=opts.TitleOpts(title="一天内源-网-荷-储互动情况（3D柱状图）"),
        legend_opts=opts.LegendOpts(is_show=False),
    )
    .render(output_file)
)

# 读取生成的 HTML 文件并添加自定义 CSS
with open(output_file, 'r', encoding='utf-8') as file:
    html_content = file.read()

custom_css = """
    <style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #f0f2f5;
        }
    </style>
"""

html_content = html_content.replace('</head>', custom_css + '</head>')

# 写回修改后的 HTML 内容
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(html_content)

