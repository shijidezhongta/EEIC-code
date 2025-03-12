from pyecharts import options as opts
from pyecharts.charts import Sankey
import os

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.realpath(__file__))

# 生成图表并保存到当前脚本所在的文件夹下
output_file = os.path.join(script_dir, "sankey_vertical.html")

colors = [
    "#f12711",  # 起始颜色：鲜红色
    "#f33714",  # 渐变中间色：稍微偏橙的红色
    "#f54717",  # 渐变中间色：橙色
    "#f7571a",  # 渐变中间色：金橙色
    "#f8671d",  # 渐变中间色：金黄色
    "#f97720",  # 渐变中间色：黄色
    "#f98723",  # 渐变中间色：金黄色
    "#f99726",  # 渐变中间色：明亮的黄色
    "#fba429",  # 渐变中间色：深黄色
    "#f5af19",  # 终止颜色：金黄色
    "#f9b227",  # 新增颜色：黄色偏红
    "#f2a520",  # 新增颜色：橙色
    "#f3801c",  # 新增颜色：明亮的红橙色
    "#f16c17",  # 新增颜色：深红色
    "#e14c10",  # 新增颜色：暗红色
    "#d2360e",  # 新增颜色：深橙色
    "#c2210a",  # 新增颜色：火红色
    "#b21207",  # 新增颜色：鲜红色
    "#a00a04",  # 新增颜色：鲜艳红色
    "#8e0803",  # 新增颜色：红色
]


# 定义节点，节点之间的关系通过 links 连接
nodes = [
    {"name": "武汉"},  
    {"name": "黄石"},   
    {"name": "荆门"}, 
    {"name": "宜昌"},  
    {"name": "襄阳"},   
    {"name": "鄂州"}, 
    {"name":"十堰"} , 
]

# 定义节点之间的链接关系及其对应的值
links = [
    {"source": "武汉", "target": "荆门", "value": 5},   
    {"source": "鄂州", "target": "黄石", "value": 3},   
    {"source": "武汉", "target": "宜昌", "value": 3},  
    {"source": "宜昌", "target": "荆门", "value": 1},  
    {"source": "宜昌", "target": "襄阳", "value": 2},  
    {"source": "黄石", "target": "襄阳", "value": 1},   
    {"source": "鄂州", "target": "襄阳", "value": 2},   
    {"source": "十堰", "target": "襄阳", "value": 3},  
    {"source": "十堰", "target": "黄石", "value": 1},  
]



# 创建 Sankey 图表
c = (
    Sankey(init_opts=opts.InitOpts(width="780px", height="300px"))  # 创建 Sankey 图
    .set_colors(colors)  # 设置节点颜色
    .add(
        "sankey",  # 设置图表名称
        nodes=nodes,  # 节点数据
        links=links,  # 链接数据
        pos_bottom="5%",  # 设置图表的位置偏移
        orient="vertical",  # 设置为垂直方向
        linestyle_opt=opts.LineStyleOpts(opacity=0.2, curve=0.5, color="source"),  # 设置连接线样式
        label_opts=opts.LabelOpts(
            position="top",  # 设置标签位置
            color="#1E90FF",  # 设置标签字体颜色为亮蓝色
            font_size=14,  # 设置标签字体大小
            font_weight="bold" , # 设置标签字体加粗
        ),
    )
    .set_global_opts(
        legend_opts=opts.LegendOpts(is_show=False)  # 隐藏图例
    )
    .render(output_file)  # 渲染并保存图表为 HTML 文件
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
        #main {
            width: 0px;    /* 使图表宽度占据父容器的100% */
            height: 0px;   /* 使图表高度占据父容器的100% */
            margin: 0;      /* 去掉默认的空白 */
            padding: 0;     /* 去掉默认的内边距 */
        }
    </style>
"""

# 将自定义 CSS 插入到 <head> 部分
html_content = html_content.replace('</head>', custom_css + '</head>')

# 重新写回修改后的 HTML 内容
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(html_content)