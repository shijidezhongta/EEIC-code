from pyecharts import options as opts
from pyecharts.charts import Grid, Liquid
from pyecharts.commons.utils import JsCode
import os

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.realpath(__file__))

# 生成图表并保存到当前脚本所在的文件夹下
output_file = os.path.join(script_dir, "multiple_liquid.html")


l1 = (
    Liquid()
    .add("aaa", [0.6, 0.5, 0.4], center=["10%", "50%"])

)

l2 = Liquid().add(
    "bbb",
    [0.3254],
    center=["50%", "50%"],
    label_opts=opts.LabelOpts(
        font_size=50,
        formatter=JsCode(
            """function (param) {
                    return (Math.floor(param.value * 10000) / 100) + '%';
                }"""
        ),

    ),
)

l3 = (
    Liquid()
    .add("ccc", [0.5], center=["90%", "50%"])

)

# 修改 Grid 设置画布大小为 250px 宽和 780px 高
grid = Grid(init_opts=opts.InitOpts(width="660px", height="260px")).add(
    l1, grid_opts=opts.GridOpts(width="250px", height="780px")
).add(l2, grid_opts=opts.GridOpts(width="250px", height="780px")).add(l3, grid_opts=opts.GridOpts(width="250px", height="780px"))
grid.render(output_file)

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
            margin-left: 10px;  /* 将图表整体右移50px */
        }
    </style>
"""

# 将自定义 CSS 插入到 <head> 部分
html_content = html_content.replace('</head>', custom_css + '</head>')

# 重新写回修改后的 HTML 内容
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(html_content)