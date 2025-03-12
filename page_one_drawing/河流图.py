import pyecharts.options as opts
from pyecharts.charts import ThemeRiver
import os
# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.realpath(__file__))

# 生成图表并保存到当前脚本所在的文件夹下
output_file = os.path.join(script_dir, "river.html")

x_data = ["火电", "风电", "光伏"]
y_data = [
    [0, 230, "火电"],
    [1, 180, "火电"],
    [2, 144, "火电"],
    [3, 120, "火电"],
    [4, 124, "火电"],
    [5, 135, "火电"],
    [6, 136, "火电"],
    [7, 142, "火电"],
    [8, 156, "火电"],
    [9, 198, "火电"],
    [10, 208, "火电"],
    [11, 217, "火电"],
    [12, 229, "火电"],
    [13, 213, "火电"],
    [14, 217, "火电"],
    [15, 224, "火电"],
    [16, 226, "火电"],
    [17, 229, "火电"],
    [18, 236, "火电"],
    [19, 245, "火电"],
    [20, 267, "火电"],
    [21, 289, "火电"],
    [22, 287, "火电"],
    [23, 240, "火电"],
    [0, 80, "风电"],
    [1, 90, "风电"],
    [2, 70, "风电"],
    [3, 20, "风电"],
    [4, 30, "风电"],
    [5, 40, "风电"],
    [6, 35, "风电"],
    [7, 39, "风电"],
    [8, 60, "风电"],
    [9, 40, "风电"],
    [10, 30, "风电"],
    [11, 50, "风电"],
    [12, 80, "风电"],
    [13, 70, "风电"],
    [14, 50, "风电"],
    [15, 73, "风电"],
    [16, 82, "风电"],
    [17, 71, "风电"],
    [18, 94, "风电"],
    [19, 47, "风电"],
    [20, 41, "风电"],
    [21, 50, "风电"],
    [22, 45, "风电"],
    [23, 35, "风电"],
    [0, 0, "光伏"],
    [1, 0, "光伏"],
    [2, 0, "光伏"],
    [3, 0, "光伏"],
    [4, 0, "光伏"],
    [5, 0, "光伏"],
    [6, 21, "光伏"],
    [7, 25, "光伏"],
    [8, 45, "光伏"],
    [9, 57, "光伏"],
    [10, 69, "光伏"],
    [11, 104, "光伏"],
    [12, 150, "光伏"],
    [13, 190, "光伏"],
    [14, 201, "光伏"],
    [15, 180, "光伏"],
    [16, 142, "光伏"],
    [17, 79, "光伏"],
    [18, 49, "光伏"],
    [19, 7, "光伏"],
    [20, 0, "光伏"],
    [21, 0, "光伏"],
    [22, 0, "光伏"],
    [23, 0, "光伏"],
]
(
    ThemeRiver(init_opts=opts.InitOpts(width="585px", height="240px"))
    .add(
        series_name=x_data,
        data=y_data,
        singleaxis_opts=opts.SingleAxisOpts(
            pos_top="70", pos_bottom="50",axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#FFFFFF")  # 将单轴线条设置为白色
            ),
        ),
    )
    .set_series_opts(
        label_opts=opts.LabelOpts(is_show=False),  # 隐藏数据标签
    )
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line"),
        legend_opts=opts.LegendOpts(
            is_show=True,  # 显示图例
            textstyle_opts=opts.TextStyleOpts(color="#FFFFFF")  # 设置图例字体颜色为白色
        ),
    )
    .render(output_file)
)

# 读取生成的 HTML 文件
with open(output_file, 'r', encoding='utf-8') as file:
    html_content = file.read()

# 添加自定义 CSS 样式：设置页面高度、去除默认边距
custom_css = """
    <style>
        html, body {
            height: 100%;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #002D4A;
        }
        #main {
            width: 95%;
            height: 95%;
        }
    </style>
"""

# 将自定义 CSS 插入到 <head> 部分
html_content = html_content.replace('</head>', custom_css + '</head>')

# 重新写回修改后的 HTML 内容
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(html_content)