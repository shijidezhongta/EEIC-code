import os
from pyecharts import options as opts
from pyecharts.charts import Pie

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.realpath(__file__))

# 生成图表并保存到当前脚本所在的文件夹下
output_file = os.path.join(script_dir, "pie.html")

# 默认初始数据，如果没有传入自定义数据
data = [("抽水蓄能", 45), ("氢储能", 20), ("电化学储能", 30), ("压缩空气储能", 5)]

c = (
    Pie(init_opts=opts.InitOpts(width="380px", height="310px"))
    .add("", data)
    .set_colors(["#6d4bac", "#b389f2", "#568ff2", "#0099c6"])
    .set_global_opts(
        legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="#44B7FF"))  # 设置图例文字颜色
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%", color="#44B7FF"))  # 显示百分比
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




