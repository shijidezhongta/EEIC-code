# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
# from nltk.corpus import stopwords

# # 示例文本
# # text = """
# # Python is a great programming language. It is widely used in data science, 
# # web development, and artificial intelligence. Many popular libraries in Python 
# # include pandas, numpy, matplotlib, and scikit-learn.
# # """

# text = """
# 阿斯 加德 哈吉 斯打 款哈 金卡 等哈 解答 哈几 哈大 挖机 卡 哈王 大拿手机 第八集 凯撒 阿斯
# """

# font_path = "C:/Windows/Fonts/simhei.ttf"  # 宋体
# # 选择字体路径，假设你已下载了 Noto Sans 字体
# # font_path = "C:/Windows/Fonts/NotoSansCJK-Regular.ttc"  # 例如：Noto Sans 字体路径

# # 生成词云
# wc = WordCloud(
#     font_path=font_path, 
#     background_color=None,  # 设置背景色为 #1D2B3A（深蓝色）
#     mode='RGBA',                 # 使用 RGBA 模式，支持透明度
#     width=800, 
#     height=600,
#     colormap='cool',             # 使用冷色调，适合深色背景（可以试试 'cool', 'Blues', 'winter' 等）
#     contour_color='white',       # 如果需要的话，给词云加上白色轮廓
#     contour_width=1              # 轮廓宽度
# ).generate(text)

# # 显示词云图像
# plt.imshow(wc, interpolation='bilinear')
# plt.axis('off')  # 不显示坐标轴
# plt.show()



import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from wordcloud import WordCloud
import numpy as np

class WordCloudWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 加载UI文件
        loadUi("one_page.ui", self)
        
        # 生成词云并加载到 graphicsView 中
        self.generate_and_display_wordcloud()

    def generate_and_display_wordcloud(self):
        # 生成词云
        text = "Python is a great programming language. It is widely used in data science and artificial intelligence."
        font_path = "C:/Windows/Fonts/simhei.ttf"  # 或其他支持中文的字体路径
        
        wc = WordCloud(
            font_path=font_path,
            background_color=None,
            mode='RGBA',
            width=200,
            height=300,
            colormap='cool',
            contour_color='white',
            contour_width=1
        ).generate(text)

        # 将词云图转换为QImage格式
        img = wc.to_image()
        img = img.convert("RGBA")  # 确保图像是RGBA格式
        
        # 转换为 QImage
        width, height = img.size
        data = np.array(img)
        qt_image = QImage(data.data, width, height, QImage.Format_RGBA8888)

        # 创建 QGraphicsScene
        scene = QGraphicsScene()

        # 将 QImage 转换为 QPixmap 并添加到场景中
        pixmap = QPixmap.fromImage(qt_image)
        scene.addPixmap(pixmap)

        # 将场景设置到 graphicsView
        self.graphicsView.setScene(scene)

# 运行应用
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WordCloudWindow()
    window.show()
    sys.exit(app.exec_())
