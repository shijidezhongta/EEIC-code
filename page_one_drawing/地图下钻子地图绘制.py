from pyecharts import options as opts
from pyecharts.charts import Geo, HeatMap, Map, Grid
from pyecharts.globals import ChartType, SymbolType
import os

# 准备数据：武汉市各区人口数据（随便给一个数据）
wuhan_population = {
    "江岸区": 100, "江汉区": 120, "硚口区": 110, "汉阳区": 130,
    "武昌区": 150, "青山区": 90, "洪山区": 160, "东西湖区": 80,
    "汉南区": 30, "蔡甸区": 70, "江夏区": 100, "黄陂区": 120,
    "新洲区": 90
}

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.realpath(__file__))

# 生成图表并保存到当前脚本所在的文件夹下
output_file = os.path.join(script_dir, "map_wuhan.html")

geo = (
    Geo()
    .add_schema(maptype="武汉",
                zoom=1.25  # 设置缩放级别，值越大越靠近，值越小越远
                )  # 使用武汉地图
    .add(
        "",
        [("江岸区", 55), ("武昌区", 66), ("洪山区", 77), ("汉阳区", 88)],  # 武汉市各区
        type_=ChartType.EFFECT_SCATTER,
        color="white",
    )
    .add(
        "geo",
        [("江岸区", "武昌区"), ("江岸区", "洪山区"), ("江岸区", "汉阳区"), ("洪山区", "汉阳区")],  # 连接武汉市内的区
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(
            symbol=SymbolType.ARROW,  # 设置箭头的样式
            symbol_size=6,  # 设置箭头的大小
            color="blue"  # 设置箭头的颜色为蓝色
        ),
        linestyle_opts=opts.LineStyleOpts(
            color="blue",  # 设置线条的颜色为蓝色
            width=5,  # 设置线条宽度
            curve=0.2,  # 设置线条的弯曲程度
        ),
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 隐藏标签
    .set_global_opts(
        legend_opts=opts.LegendOpts(is_show=False)  # 隐藏图例
    )
)

# 创建 HeatMap 热力图
heatmap = (
    Map()
    # 添加数据到地图
    .add(
        "人口数",
        list(wuhan_population.items()),  # 添加市区及其人口数据
        "武汉",  # 使用武汉市地图
        zoom=1.25,  # 设置缩放级别，值越大越靠近，值越小越远
        label_opts=opts.LabelOpts(
            is_show=True,  # 显示标签
            position="top",  # 将标签置于上方
            font_size=12,  # 设置字体大小
            color="#FFFFFF",  # 设置标签颜色为白色
            font_weight="bold"  # 设置标签字体加粗
        )
    )

    # 设置全局配置（标题等）
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            min_=30,  # 设置最小值
            max_=160,  # 设置最大值
            is_piecewise=True,  # 设置分段
            pieces=[
                {"min": 150, "color": "#2193b0"},  # 渐变色的起始色
                {"min": 100, "max": 149, "color": "#4d8cc7"},  # 中间过渡色
                {"min": 70, "max": 99, "color": "#72a4d3"},  # 中间过渡色
                {"min": 40, "max": 69, "color": "#94c1e2"},  # 中间过渡色
                {"max": 39, "color": "#6dd5ed"}  # 渐变色的结束色
            ],
            is_show=False  # 隐藏图例
        ),
        legend_opts=opts.LegendOpts(is_show=False),  # 去掉图例
    )
)

# 使用 Grid 叠加两个图表
grid = (
    Grid(init_opts=opts.InitOpts(width="1380px", height="780px"))
    .add(heatmap, grid_opts=opts.GridOpts())  # 添加 HeatMap 热力图
    .add(geo, grid_opts=opts.GridOpts())  # 添加 Geo 迁徙流动图
)

grid.render(output_file)

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
            width: 1300px;    /* 使图表宽度占据父容器的100% */
            height: 800px;   /* 使图表高度占据父容器的100% */
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


# 准备数据：宜昌市各区县人口数据（随机示例）
yichang_population = {
    "西陵区": 50, "伍家岗区": 40, "点军区": 20, "猇亭区": 15,
    "夷陵区": 60, "宜都市": 35, "当阳市": 45, "枝江市": 38,
    "远安县": 12, "兴山县": 10, "秭归县": 18, "长阳土家族自治县": 16,
    "五峰土家族自治县": 8
}

# 生成图表并保存到当前脚本所在的文件夹下
output_file = os.path.join(script_dir, "map_yichang.html")

geo = (
    Geo()
    .add_schema(maptype="宜昌",
                zoom=1.25  # 设置缩放级别，值越大越靠近，值越小越远
                )  # 使用宜昌地图
    .add(
        "",
        [("西陵区", 25), ("伍家岗区", 30), ("夷陵区", 35), ("宜都市", 20)],  # 宜昌市各区县
        type_=ChartType.EFFECT_SCATTER,
        color="white",
    )
    .add(
        "geo",
        [("西陵区", "伍家岗区"), ("西陵区", "夷陵区"), ("西陵区", "宜都市"), ("夷陵区", "宜都市")],  # 连接宜昌市内的区县
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(
            symbol=SymbolType.ARROW,  # 设置箭头的样式
            symbol_size=6,  # 设置箭头的大小
            color="blue"  # 设置箭头的颜色为蓝色
        ),
        linestyle_opts=opts.LineStyleOpts(
            color="blue",  # 设置线条的颜色为蓝色
            width=5,  # 设置线条宽度
            curve=0.2,  # 设置线条的弯曲程度
        ),
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 隐藏标签
    .set_global_opts(
        legend_opts=opts.LegendOpts(is_show=False)  # 隐藏图例
    )
)

# 创建 HeatMap 热力图
heatmap = (
    Map()
    # 添加数据到地图
    .add(
        "人口数",
        list(yichang_population.items()),  # 添加区县及其人口数据
        "宜昌",  # 使用宜昌市地图
        zoom=1.25,  # 设置缩放级别，值越大越靠近，值越小越远
        label_opts=opts.LabelOpts(
            is_show=True,  # 显示标签
            position="top",  # 将标签置于上方
            font_size=12,  # 设置字体大小
            color="#FFFFFF",  # 设置标签颜色为白色
            font_weight="bold"  # 设置标签字体加粗
        )
    )

    # 设置全局配置（标题等）
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            min_=8,  # 设置最小值
            max_=60,  # 设置最大值
            is_piecewise=True,  # 设置分段
            pieces=[
                {"min": 50, "color": "#2193b0"},  # 渐变色的起始色
                {"min": 30, "max": 49, "color": "#4d8cc7"},  # 中间过渡色
                {"min": 20, "max": 29, "color": "#72a4d3"},  # 中间过渡色
                {"min": 10, "max": 19, "color": "#94c1e2"},  # 中间过渡色
                {"max": 9, "color": "#6dd5ed"}  # 渐变色的结束色
            ],
            is_show=False  # 隐藏图例
        ),
        legend_opts=opts.LegendOpts(is_show=False),  # 去掉图例
    )
)

# 使用 Grid 叠加两个图表
grid = (
    Grid(init_opts=opts.InitOpts(width="1380px", height="780px"))
    .add(heatmap, grid_opts=opts.GridOpts())  # 添加 HeatMap 热力图
    .add(geo, grid_opts=opts.GridOpts())  # 添加 Geo 迁徙流动图
)

grid.render(output_file)

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
            width: 1300px;    /* 使图表宽度占据父容器的100% */
            height: 800px;   /* 使图表高度占据父容器的100% */
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