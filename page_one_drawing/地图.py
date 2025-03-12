from pyecharts import options as opts
from pyecharts.charts import Geo, HeatMap,Map, Grid
from pyecharts.globals import ChartType, SymbolType
import os

# 准备数据：湖北省各地市人口数据（随便给一个数据）
hubei_population = {
    "武汉市": 1121, "黄石市": 250, "十堰市": 350, "宜昌市": 400,
    "襄阳市": 470, "鄂州市": 200, "荆门市": 240, "孝感市": 220,
    "荆州市": 530, "黄冈市": 460, "咸宁市": 440, "随州市": 200,
    "恩施土家族苗族自治州": 250, "仙桃市": 180, "潜江市": 180, "天门市": 150,
    "神农架林区": 10
}

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.realpath(__file__))

# 生成图表并保存到当前脚本所在的文件夹下
output_file = os.path.join(script_dir, "map_hubei.html")

geo = (
    Geo()
    .add_schema(maptype="湖北",
                zoom=1.25  # 设置缩放级别，值越大越靠近，值越小越远
                )  # 使用湖北地图
    .add(
        "",
        [("武汉", 55), ("宜昌", 66), ("襄阳", 77), ("荆州", 88)],  # 湖北省城市
        type_=ChartType.EFFECT_SCATTER,
        color="white",
    )
    .add(
        "geo",
        [("武汉", "宜昌"), ("武汉", "襄阳"), ("武汉", "荆州"), ("襄阳", "荆州")],  # 连接湖北省内的城市
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(
            symbol=SymbolType.ARROW,  # 设置箭头的样式
            symbol_size=10,  # 增大箭头的大小
            color="yellow"  # 设置箭头的颜色为黄色，在深色背景下更明显
        ),
        linestyle_opts=opts.LineStyleOpts(
            color="yellow",  # 设置线条的颜色为黄色
            width=8,  # 增加线条宽度
            opacity=1,  # 设置线条的透明度
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
        list(hubei_population.items()),  # 添加市区及其人口数据
        "湖北",  # 使用湖北省地图
        zoom=1.25,# 设置缩放级别，值越大越靠近，值越小越远
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
            min_=100,  # 设置最小值
            max_=1200,  # 设置最大值
            is_piecewise=True,  # 设置分段
            pieces=[
                {"min": 1000, "color": "#2193b0"},  # 渐变色的起始色
                {"min": 500, "max": 999, "color": "#4d8cc7"},  # 中间过渡色
                {"min": 200, "max": 499, "color": "#72a4d3"},  # 中间过渡色
                {"min": 100, "max": 199, "color": "#94c1e2"},  # 中间过渡色
                {"max": 99, "color": "#6dd5ed"}  # 渐变色的结束色
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