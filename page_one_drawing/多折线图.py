import pyecharts.options as opts
from pyecharts.charts import Line
import os

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.realpath(__file__))

# 生成图表并保存到当前脚本所在的文件夹下
output_file = os.path.join(script_dir, "carbon_price_chart.html")

# 数据
x_data = ["2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06", 
          "2024-07", "2024-08", "2024-09", "2024-10", "2024-11", "2024-12"]
max_data = [57, 65, 69, 65, 58, 62, 58, 79, 73, 66, 53, 61]
min_data = [42, 51, 48, 46, 36, 42, 34, 49, 38, 30, 40, 37]
avg_data = [47, 58, 58, 53, 48, 56, 47, 64, 62, 52, 47, 50]

# 创建折线图
(
    Line(init_opts=opts.InitOpts(width="585px", height="240px"))
    .add_xaxis(xaxis_data=x_data)
    .add_yaxis(
        series_name="最大值",
        y_axis=max_data,
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_yaxis(
        series_name="最小值",
        y_axis=min_data,
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_yaxis(
        series_name="平均值",
        y_axis=avg_data,
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(is_show=False),
        legend_opts=opts.LegendOpts(
            is_show=True,  # 显示图例
            textstyle_opts=opts.TextStyleOpts(color="#FFFFFF")  # 设置图例字体颜色为白色
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=False),  # 去掉竖着的网格线
            axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#FFFFFF")),  # Y 轴线条为白色
        ),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            boundary_gap=False,
            axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#FFFFFF")),  # X 轴线条为白色
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