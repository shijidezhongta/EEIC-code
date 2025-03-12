from pyecharts import options as opts
from pyecharts.charts import WordCloud
import os

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.realpath(__file__))

# 生成图表并保存到当前脚本所在的文件夹下
output_file = os.path.join(script_dir, "word_cloud.html")

data = [
    ("电力系统", 100),
    ("配电网", 90),
    ("电网", 85),
    ("输电网", 80),
    ("负荷", 75),
    ("发电", 70),
    ("智能电网", 65),
    ("电力调度", 60),
    ("可再生能源", 55),
    ("储能", 50),
    ("风力发电", 45),
    ("光伏", 40),
    ("电气工程", 35),
    ("电力市场", 30),
    ("电力安全", 25),
    ("电网优化", 20),
    ("需求响应", 15),
    ("电力工程", 10)
]


def get_gradient_color(x, max_value):
    # 从亮黄(#FFFF00)渐变到亮绿(#00FF00)
    start_rgb = (255, 255, 0)   # #FFFF00
    end_rgb = (0, 255, 0)       # #00FF00
    
    ratio = x / max_value
    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
    return f"#{r:02x}{g:02x}{b:02x}"

# 获取数据中的最大值
max_value = max([item[1] for item in data])

# 创建词云图
wordcloud = (
    WordCloud(init_opts=opts.InitOpts(width="460px", height="305px"))
    .add("", data, word_size_range=[20, 100], shape="diamond")
    .set_global_opts(title_opts=opts.TitleOpts(is_show=False))
)

wordcloud.set_series_opts(
    label_opts=opts.LabelOpts(formatter="{b}"),
    textstyle_opts=opts.TextStyleOpts()  # 这里不设置颜色，使用默认的浅色颜色
)

# 渲染词云图
wordcloud.render(output_file)

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