import pyecharts.options as opts
from pyecharts.charts import Line
import os
import json
import numpy as np
from pyecharts.globals import JsCode
def updata_four_plot():
    #----------------------数据读取---------------------#
    # 读取 JSON 文件中的数据
    with open("database.json", "r") as json_file:
        data = json.load(json_file)
    P_w = np.array(data.get("P_w"))
    P_pv = np.array(data.get("P_pv"))
    Pfc = np.array(data.get("Pfc"))
    # 从数据库中读取数据  
    Pgen = data.get("Pgen")
    Ppm = data.get("Ppm")
    Ppm = np.array(Ppm)
    Pgen = np.array(Pgen) 
    Total_Ppm = - Ppm - Pgen

    Pcaes_d = data.get("Pcaes_d") 
    Pcaes_g = data.get("Pcaes_g")
    Pcaes_d = np.array(Pcaes_d)     
    Pcaes_g = np.array(Pcaes_g)
    Total_CAES = - Pcaes_d - Pcaes_g

    Pfc = data.get("Pfc")  
    Pel = data.get("Pel")
    Pfc = np.array(Pfc)
    Pel = np.array(Pel) 
    Total_H2 = - Pfc - Pel

    Pdis = data.get("Pdis")     
    Pcha = data.get("Pcha")  
    Pdis = np.array(Pdis)
    Pcha = np.array(Pcha)
    Total_bat = - Pdis - Pcha

    # 获取当前脚本所在的目录
    script_dir = os.path.dirname(os.path.realpath(__file__))

    #----------------------抽水蓄能---------------------#
    # 自定义数据
    x_data = [str(i) for i in range(1, 25)]  # 生成1到24的字符串列表

    # 生成图表并保存到当前脚本所在的文件夹下
    output_Ppm = os.path.join(script_dir, "Ppm_plot.html")

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

    # 生成图表并保存到当前脚本所在的文件夹下
    output_H2 = os.path.join(script_dir, "H2_plot.html")

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

    #----------------------电化学储能---------------------#
    # 生成图表并保存到当前脚本所在的文件夹下
    output_bat = os.path.join(script_dir, "bat_plot.html")

    # 使用 InitOpts 来设置宽度和高度
    c = (
        Line(init_opts=opts.InitOpts(width="385px", height="355px"))  # 设置图表的宽高    
        .add_xaxis(x_data)  # 使用自定义的X轴数据
        .add_yaxis(
            "电化学储能出力情况", 
            Total_bat, 
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
        .render(output_bat)  # 渲染并保存为 HTML 文件
    )

    # 读取生成的 HTML 文件
    with open(output_bat, 'r', encoding='utf-8') as file:
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
    with open(output_bat, 'w', encoding='utf-8') as file:
        file.write(html_content)

    #----------------------压缩空气储能---------------------#

    # 生成图表并保存到当前脚本所在的文件夹下
    output_CAES = os.path.join(script_dir, "CAES_plot.html")

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

    # 生成图表并保存到当前脚本所在的文件夹下
    output_pv = os.path.join(script_dir, "Ppv_plot.html")

    # 使用 InitOpts 来设置宽度和高度
    c = (
        Line(init_opts=opts.InitOpts(width="385px", height="355px"))  # 设置图表的宽高    
        .add_xaxis(x_data)  # 使用自定义的X轴数据
        .add_yaxis(
            "光伏出力情况", 
            P_pv, 
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
        .render(output_pv)  # 渲染并保存为 HTML 文件
    )

    # 读取生成的 HTML 文件
    with open(output_pv, 'r', encoding='utf-8') as file:
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
    with open(output_pv, 'w', encoding='utf-8') as file:
        file.write(html_content)

    #----------------------风电---------------------#

    # 生成图表并保存到当前脚本所在的文件夹下
    output_w = os.path.join(script_dir, "Pw_plot.html")

    # 使用 InitOpts 来设置宽度和高度
    c = (
        Line(init_opts=opts.InitOpts(width="385px", height="355px"))  # 设置图表的宽高    
        .add_xaxis(x_data)  # 使用自定义的X轴数据
        .add_yaxis(
            "风电出力情况", 
            P_w, 
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
        .render(output_w)  # 渲染并保存为 HTML 文件
    )

    # 读取生成的 HTML 文件
    with open(output_w, 'r', encoding='utf-8') as file:
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
    with open(output_w, 'w', encoding='utf-8') as file:
        file.write(html_content)