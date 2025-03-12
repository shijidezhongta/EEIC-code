import json
import numpy as np
import os
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Grid
def updata_total_plot():
    # 获取当前脚本所在的目录
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # 生成图表并保存到当前脚本所在的文件夹下
    output_total = os.path.join(script_dir, "total_plot.html")

    # 读取 JSON 文件中的数据
    with open("database.json", "r") as json_file:
        data = json.load(json_file)

    # 从数据库中读取数据
    Pmt = np.array(data.get("Pmt"))
    P_w = np.array(data.get("P_w"))
    P_pv = np.array(data.get("P_pv"))
    Pfc = np.array(data.get("Pfc"))
    Pfc = - Pfc
    Pel = np.array(data.get("Pel"))
    Pel = - Pel
    Pdis = np.array(data.get("Pdis"))
    Pdis = - Pdis
    Pcha = np.array(data.get("Pcha"))
    Pcha = - Pcha
    Pgen = np.array(data.get("Pgen"))
    Pgen = - Pgen
    Ppm = np.array(data.get("Ppm"))
    Ppm = - Ppm
    Pcaes_d = np.array(data.get("Pcaes_d"))
    Pcaes_d = - Pcaes_d
    Pcaes_g = np.array(data.get("Pcaes_g"))
    Pcaes_g = - Pcaes_g
    Load_real = np.array(data.get("Load_real"))

    # 定义 X 轴数据（假设为时间或其他分类变量）
    x_data = [str(i) for i in range(1, len(Pmt) + 1)]

    # 创建堆积柱状图
    bar = (
        Bar()
        .add_xaxis(x_data)  # 添加 X 轴数据
        .add_yaxis("Pmt", Pmt.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Pmt
        .add_yaxis("P_w", P_w.tolist(), stack="stack1")  # 添加 Y 轴数据系列 P_w
        .add_yaxis("P_pv", P_pv.tolist(), stack="stack1")  # 添加 Y 轴数据系列 P_pv
        .add_yaxis("Pfc", Pfc.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Pfc
        .add_yaxis("Pel", Pel.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Pel
        .add_yaxis("Pdis", Pdis.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Pdis
        .add_yaxis("Pcha", Pcha.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Pcha
        .add_yaxis("Pgen", Pgen.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Pgen
        .add_yaxis("Ppm", Ppm.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Ppm
        .add_yaxis("Pcaes_d", Pcaes_d.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Pcaes_d
        .add_yaxis("Pcaes_g", Pcaes_g.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Pcaes_g
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 隐藏数据标签
        .set_global_opts(
            title_opts=opts.TitleOpts(is_show=False),  # 隐藏标题
            legend_opts=opts.LegendOpts(is_show=False),  # 隐藏图例
            yaxis_opts=opts.AxisOpts(
                min_=-200,  # 设置 Y 轴最小值
                max_=500,  # 设置 Y 轴最大值
                interval=50,  # 设置 Y 轴刻度间隔
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#CCEDFF")  # 设置 Y 轴线条颜色为白色
                ),
                axislabel_opts=opts.LabelOpts(color="#CCEDFF"),  # 设置 Y 轴标签颜色为白色
                splitline_opts=opts.SplitLineOpts(
                    is_show=True,
                    linestyle_opts=opts.LineStyleOpts(
                        color="#CCEDFF",
                        opacity=0.2,  # 设置网格线透明度为 0.2
                    )
                ),
            ),
            xaxis_opts=opts.AxisOpts(
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#CCEDFF")  # 设置 X 轴线条颜色为白色
                ),
                axislabel_opts=opts.LabelOpts(color="#CCEDFF"),  # 设置 X 轴标签颜色为白色
                splitline_opts=opts.SplitLineOpts(
                    is_show=False  # 隐藏 X 轴网格线
                ),
            ),
        )
    )

    # 创建折线图，并将其样式与柱状图保持一致
    line = (
        Line()
        .add_xaxis(x_data)  # 使用相同的 X 轴数据
        .add_yaxis(
            "负荷量",
            Load_real.tolist(),
            is_smooth=True,
            z_level = 2,
            color="#E12F13",  # 使用与柱状图一致的颜色
        )  # 添加负荷量折线图
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 隐藏数据标签
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                min_=-200,  # 设置 Y 轴最小值，与柱状图一致
                max_=500,  # 设置 Y 轴最大值，与柱状图一致
                interval=50,  # 设置 Y 轴刻度间隔，与柱状图一致
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#CCEDFF")  # 设置 Y 轴线条颜色为白色
                ),
                axislabel_opts=opts.LabelOpts(color="#CCEDFF"),  # 设置 Y 轴标签颜色为白色
                splitline_opts=opts.SplitLineOpts(
                    is_show=True,
                    linestyle_opts=opts.LineStyleOpts(
                        color="#CCEDFF",
                        opacity=0.2,  # 设置网格线透明度为 0.2
                    )
                ),
            ),
            xaxis_opts=opts.AxisOpts(
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#CCEDFF")  # 设置 X 轴线条颜色为白色
                ),
                axislabel_opts=opts.LabelOpts(color="#CCEDFF"),  # 设置 X 轴标签颜色为白色
                splitline_opts=opts.SplitLineOpts(
                    is_show=False  # 隐藏 X 轴网格线
                ),
            ),
            legend_opts=opts.LegendOpts(is_show=False),  # 隐藏图例
        )
    )

    # 使用 Grid 将两个图表叠加
    grid = (
        Grid(init_opts=opts.InitOpts(width="1180px", height="820px"))
        .add(line, grid_opts=opts.GridOpts())  # 添加折线图
        .add(bar, grid_opts=opts.GridOpts())  # 添加堆积柱状图
    )

    # 渲染图表并保存为 HTML 文件
    grid.render(output_total)

    # 读取生成的 HTML 文件
    with open(output_total, 'r', encoding='utf-8') as file:
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
                background: #002D4A;  # 设置背景颜色为深蓝色
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
    with open(output_total, 'w', encoding='utf-8') as file:
        file.write(html_content)
