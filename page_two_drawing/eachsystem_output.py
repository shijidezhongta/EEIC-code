import json
import numpy as np
import os
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Grid
def updata_four_plot():
    # 获取当前脚本所在的目录
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # 生成图表并保存到当前脚本所在的文件夹下
    output_Ppm = os.path.join(script_dir, "Ppm.html")
    output_CAES = os.path.join(script_dir, "CAES.html")
    output_H2 = os.path.join(script_dir, "H2.html")
    output_bat1 = os.path.join(script_dir, "bat1.html")
    output_bat2 = os.path.join(script_dir, "bat2.html")
    output_pw1 = os.path.join(script_dir, "w1.html")
    output_pw2 = os.path.join(script_dir, "w2.html")
    output_pw3 = os.path.join(script_dir, "w3.html")
    output_pv1 = os.path.join(script_dir, "pv1.html")
    output_pv2 = os.path.join(script_dir, "pv2.html")
    output_Ppm_zero = os.path.join(script_dir, "Ppm_zero.html")
    output_CAES_zero = os.path.join(script_dir, "CAES_zero.html")
    output_H2_zero = os.path.join(script_dir, "H2_zero.html")
    output_bat_zero = os.path.join(script_dir, "bat_zero.html")
    output_pw_zero = os.path.join(script_dir, "w_zero.html")
    output_pv_zero = os.path.join(script_dir, "pv_zero.html")
    # --------------------------------------------读取数据---------------------------------- #   
    # # 读取 JSON 文件中的数据
    with open("database.json", "r") as json_file:
        data = json.load(json_file)

    # 从数据库中读取数据
    P_w = np.array(data.get("P_w"))
    P_pv = np.array(data.get("P_pv"))
    Pfc = np.array(data.get("Pfc"))
    Pel = np.array(data.get("Pel"))
    Pdis = np.array(data.get("Pdis"))
    Pcha = np.array(data.get("Pcha"))
    Pgen = np.array(data.get("Pgen"))
    Ppm = np.array(data.get("Ppm"))
    Pcaes_d = np.array(data.get("Pcaes_d"))
    Pcaes_g = np.array(data.get("Pcaes_g"))

    #----------------------抽水蓄能---------------------#
    # 自定义数据
    x_data = [str(i) for i in range(1, 25)]  # 生成1到24的字符串列表
    zerodata = np.zeros(24)
    Total_Ppm = - Ppm - Pgen
    # 使用 InitOpts 来设置宽度和高度
    c = (
        Line(init_opts=opts.InitOpts(width="385px", height="355px"))  # 设置图表的宽高    
        .add_xaxis(x_data)  # 使用自定义的X轴数据
        .add_yaxis(
            "抽水蓄能出力情况", 
            Total_Ppm, 
            is_smooth=True, 
            color="#8ECDEC",  # 设置折线图颜色为鲜明的橙色，适合深色背景
        )  
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(color="#8ECDEC", opacity=0.2),  # 设置曲线下方阴影的颜色和透明度
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
                        opacity=0.2,  # 网格线透明度
                    )
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                min_=-100,  # 设置 Y 轴最小值
                max_=150,   # 设置 Y 轴最大值
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
        .render(output_Ppm)  # 渲染并保存为 HTML 文件
    )

    # 读取生成的 HTML 文件
    with open(output_Ppm, 'r', encoding='utf-8') as file:
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
    with open(output_Ppm, 'w', encoding='utf-8') as file:
        file.write(html_content)

    #----------------------氢储能---------------------#
    Total_H2 = - Pel - Pfc
    # 使用 InitOpts 来设置宽度和高度
    c = (
        Line(init_opts=opts.InitOpts(width="385px", height="355px"))  # 设置图表的宽高    
        .add_xaxis(x_data)  # 使用自定义的X轴数据
        .add_yaxis(
            "氢储能出力情况", 
            Total_H2, 
            is_smooth=True, 
            color="#8ECDEC",  # 设置折线图颜色为鲜明的橙色，适合深色背景
        )  
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(color="#8ECDEC", opacity=0.2),  # 设置曲线下方阴影的颜色和透明度
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
                        opacity=0.2,  # 网格线透明度
                    )
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                min_=-100,  # 设置 Y 轴最小值
                max_=150,   # 设置 Y 轴最大值
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
        .render(output_H2)  # 渲染并保存为 HTML 文件
    )

    # 读取生成的 HTML 文件
    with open(output_H2, 'r', encoding='utf-8') as file:
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
    with open(output_H2, 'w', encoding='utf-8') as file:
        file.write(html_content)

    #----------------------电化学储能——模块1 ---------------------#
    # 生成图表并保存到当前脚本所在的文件夹下
    Total_bat1 = - Pdis[0] - Pcha[0] 
    # 使用 InitOpts 来设置宽度和高度
    c = (
        Line(init_opts=opts.InitOpts(width="385px", height="355px"))  # 设置图表的宽高    
        .add_xaxis(x_data)  # 使用自定义的X轴数据
        .add_yaxis(
            "电化学储能出力情况", 
            Total_bat1, 
            is_smooth=True, 
            color="#8ECDEC",  # 设置折线图颜色为鲜明的橙色，适合深色背景
        )  
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(color="#8ECDEC", opacity=0.2),  # 设置曲线下方阴影的颜色和透明度
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
                        opacity=0.2,  # 网格线透明度
                    )
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                min_=-100,  # 设置 Y 轴最小值
                max_=150,   # 设置 Y 轴最大值
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
        .render(output_bat1)  # 渲染并保存为 HTML 文件
    )

    # 读取生成的 HTML 文件
    with open(output_bat1, 'r', encoding='utf-8') as file:
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
    with open(output_bat1, 'w', encoding='utf-8') as file:
        file.write(html_content)

    #----------------------电化学储能——模块2---------------------#
    # 生成图表并保存到当前脚本所在的文件夹下
    Total_bat2 = - Pdis[1] - Pcha[1] 
    # 使用 InitOpts 来设置宽度和高度
    c = (
        Line(init_opts=opts.InitOpts(width="385px", height="355px"))  # 设置图表的宽高    
        .add_xaxis(x_data)  # 使用自定义的X轴数据
        .add_yaxis(
            "电化学储能出力情况", 
            Total_bat2, 
            is_smooth=True, 
            color="#8ECDEC",  # 设置折线图颜色为鲜明的橙色，适合深色背景
        )  
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(color="#8ECDEC", opacity=0.2),  # 设置曲线下方阴影的颜色和透明度
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
                        opacity=0.2,  # 网格线透明度
                    )
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                min_=-100,  # 设置 Y 轴最小值
                max_=150,   # 设置 Y 轴最大值
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
        .render(output_bat2)  # 渲染并保存为 HTML 文件
    )

    # 读取生成的 HTML 文件
    with open(output_bat2, 'r', encoding='utf-8') as file:
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
    with open(output_bat2, 'w', encoding='utf-8') as file:
        file.write(html_content)

    #----------------------压缩空气储能---------------------#
    Total_CAES = - Pcaes_d - Pcaes_g
    # 使用 InitOpts 来设置宽度和高度
    c = (
        Line(init_opts=opts.InitOpts(width="385px", height="355px"))  # 设置图表的宽高    
        .add_xaxis(x_data)  # 使用自定义的X轴数据
        .add_yaxis(
            "压缩空气储能出力情况", 
            Total_CAES, 
            is_smooth=True, 
            color="#8ECDEC",  # 设置折线图颜色为鲜明的橙色，适合深色背景
        )  
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(color="#8ECDEC", opacity=0.2),  # 设置曲线下方阴影的颜色和透明度
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
                        opacity=0.2,  # 网格线透明度
                    )
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                min_=-100,  # 设置 Y 轴最小值
                max_=150,   # 设置 Y 轴最大值
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
        .render(output_CAES)  # 渲染并保存为 HTML 文件
    )

    # 读取生成的 HTML 文件
    with open(output_CAES, 'r', encoding='utf-8') as file:
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
    with open(output_CAES, 'w', encoding='utf-8') as file:
        file.write(html_content)

    #----------------------光伏---------------------#
    for k in range(2):
        # 使用 InitOpts 来设置宽度和高度
        c = (
            Line(init_opts=opts.InitOpts(width="385px", height="355px"))  # 设置图表的宽高    
            .add_xaxis(x_data)  # 使用自定义的X轴数据
            .add_yaxis(
                "光伏出力情况", 
                P_pv[k], 
                is_smooth=True, 
                color="#8ECDEC",  # 设置折线图颜色为鲜明的橙色，适合深色背景
            )  
            .set_series_opts(
                areastyle_opts=opts.AreaStyleOpts(color="#8ECDEC", opacity=0.2),  # 设置曲线下方阴影的颜色和透明度
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
                            opacity=0.2,  # 网格线透明度
                        )
                    ),
                ),
                yaxis_opts=opts.AxisOpts(
                    min_=-50,  # 设置 Y 轴最小值
                    max_=400,   # 设置 Y 轴最大值
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
        )
        if k == 0:
            c.render(output_pv1)  # 渲染并保存为 HTML 文件
        else:
            c.render(output_pv2)  # 渲染并保存为 HTML 文件


        if k == 0:
            # 读取生成的 HTML 文件
            with open(output_pv1, 'r', encoding='utf-8') as file:
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
            with open(output_pv1, 'w', encoding='utf-8') as file:
                file.write(html_content)
        else:
            # 读取生成的 HTML 文件
            with open(output_pv2, 'r', encoding='utf-8') as file:
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
            with open(output_pv2, 'w', encoding='utf-8') as file:
                file.write(html_content)            

    #----------------------风电---------------------#
    for k in range(3):
        c = (
            Line(init_opts=opts.InitOpts(width="385px", height="355px"))  # 设置图表的宽高    
            .add_xaxis(x_data)  # 使用自定义的X轴数据
            .add_yaxis(
                "风电出力情况", 
                P_w[k], 
                is_smooth=True, 
                color="#8ECDEC",  # 设置折线图颜色为鲜明的橙色，适合深色背景
            )  
            .set_series_opts(
                areastyle_opts=opts.AreaStyleOpts(color="#8ECDEC", opacity=0.2),  # 设置曲线下方阴影的颜色和透明度
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
                            opacity=0.2,  # 网格线透明度
                        )
                    ),
                ),
                yaxis_opts=opts.AxisOpts(
                    min_=-50,  # 设置 Y 轴最小值
                    max_=300,   # 设置 Y 轴最大值
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
        )
        if k ==0:
            c.render(output_pw1)  # 渲染并保存为 HTML 文件
            # 读取生成的 HTML 文件
            with open(output_pw1, 'r', encoding='utf-8') as file:
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
            with open(output_pw1, 'w', encoding='utf-8') as file:
                file.write(html_content)
        elif k == 1:
            c.render(output_pw2)  # 渲染并保存为 HTML 文件  
            # 读取生成的 HTML 文件
            with open(output_pw2, 'r', encoding='utf-8') as file:
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
            with open(output_pw2, 'w', encoding='utf-8') as file:
                file.write(html_content)
        else:
            c.render(output_pw3)  # 渲染并保存为 HTML 文件
            # 读取生成的 HTML 文件
            with open(output_pw3, 'r', encoding='utf-8') as file:
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
            with open(output_pw3, 'w', encoding='utf-8') as file:
                file.write(html_content)

#-----------------------------------------绘制零数据图---------------------------------------------------------------#
# 使用 InitOpts 来设置宽度和高度
    c = (
        Line(init_opts=opts.InitOpts(width="385px", height="355px"))  # 设置图表的宽高    
        .add_xaxis(x_data)  # 使用自定义的X轴数据
        .add_yaxis(
            "抽水蓄能出力情况", 
            zerodata, 
            is_smooth=True, 
            color="#8ECDEC",  # 设置折线图颜色为鲜明的橙色，适合深色背景
        )  
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(color="#8ECDEC", opacity=0.2),  # 设置曲线下方阴影的颜色和透明度
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
                        opacity=0.2,  # 网格线透明度
                    )
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                min_=-100,  # 设置 Y 轴最小值
                max_=150,   # 设置 Y 轴最大值
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
        .render(output_Ppm_zero)  # 渲染并保存为 HTML 文件
    )

    # 读取生成的 HTML 文件
    with open(output_Ppm_zero, 'r', encoding='utf-8') as file:
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
    with open(output_Ppm_zero, 'w', encoding='utf-8') as file:
        file.write(html_content)

    #----------------------氢储能---------------------#
    Total_H2 = - Pel - Pfc
    # 使用 InitOpts 来设置宽度和高度
    c = (
        Line(init_opts=opts.InitOpts(width="385px", height="355px"))  # 设置图表的宽高    
        .add_xaxis(x_data)  # 使用自定义的X轴数据
        .add_yaxis(
            "氢储能出力情况", 
            zerodata, 
            is_smooth=True, 
            color="#8ECDEC",  # 设置折线图颜色为鲜明的橙色，适合深色背景
        )  
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(color="#8ECDEC", opacity=0.2),  # 设置曲线下方阴影的颜色和透明度
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
                        opacity=0.2,  # 网格线透明度
                    )
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                min_=-100,  # 设置 Y 轴最小值
                max_=150,   # 设置 Y 轴最大值
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
        .render(output_H2_zero)  # 渲染并保存为 HTML 文件
    )

    # 读取生成的 HTML 文件
    with open(output_H2_zero, 'r', encoding='utf-8') as file:
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
    with open(output_H2_zero, 'w', encoding='utf-8') as file:
        file.write(html_content)

    #----------------------电化学储能——模块1 ---------------------#
    # 生成图表并保存到当前脚本所在的文件夹下
    # 使用 InitOpts 来设置宽度和高度
    c = (
        Line(init_opts=opts.InitOpts(width="385px", height="355px"))  # 设置图表的宽高    
        .add_xaxis(x_data)  # 使用自定义的X轴数据
        .add_yaxis(
            "电化学储能出力情况", 
            zerodata, 
            is_smooth=True, 
            color="#8ECDEC",  # 设置折线图颜色为鲜明的橙色，适合深色背景
        )  
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(color="#8ECDEC", opacity=0.2),  # 设置曲线下方阴影的颜色和透明度
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
                        opacity=0.2,  # 网格线透明度
                    )
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                min_=-100,  # 设置 Y 轴最小值
                max_=150,   # 设置 Y 轴最大值
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
        .render(output_bat_zero)  # 渲染并保存为 HTML 文件
    )

    # 读取生成的 HTML 文件
    with open(output_bat_zero, 'r', encoding='utf-8') as file:
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
    with open(output_bat_zero, 'w', encoding='utf-8') as file:
        file.write(html_content)

    #----------------------压缩空气储能---------------------#
    # 使用 InitOpts 来设置宽度和高度
    c = (
        Line(init_opts=opts.InitOpts(width="385px", height="355px"))  # 设置图表的宽高    
        .add_xaxis(x_data)  # 使用自定义的X轴数据
        .add_yaxis(
            "压缩空气储能出力情况", 
            zerodata, 
            is_smooth=True, 
            color="#8ECDEC",  # 设置折线图颜色为鲜明的橙色，适合深色背景
        )  
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(color="#8ECDEC", opacity=0.2),  # 设置曲线下方阴影的颜色和透明度
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
                        opacity=0.2,  # 网格线透明度
                    )
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                min_=-100,  # 设置 Y 轴最小值
                max_=150,   # 设置 Y 轴最大值
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
        .render(output_CAES_zero)  # 渲染并保存为 HTML 文件
    )

    # 读取生成的 HTML 文件
    with open(output_CAES_zero, 'r', encoding='utf-8') as file:
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
    with open(output_CAES_zero, 'w', encoding='utf-8') as file:
        file.write(html_content)
#-------------------------风电与光伏---------------------#
    c = (
        Line(init_opts=opts.InitOpts(width="385px", height="355px"))  # 设置图表的宽高    
        .add_xaxis(x_data)  # 使用自定义的X轴数据
        .add_yaxis(
            "光伏出力情况", 
            zerodata, 
            is_smooth=True, 
            color="#8ECDEC",  # 设置折线图颜色为鲜明的橙色，适合深色背景
        )  
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(color="#8ECDEC", opacity=0.2),  # 设置曲线下方阴影的颜色和透明度
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
                        opacity=0.2,  # 网格线透明度
                    )
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                min_=-50,  # 设置 Y 轴最小值
                max_=400,   # 设置 Y 轴最大值
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
        .render(output_pv_zero)  # 渲染并保存为 HTML 文件
    )

    # 读取生成的 HTML 文件
    with open(output_pv_zero, 'r', encoding='utf-8') as file:
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
    with open(output_pv_zero, 'w', encoding='utf-8') as file:
        file.write(html_content)
#-------------------------风电---------------------#       
    c = (
        Line(init_opts=opts.InitOpts(width="385px", height="355px"))  # 设置图表的宽高    
        .add_xaxis(x_data)  # 使用自定义的X轴数据
        .add_yaxis(
            "风电出力情况", 
            zerodata, 
            is_smooth=True, 
            color="#8ECDEC",  # 设置折线图颜色为鲜明的橙色，适合深色背景
        )  
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(color="#8ECDEC", opacity=0.2),  # 设置曲线下方阴影的颜色和透明度
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
                        opacity=0.2,  # 网格线透明度
                    )
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                min_=-50,  # 设置 Y 轴最小值
                max_=300,   # 设置 Y 轴最大值
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
        .render(output_pw_zero)  # 渲染并保存为 HTML 文件
    )

    # 读取生成的 HTML 文件
    with open(output_pw_zero, 'r', encoding='utf-8') as file:
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
    with open(output_pw_zero, 'w', encoding='utf-8') as file:
        file.write(html_content)
