import json
import os
from pyecharts import options as opts
from pyecharts.charts import Graph

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.realpath(__file__))

# 生成图表并保存到当前脚本所在的文件夹下
output_file = os.path.join(script_dir, "graph_les_miserables.html")

with open("relationtest.json", "r", encoding="utf-8") as f:
    j = json.load(f)
    nodes = j["nodes"]
    links = j["links"]
    categories = j["categories"]

c = (
    Graph(init_opts=opts.InitOpts(width="1400px", height="750px"))
    .add(
        "",
        nodes=nodes,
        links=links,
        categories=categories,
        layout="circular",
        is_rotate_label=True,
        linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3),
        label_opts=opts.LabelOpts(position="right" , color="white"),
    )
    .set_global_opts(
        # title_opts=opts.TitleOpts(title="Graph-Les Miserables"),
        # legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%"),
        legend_opts = opts.LegendOpts(is_show=False),
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
            height: 100%;  /* 设置页面高度为100% */
            margin: 0;     /* 去除默认边距 */
            padding: 0;    /* 去除默认内边距 */
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #002D4A;
        }
    </style>
"""

# 将自定义 CSS 插入到 <head> 部分
html_content = html_content.replace('</head>', custom_css + '</head>')

# 重新写回修改后的 HTML 内容
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(html_content)