import os
from pyecharts import options as opts
from pyecharts.charts import Pie

# 数据准备
energy_data = {
    "发电结构": [
        ("火电", 1560),
        ("风电", 780),
        ("太阳能", 650),
    ],
    "储能结构": [
        ("抽水蓄能", 420),
        ("电化学储能", 280),
        ("压缩空气储能", 180),
        ("氢储能", 120)
    ]
}

# color_scale = [
#     # 火电色系（暖色调渐变）
#     "#FF4444",  # 警示红（基础火电）
#     "#FF7F50",  # 珊瑚橙（过渡色）
#     "#FFA500",  # 琥珀色（辅助火电）

#     # 新能源色系（冷色调渐变）
#     "#00CED1",  # 深绿松石（风电）
#     "#20B2AA",  # 亮海蓝（过渡色）
#     "#98FB98",  # 薄荷绿（太阳能）

#     # 储能色系（科技紫+渐变）
#     "#9370DB",  # 中紫色（抽水蓄能）
#     "#BA55D3",  # 中等兰花紫（电化学）
#     "#DA70D6",  # 兰花紫（压缩空气）
#     "#FF69B4"   # 亮粉（氢储能）
# ]

# 生成图表
script_dir = os.path.dirname(os.path.realpath(__file__))
output_file = os.path.join(script_dir, "energy_structure.html")

c = (
    Pie(init_opts=opts.InitOpts(width="380px", height="310px"))
    .add(
        series_name="发电结构",
        data_pair=energy_data["发电结构"],
        radius=["20%", "35%"],
        center=["50%", "50%"],
        # color=color_scale[:3],
        label_opts=opts.LabelOpts(
            position="outside",
            formatter="{b}: {d}%",
            color="white",
            font_size=14
        )
    )
    .add(
        series_name="储能结构",
        data_pair=energy_data["储能结构"],
        radius=["45%", "60%"],
        center=["50%", "50%"],
        # color=color_scale[3:],
        label_opts=opts.LabelOpts(
            position="inside",
            formatter="{b}\n{d}%",
            color="white",
            font_size=12
        )
    )
    .set_global_opts(
        # title_opts=opts.TitleOpts(
        #     title="能源结构与储能分布",
        #     title_textstyle_opts=opts.TextStyleOpts(
        #         color="white",
        #         font_size=24,
        #         font_weight="bold"
        #     ),
        #     pos_left="center"
        # ),
        title_opts=opts.TitleOpts(is_show=False),   # 隐藏标题
        # legend_opts=opts.LegendOpts(
        #     type_="scroll",
        #     orient="vertical",
        #     pos_left="10%",
        #     pos_top="20%",
        #     textstyle_opts=opts.TextStyleOpts(color="white")
        # ),
        legend_opts = opts.LegendOpts(is_show=False),
        tooltip_opts=opts.TooltipOpts(
            trigger="item",
            formatter="{a} <br/>{b}: {c}万千瓦 ({d}%)"
        )
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
    
# # 添加自定义CSS样式
# with open(output_file, 'r', encoding='utf-8') as f:
#     content = f.read()

# custom_style = """
# <style>
# /* 全局重置 */
# * {
#     margin: 0;
#     padding: 0;
#     box-sizing: border-box;
# }

# /* 根容器设置 */
# html, body {
#     width: 100vw;   /* 视口宽度 */
#     height: 100vh;  /* 视口高度 */
#     overflow: hidden; /* 禁用滚动条 */
#     background: #001a33; /* 备用背景色 */
# }

# /* 主图表容器 */
# .chart-container {
#     position: absolute;
#     top: 10px;
#     right: 10px;
#     bottom: 10px;
#     left: 10px;
#     background: radial-gradient(circle at 50% 50%, 
#         rgba(0, 51, 102, 0.9) 0%, 
#         rgba(0, 26, 51, 0.95) 100%);
#     border-radius: 12px;
#     box-shadow: 0 0 20px rgba(0, 100, 255, 0.2);
#     border: 1px solid rgba(0, 150, 255, 0.15);
# }
# </style>
# """

# content = content.replace('</head>', f'{custom_style}</head>')
# content = content.replace('<div id="', '<div class="chart-container" style="padding:20px;"><div id="')
# content = content.replace('</body>', '</div></body>')

# with open(output_file, 'w', encoding='utf-8') as f:
#     f.write(content)