import pyecharts.options as opts
from pyecharts.charts import Line
import os
# 自定义数据
x_data = [str(i) for i in range(1, 25)]  # 生成1到24的字符串列表
y_data_A = [188.24, 183.01, 180.15, 179.01, 176.07, 178.39, 189.95, 228.85, 255.45, 276.35, 
            293.71, 282.57, 279.64, 266.31, 264.61, 264.61, 274.48, 303.93, 318.99, 338.11, 
            316.14, 273.87, 231.07, 194.04]

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.realpath(__file__))

# 生成图表并保存到当前脚本所在的文件夹下
output_file = os.path.join(script_dir, "chart.html")

# 使用 InitOpts 来设置宽度和高度
c = (
    Line(init_opts=opts.InitOpts(width="470px", height="385px"))  # 设置图表的宽高    
    .add_xaxis(x_data)  # 使用自定义的X轴数据
    .add_yaxis(
        "负荷", 
        y_data_A, 
        is_smooth=True, 
        color="#8ECDEC",  # 设置折线图颜色为鲜明的橙色，适合深色背景
    )  
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(color="#8ECDEC", opacity=0.3),  # 通过 areastyle_opts 设置面积图的填充颜色和透明度
        label_opts=opts.LabelOpts(is_show=False),  # 隐藏数据标签
    )
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(
            name="时间/h",  # X 轴命名
            name_location="middle",  # 轴名位置
            name_gap=30,  # 设置轴名与轴的间距
            name_textstyle_opts=opts.TextStyleOpts(font_size=16),  # 设置 X 轴标题字体大小
            axistick_opts=opts.AxisTickOpts(is_align_with_label=True),  # 设置 X 轴刻度与标签对齐
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#CCEDFF")  # X 轴线条为白色
            ),
            axislabel_opts=opts.LabelOpts(color="#CCEDFF"),  # X 轴标签颜色为白色
            splitline_opts=opts.SplitLineOpts(
                is_show=True,
                linestyle_opts=opts.LineStyleOpts(
                color="#CCEDFF",  # 网格线颜色
                opacity=0,  # 网格线透明度
                )
            ),
        ),
        yaxis_opts=opts.AxisOpts(
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#CCEDFF")  # Y 轴线条为白色
            ),
            axislabel_opts=opts.LabelOpts(color="#CCEDFF"),  # Y 轴标签颜色为白色
            splitline_opts=opts.SplitLineOpts(
                is_show=True,
                linestyle_opts=opts.LineStyleOpts(
                    color="#CCEDFF",  # 网格线颜色
                    opacity=0.2,  # 网格线透明度
                )
            ),            
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),  # 提示框设置
        legend_opts=opts.LegendOpts(is_show=False)  # 去掉图例
    )
    .render(output_file)  # 渲染并保存为 HTML 文件
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