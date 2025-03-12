'''
    软件主程序
    主要控制软件的布局及交互逻辑，不包含模型计算过程和AI功能
'''
import sys
import os
import json
import numpy as np
import base64
import threading
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedLayout, QWidget, QTableWidget, QTableWidgetItem, 
    QAbstractItemView, QGraphicsDropShadowEffect, QFrame, QLabel, QGridLayout, 
    QVBoxLayout, QSpacerItem, QSizePolicy, QHBoxLayout, QPushButton, QLineEdit, 
    QGraphicsScene, QDialog,QTextEdit
)
from PyQt5.QtGui import (
    QIcon, QStandardItem, QStandardItemModel, QPainter, QPainterPath, QColor, 
    QImage, QPixmap
)
from PyQt5.QtCore import (
    QThread, pyqtSignal, QTimer, QEvent, Qt, QPropertyAnimation, QEasingCurve, 
    pyqtSlot, QUrl
)
from PyQt5.QtWebEngineWidgets import QWebEngineView

# 自定义模块导入
import DBInit
import langchain4 as langchain_chat
import page_two_drawing.eachsystem_output as model_every_plot
import page_two_drawing.total_output as model_total_plot

# UI界面导入
from UI.main_ui import Ui_ui_main
from UI.one_page import Ui_Form
from UI.two_page import Ui_page_two
from UI.gpt_main import Ui_Form as Ui_Form_gpt
from UI.control import Ui_Form as Ui_Form_control
from UI.connect_db import ConnectDB
from UI.home_window import HomeWindow
from UI.chat_window import ChatWindow

#-------------------------------------------------------UI函数模块----------------------------------------------------------------#

#-------------------------------------线程-----------------------------------#       
class ComputeDataThread(QThread):
    data_ready_signal = pyqtSignal(list)  # 修改为接收一个列表

    def __init__(self, frame_home_page):
        super().__init__()
        self.frame_home_page = frame_home_page

    def run(self):
        # 计算数据
        value_Pmt, value_pv, value_CAES, value_Pump, value_H2, value_bat, value_w, value_CO2, value_if_demand, value_if_carbon = self.frame_home_page.get_value()
       
        # 读取 JSON 文件中的数据
        with open("database.json", "r") as json_file:
            data_base = json.load(json_file)
        # 更新数据库中的相应字段
        data_base["value_Pmt"] = value_Pmt
        data_base["value_pv"] = value_pv
        data_base["value_CAES"] = value_CAES
        data_base["value_Pump"] = value_Pump
        data_base["value_H2"] = value_H2
        data_base["value_bat"] = value_bat
        data_base["value_w"] = value_w
        data_base["value_CO2"] = value_CO2
        data_base["value_if_demand"] = value_if_demand
        data_base["value_if_carbon"] = value_if_carbon
        # 保存更新后的数据回到 JSON 文件
        with open("database.json", "w", encoding="utf-8") as json_file:
            json.dump(data_base, json_file, ensure_ascii=False, indent=4)

        import subprocess
        python_path = "envs\\pythonForCplex\\python.exe"
        subprocess.run([python_path, 'Model_solving_cplex.py'])

#-----------------------------------消息提醒窗口---------------------------------#
from PyQt5.QtCore import Qt, QRectF, QSize, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPainterPath, \
    QColor
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, \
    QGridLayout, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect, \
    QListWidget, QListWidgetItem, QApplication, QPushButton

class NotificationIcon:
    Info, Success, Warning, Error, Close = range(5)
    Types = {
        Success: None,
    }

    @classmethod
    def init(cls):
        cls.Types[cls.Success] = QPixmap(QImage.fromData(base64.b64decode(
            'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACZUlEQVRYR8VXS3LTQBDtVsDbcAPMCbB3limkcAKSG4QFdnaYE2BOQLKzxSLJCeAGSUQheSnfwLmB2VJhXmpExpFHI2sk2RWv5FJPv9evP9NieuIfPzE+VSJw8qt3IMDvmahDoDYxt2UAACXMWIIowR5ffn8TJbaBWRE4CXvHAH9RgKXOgQUI48CfXZbZbiTw8Xe/w3d0zkydMkem91IZpyWOJu5sUXS+kEAqt3B+MNOLOuDqDEBLxxFHk7eza5MfIwEJDjhXTYD1s8zinYlEjsCD7FdNI9cJpEq0RFdPR47AMOzLCn69zegz6UgCP+pmfa8RSKudnPNdgCufTOLDxJtdPP7PoA1Cd8HEL5sSUCCD0B0x8bc1f8Bi6sevcgS2VXh6hMOwDz0gsUddNaxWKRjeuKfE/KlJ9Dq4UYH/o/Ns6scj+bgiMAjdayb26xLQwTfVEwg3gRcf6ARq578KuLo7VDc8psCQqwfjr4EfjYvkrAquFJ56UYpdSkAZSmNd1rrg0leOQFELgvA58OJTxVyRaAJORPOpF6UXnFUR5sDiXjs7UqsOMGMRlrWhTkJXpFL3mNrQZhA1lH3F0TiI5FurUQyMpn58VjhkSqQA4Tbw4nSVW6sBU5VXktXSeONlJH3s8jrOVr9RgVSFuNcWfzlh5n3LoKzMAPxxWuiULiQpiR2sZNnCyzIuWUr5Z1Ml0sgdHFZaShVDuR86/0huL3VXtDk/F4e11vKsTHLSCeKx7bYkW80hjLOrV1GhWH0ZrSlyh2MwdZhYfi8oZeYgLBmUiGd8sfVPM6syr2lUSYGaGBuP3QN6rVUwYV/egwAAAABJRU5ErkJggg==')))
        cls.Types[cls.Close] = QPixmap(QImage.fromData(base64.b64decode(
            'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAeElEQVQ4T2NkoBAwUqifgboGzJy76AIjE3NCWmL0BWwumzV/qcH/f38XpCfHGcDkUVwAUsDw9+8GBmbmAHRDcMlheAGbQnwGYw0DZA1gp+JwFUgKZyDCDQGpwuIlrGGAHHAUGUCRFygKRIqjkeKERE6+oG5eIMcFAOqSchGwiKKAAAAAAElFTkSuQmCC')))

    @classmethod
    def icon(cls, ntype):
        return cls.Types.get(ntype)


class NotificationItem(QWidget):
    closed = pyqtSignal(QListWidgetItem)

    def __init__(self, title, message, item, *args, ntype=0, callback=None, **kwargs):
        super(NotificationItem, self).__init__(*args, **kwargs)
        self.item = item
        self.callback = callback
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.bgWidget = QWidget(self)  # 背景控件, 用于支持动画效果
        layout.addWidget(self.bgWidget)

        layout = QGridLayout(self.bgWidget)
        layout.setHorizontalSpacing(15)
        layout.setVerticalSpacing(10)

        # 标题左边图标
        layout.addWidget(
            QLabel(self, pixmap=NotificationIcon.icon(ntype)), 0, 0)

        # 标题
        self.labelTitle = QLabel(title, self)
        font = self.labelTitle.font()
        font.setBold(True)
        font.setPixelSize(22)
        self.labelTitle.setFont(font)

        # 关闭按钮
        self.labelClose = QLabel(
            self, cursor=Qt.PointingHandCursor, pixmap=NotificationIcon.icon(NotificationIcon.Close))

        # 消息内容
        self.labelMessage = QLabel(
            message, self, cursor=Qt.PointingHandCursor, wordWrap=True, alignment=Qt.AlignLeft | Qt.AlignTop)
        font = self.labelMessage.font()
        font.setPixelSize(20)
        self.labelMessage.setFont(font)
        self.labelMessage.adjustSize()

        # 添加到布局
        layout.addWidget(self.labelTitle, 0, 1)
        layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 2)
        layout.addWidget(self.labelClose, 0, 3)
        layout.addWidget(self.labelMessage, 1, 1, 1, 2)

        # 边框阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(12)
        effect.setColor(QColor(0, 0, 0, 25))
        effect.setOffset(0, 2)
        self.setGraphicsEffect(effect)
        self.adjustSize()

        # 5秒自动关闭
        self._timer = QTimer(self, timeout=self.doClose)
        self._timer.setSingleShot(True)  # 只触发一次
        self._timer.start(5000)

    def doClose(self):
        try:
            # 可能由于手动点击导致item已经被删除了
            self.closed.emit(self.item)
        except:
            pass

    def showAnimation(self, width):
        # 显示动画
        pass

    def closeAnimation(self):
        # 关闭动画
        pass

    def mousePressEvent(self, event):
        super(NotificationItem, self).mousePressEvent(event)
        w = self.childAt(event.pos())
        if not w:
            return
        if w == self.labelClose:  # 点击关闭图标
            # 先尝试停止计时器
            self._timer.stop()
            self.closed.emit(self.item)
        elif w == self.labelMessage and self.callback and callable(self.callback):
            # 点击消息内容
            self._timer.stop()
            self.closed.emit(self.item)
            self.callback()  # 回调

    def paintEvent(self, event):
        # 圆角以及背景色
        super(NotificationItem, self).paintEvent(event)
        painter = QPainter(self)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 6, 6)
        painter.fillPath(path, Qt.white)


class NotificationWindow(QListWidget):
    _instance = None

    def __init__(self, *args, **kwargs):
        super(NotificationWindow, self).__init__(*args, **kwargs)
        self.setSpacing(20)
        self.setMinimumWidth(412)
        self.setMaximumWidth(412)
        QApplication.instance().setQuitOnLastWindowClosed(True)
        # 隐藏任务栏,无边框,置顶等
        self.setWindowFlags(self.windowFlags() | Qt.Tool |
                            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 去掉窗口边框
        self.setFrameShape(self.NoFrame)
        # 背景透明
        self.viewport().setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 不显示滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 获取屏幕高宽
        rect = QApplication.instance().desktop().availableGeometry(self)
        self.setMinimumHeight(rect.height())
        self.setMaximumHeight(rect.height())
        self.move(rect.width() - self.minimumWidth() - 18, 0)

    def removeItem(self, item):
        # 删除item
        w = self.itemWidget(item)
        self.removeItemWidget(item)
        item = self.takeItem(self.indexFromItem(item).row())
        w.close()
        w.deleteLater()
        del item

    @classmethod
    def _createInstance(cls):
        # 创建实例
        if not cls._instance:
            cls._instance = NotificationWindow()
            cls._instance.show()
            NotificationIcon.init()

    @classmethod
    def success(cls, title, message, callback=None):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem(title, message, item, cls._instance,
                             ntype=NotificationIcon.Success, callback=callback)
        w.closed.connect(cls._instance.removeItem)
        item.setSizeHint(QSize(cls._instance.width() -
                               cls._instance.spacing(), w.height()))
        cls._instance.setItemWidget(item, w)
        
#------------------------------------进度条-----------------------------#
# 圆形进度条对话框窗口类
class ProgressDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(ProgressDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("计算中...")  # 设置窗口标题
        self.setFixedSize(300, 300)  # 设置窗口大小

        layout = QVBoxLayout(self)
        self.progress_bar = CircleProgressBar(self)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        # 设置背景色为 #0F192A
        self.setStyleSheet("background-color: #0F192A;")  # 背景颜色

        # 设置定时器，5秒后自动关闭进度条窗口
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.close)  # 超时后关闭窗口
        self._timer.start(5000)  # 5秒后触发

        # 标志位，确保通知只发送一次
        self.is_notification_sent = False

    def showEvent(self, event):
        super(ProgressDialog, self).showEvent(event)
        # 启动进度条动画
        self.progress_bar.start_animation()


    def closeEvent(self, event):
        # 确保通知只触发一次
        if not self.is_notification_sent:
            # NotificationWindow.success('提示', '计算已完成！')
            self.is_notification_sent = True  # 更新标志位，防止再次触发通知

        # 调用父类的 closeEvent 方法
        super(ProgressDialog, self).closeEvent(event)


# 圆形进度条类
class CircleProgressBar(QWidget):
    Color = QColor(24, 189, 155)  # 圆圈颜色
    Clockwise = True  # 顺时针还是逆时针
    Delta = 36

    def __init__(self, *args, color=None, clockwise=True, **kwargs):
        super(CircleProgressBar, self).__init__(*args, **kwargs)
        self.angle = 0
        self.Clockwise = clockwise
        if color:
            self.Color = color
        self._timer = QTimer(self, timeout=self.update)
        self._timer.start(100)  # 每100ms刷新一次
        self._running = False  # 用于控制进度条是否在运行

    def paintEvent(self, event):
        super(CircleProgressBar, self).paintEvent(event)
        if not self._running:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        side = min(self.width(), self.height())
        painter.scale(side / 100.0, side / 100.0)
        painter.rotate(self.angle)
        painter.save()
        painter.setPen(Qt.NoPen)
        color = self.Color.toRgb()
        for i in range(11):
            color.setAlphaF(1.0 * i / 10)
            painter.setBrush(color)
            painter.drawEllipse(30, -10, 20, 20)
            painter.rotate(36)
        painter.restore()
        self.angle += self.Delta if self.Clockwise else -self.Delta
        self.angle %= 360

    def start_animation(self):
        self._running = True
        self.update()

    def stop_animation(self):
        self._running = False
        self.update()     

##---------------------------------------------------------------界面1-------------------------------------------------------------##
class FrameHomePage(QWidget, Ui_Form):
    def __init__(self,main_widget):
        super(FrameHomePage, self).__init__(parent = None)
        self.setupUi(self)
        self.retranslateUi(self)
        
        # 绑定按钮点击事件
        self.pushButton_control.clicked.connect(self.dialog_show)
        self.pushButton_graph.clicked.connect(self.plot_graph)
        self.pushButton_map.clicked.connect(self.plot_map)

        # 获取webEngineView控件
        self.webEngineView_load = self.findChild(QWebEngineView, "webEngineView_load")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_load.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 设置文件夹路径
        folder_path = "page_one_drawing"
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "chart.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_load.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # 获取webEngineView控件
        self.webEngineView_energy = self.findChild(QWebEngineView, "webEngineView_energy")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_energy.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "energy_structure.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_energy.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # 获取webEngineView控件
        self.webEngineView = self.findChild(QWebEngineView, "webEngineView")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "map_hubei.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile           

        # 获取webEngineView控件
        self.webEngineView_2 = self.findChild(QWebEngineView, "webEngineView_2")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_2.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "river.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_2.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile  

        # 获取webEngineView控件
        self.webEngineView_worldcloud = self.findChild(QWebEngineView, "webEngineView_wordcloud")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_worldcloud.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "word_cloud.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_worldcloud.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile  

        # 获取webEngineView控件
        self.webEngineView_3 = self.findChild(QWebEngineView, "webEngineView_3")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_3.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "carbon_price_chart.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_3.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile  

    def plot_graph(self):
        # 清空当前显示的内容（清空画布）
        self.webEngineView.setHtml("")  # 设置空白页面
        # 设置文件夹路径
        folder_path = "page_one_drawing"
        # 获取webEngineView控件
        self.webEngineView = self.findChild(QWebEngineView, "webEngineView")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "graph_les_miserables.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile    

    def plot_map(self):
        # 清空当前显示的内容（清空画布）
        self.webEngineView.setHtml("")  # 设置空白页面
        # 设置文件夹路径
        folder_path = "page_one_drawing"
        # 获取webEngineView控件
        self.webEngineView = self.findChild(QWebEngineView, "webEngineView")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "map_hubei.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile    

    def dialog_show(self):
        self.dialog = Model_dialog()
        self.dialog.show()

##------------------------------------弹窗-----------------------------##
class Model_dialog(QWidget, Ui_Form_control):
    def __init__(self, parent=None):
        super(Model_dialog, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_plot.clicked.connect(self.start_computing_data)
        self.home = FrameHomePage(self)

    def get_value(self):
        # 从窗口里获取数据
        value_Pmt = self.lineEdit_Pmt.text()
        value_pv = self.lineEdit_pv.text()
        value_CAES = self.lineEdit_CAES.text()
        value_Pump = self.lineEdit_Pump.text()
        value_H2 = self.lineEdit_H2.text()
        value_bat = self.lineEdit_bat.text()
        value_w = self.lineEdit_w.text()
        value_CO2 = self.lineEdit_CO2.text()
        value_if_demand = self.lineEdit_if_demand.text()
        value_if_carbon = self.lineEdit_if_carbon.text()
        return value_Pmt, value_pv, value_CAES, value_Pump, value_H2, value_bat, value_w, value_CO2, value_if_demand, value_if_carbon

    def start_computing_data(self):
        # 创建并显示进度条窗口
        self.progress_dialog = ProgressDialog(self)
        self.progress_dialog.show()

        # 数据求解函数
        self.data_thread = ComputeDataThread(self)  # 传入当前实例
        self.data_thread.start()  # 启动线程

from PyQt5.QtCore import QObject, pyqtSlot

class Bridge(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # 假设parent是主窗口，用于访问webEngineView

    @pyqtSlot(str)
    def handleMapClick(self, region):
        if region == 'wuhan':
            self.judge()

    def judge(self):
        # 清除原始绘图
        self.parent.webEngineView.page().runJavaScript('clearMap();')
        # 加载武汉市地图
        folder_path = self.parent.folder_path  # 假设folder_path存储在主窗口
        chart_file = os.path.join(folder_path, "map_wuhan.html")
        abs_path = os.path.abspath(chart_file)
        self.parent.webEngineView.setUrl(QUrl.fromLocalFile(abs_path))

##-----------------------------------------------------界面2-------------------------------------------------------------##
class FrameBlogPage(QWidget, Ui_page_two):
    def __init__(self, parent = None):
        super(FrameBlogPage,self).__init__(parent)
        self.setupUi(self)
        self.home = FrameHomePage(self)
        self.pushButton_plot.clicked.connect(self.draw_plot1)
        self.pushButton_part1.clicked.connect(self.draw_plot1)
        self.pushButton_part2.clicked.connect(self.draw_plot2)
        self.pushButton_part3.clicked.connect(self.draw_plot3)
    def update_plot(self): 
        # 绘图完成后，更新画布显示
        self.canvas.draw()

    def draw_plot1(self):
        model_every_plot.updata_four_plot()
        model_total_plot.updata_total_plot()

       # 获取webEngineView控件
        self.webEngineView_Ppm = self.findChild(QWebEngineView, "webEngineView_Ppm")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_Ppm.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 设置文件夹路径
        folder_path = "page_two_drawing"
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "Ppm.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_Ppm.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile
        
        # 获取webEngineView控件
        self.webEngineView_bat = self.findChild(QWebEngineView, "webEngineView_bat")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_bat.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "bat_zero.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_bat.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # 获取webEngineView控件
        self.webEngineView_H2 = self.findChild(QWebEngineView, "webEngineView_H2")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_H2.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "H2_zero.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_H2.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # 获取webEngineView控件
        self.webEngineView_CAES = self.findChild(QWebEngineView, "webEngineView_CAES")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_CAES.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "CAES.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_CAES.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # 获取webEngineView控件
        self.webEngineView_total = self.findChild(QWebEngineView, "webEngineView_total")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_total.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "total_plot1.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_total.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # 获取webEngineView控件
        self.webEngineView_pv = self.findChild(QWebEngineView, "webEngineView_pv")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_pv.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "pv1.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_pv.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # 获取webEngineView控件
        self.webEngineView_w = self.findChild(QWebEngineView, "webEngineView_w")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_w.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "w1.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_w.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # # 读取 JSON 文件中的数据
        # with open("database.json", "r") as json_file:
        #     data = json.load(json_file)
        # value = np.array(data.get("total_value"))
        # # 将结果显示在 textBrowser_out 中
        # self.textBrowser_out.setText(value)

    def draw_plot2(self):
        model_every_plot.updata_four_plot()
        model_total_plot.updata_total_plot()

       # 获取webEngineView控件
        self.webEngineView_Ppm = self.findChild(QWebEngineView, "webEngineView_Ppm")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_Ppm.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 设置文件夹路径
        folder_path = "page_two_drawing"
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "Ppm_zero.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_Ppm.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile
        
        # 获取webEngineView控件
        self.webEngineView_bat = self.findChild(QWebEngineView, "webEngineView_bat")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_bat.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "bat1.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_bat.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # 获取webEngineView控件
        self.webEngineView_H2 = self.findChild(QWebEngineView, "webEngineView_H2")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_H2.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "H2.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_H2.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # 获取webEngineView控件
        self.webEngineView_CAES = self.findChild(QWebEngineView, "webEngineView_CAES")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_CAES.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "CAES_zero.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_CAES.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # 获取webEngineView控件
        self.webEngineView_total = self.findChild(QWebEngineView, "webEngineView_total")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_total.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "total_plot2.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_total.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # 获取webEngineView控件
        self.webEngineView_pv = self.findChild(QWebEngineView, "webEngineView_pv")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_pv.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "pv2.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_pv.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # 获取webEngineView控件
        self.webEngineView_w = self.findChild(QWebEngineView, "webEngineView_w")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_w.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "w2.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_w.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # # 读取 JSON 文件中的数据
        # with open("database.json", "r") as json_file:
        #     data = json.load(json_file)
        # value = np.array(data.get("total_value"))
        # # 将结果显示在 textBrowser_out 中
        # self.textBrowser_out.setText(value)

    def draw_plot3(self):
        model_every_plot.updata_four_plot()
        model_total_plot.updata_total_plot()

       # 获取webEngineView控件
        self.webEngineView_Ppm = self.findChild(QWebEngineView, "webEngineView_Ppm")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_Ppm.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 设置文件夹路径
        folder_path = "page_two_drawing"
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "Ppm_zero.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_Ppm.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile
        
        # 获取webEngineView控件
        self.webEngineView_bat = self.findChild(QWebEngineView, "webEngineView_bat")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_bat.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "bat2.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_bat.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # 获取webEngineView控件
        self.webEngineView_H2 = self.findChild(QWebEngineView, "webEngineView_H2")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_H2.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "H2_zero.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_H2.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # 获取webEngineView控件
        self.webEngineView_CAES = self.findChild(QWebEngineView, "webEngineView_CAES")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_CAES.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "CAES_zero.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_CAES.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # 获取webEngineView控件
        self.webEngineView_total = self.findChild(QWebEngineView, "webEngineView_total")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_total.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "total_plot3.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_total.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # 获取webEngineView控件
        self.webEngineView_pv = self.findChild(QWebEngineView, "webEngineView_pv")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_pv.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "pv_zero.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_pv.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # 获取webEngineView控件
        self.webEngineView_w = self.findChild(QWebEngineView, "webEngineView_w")
        # 获取QWebEnginePage，并设置背景透明
        self.webEnginePage = self.webEngineView_w.page()
        self.webEnginePage.setBackgroundColor(Qt.transparent)  # 设置网页的背景透明
        # 生成完整的文件路径
        chart_file = os.path.join(folder_path, "w3.html")
        # 获取HTML文件的绝对路径
        chart_file_abs_path = os.path.abspath(chart_file)
        # 将HTML文件加载到webEngineView控件中
        self.webEngineView_w.setUrl(QUrl.fromLocalFile(chart_file_abs_path))  # 使用QUrl.fromLocalFile

        # # 读取 JSON 文件中的数据
        # with open("database.json", "r") as json_file:
        #     data = json.load(json_file)
        # value = np.array(data.get("total_value"))
        # # 将结果显示在 textBrowser_out 中
        # self.textBrowser_out.setText(value)

##------------------------------------------------------------界面3-----------------------------------------------------------------## 
class CustomWidget(QWidget):
    def __init__(self, text, show_btn_flag, *args, **kwargs):
        super(CustomWidget, self).__init__(*args, **kwargs)

        # 创建聊天标题的水平布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 0, 0)  # 设置布局的外边距

        # 创建聊天图标按钮
        chat_icon = QIcon("icons\chat_24dp_FFFFFF.svg")  # 设置聊天图标
        chat_icon_btn = QPushButton(self)  # 创建按钮控件
        chat_icon_btn.setIcon(chat_icon)  # 设置按钮的图标

        # 创建显示聊天标题的文本框（QLineEdit）
        chat_title = QLineEdit(self)
        chat_title.setText(text)  # 设置标题文本
        chat_title.setReadOnly(True)  # 设置为只读，防止编辑

        # 创建编辑和删除按钮
        delete_btn = QPushButton(self)
        delete_btn.setIcon(QIcon("icons\delete_24dp_FFFFFF.svg"))  # 设置删除按钮图标

        edit_btn = QPushButton(self)
        edit_btn.setIcon(QIcon("icons\create_24dp_FFFFFF.svg"))  # 设置编辑按钮图标

        # 设置聊天标题的样式
        chat_title_style = """
            QLineEdit {
                background:transparent;
                border: none;
                color: #fff;
                font-size: 20px;
                padding-left: 2px;
            }
        """
        chat_title.setStyleSheet(chat_title_style)  # 应用样式到 QLineEdit

        # 设置按钮的样式
        style_str = """
            QPushButton {
                border: none;
                max-width: 20px;
                max-height: 20px;
                background: transparent;
            }
        """
        chat_icon_btn.setStyleSheet(style_str)  # 设置图标按钮样式
        edit_btn.setStyleSheet(style_str)  # 设置编辑按钮样式
        delete_btn.setStyleSheet(style_str)  # 设置删除按钮样式

        # 如果不显示按钮，则隐藏编辑和删除按钮
        if not show_btn_flag:
            delete_btn.hide()  # 隐藏删除按钮
            edit_btn.hide()  # 隐藏编辑按钮

        # 将所有控件添加到布局中
        layout.addWidget(chat_icon_btn)  # 添加聊天图标按钮
        layout.addWidget(chat_title)  # 添加聊天标题文本框
        layout.addWidget(edit_btn)  # 添加编辑按钮
        layout.addWidget(delete_btn)  # 添加删除按钮

class FrameGPTPage(QWidget, Ui_Form_gpt):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 实例化数据库对象，用于处理聊天数据
        self.connect_db = ConnectDB()

        # 获取主窗口UI中的控件对象
        self.message_input = self.input_textEdit  # 用户消息输入区域
        self.input_frame = self.input_frame  # 输入区域的外框
        self.new_chat_btn = self.new_chat_pushButton  # 创建新聊天按钮
        self.send_message_btn = self.input_Button  # 发送消息按钮
        self.main_scrollArea = self.scrollArea  # 聊天内容显示的滚动区域
        self.robot_combo_box = self.comboBox  # 下拉框（可能用于选择聊天机器人或模型）
        self.clear_conversations_btn = self.pushButton  # 清空所有对话按钮
        self.logout_btn = self.pushButton_4  # 注销按钮

        # 隐藏滚动区域的垂直滚动条
        self.main_scrollArea.setVerticalScrollBarPolicy(1)

        # 根据内容调整输入框和输入区域的大小
        self.message_input.setFixedHeight(130)
        self.input_frame.setFixedHeight(150)

        # 初始化聊天列表和显示首页窗口
        self.show_chat_list()
        self.show_home_window()

        # 连接UI控件的点击信号到相应的槽函数
        self.send_message_btn.clicked.connect(self.get_response)  # 发送消息
        self.new_chat_btn.clicked.connect(self.create_new_chat)  # 创建新聊天
        self.clear_conversations_btn.clicked.connect(self.clear_conversations)  # 清空所有对话
        self.logout_btn.clicked.connect(self.log_out)  # 注销应用

    def handle_key_press(self, event):
        # 如果按下的是 Enter 键，则触发按钮点击事件
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.send_message_btn.click()  # 模拟按钮点击
        else:
            # 调用父类的 keyPressEvent 方法，确保其他按键的正常输入
            super(QTextEdit, self.message_input).keyPressEvent(event)  # 保持其他键盘事件正常处理

    def create_new_chat(self):
        self.show_home_window()  # 显示首页窗口（可能是默认状态）
        self.show_chat_list(selected_index=None)  # 显示空的聊天列表或新聊天列表

    def clear_conversations(self):
        self.connect_db.delete_all_data()  # 从数据库中删除所有聊天数据
        self.show_home_window()  # 重新加载首页窗口
        self.show_chat_list()  # 重新加载聊天列表

    def log_out(self):
        self.close()  # 关闭主窗口（以及应用程序）        

    def clear_main_scroll_area(self):
        """
        清空主聊天窗口中的所有控件，当重新加载聊天窗口时调用
        """
        # 获取滚动区域中的QGridLayout布局，并清除所有子控件
        grid_layout = self.main_scrollArea.findChild(QGridLayout)
        grid_layout.setContentsMargins(0, 0, 0, 0)  # 移除边距

        # 获取所有的子控件（如标签、按钮、框架）
        children_list = grid_layout.children()
        remove_widget_list = [QLabel, QPushButton, QFrame]  # 要移除的控件类型
        for remove_widget in remove_widget_list:
            children_list += self.main_scrollArea.findChildren(remove_widget)

        # 删除所有找到的控件
        for child in children_list:
            child.deleteLater()

        # 移除布局中的所有空白项
        for row in range(grid_layout.rowCount()):
            for column in range(grid_layout.columnCount()):
                item = grid_layout.itemAtPosition(row, column)
                if item:
                    grid_layout.removeItem(item)

        return grid_layout

    def on_chat_list_clicked(self):
        """
        处理聊天列表中聊天项被点击时的事件
        """
        chat_list = []

        # 当切换聊天时，清空输入框
        self.message_input.clear()

        # 获取当前选中的聊天行索引
        current_index = self.chat_list.currentIndex()
        select_row = current_index.row()

        # 获取聊天列表中的聊天项数量
        chat_models = self.chat_list.model()
        chat_count = chat_models.rowCount()

        # 遍历聊天列表中的所有聊天
        for i in range(chat_count):
            row_index = chat_models.index(i, 0)
            current_chat = self.chat_list.indexWidget(row_index)
            chat_title = current_chat.findChild(QLineEdit)
            if chat_title:
                # 检查聊天是否被标记为“待删除”状态
                if i == select_row and chat_title.text().startswith("Delete \""):
                    chat_list.append(chat_title.text().split('"')[1])  # 获取聊天标题
                else:
                    chat_list.append(chat_title.text())  # 获取聊天标题
            else:
                chat_list.append("")  # 没有标题则添加空字符串

        # 重新加载聊天列表
        for row, chat in enumerate(chat_list):
            index = chat_models.index(row, 0)
            # 检查当前聊天标题是否被选中
            if row == select_row:
                show_btn_flag = True  # 如果选中，显示编辑和删除按钮
            else:
                show_btn_flag = False

            # 创建聊天标题控件
            widget = CustomWidget(chat, show_btn_flag)

            # 设置并显示聊天标题到聊天列表（QListView）中
            self.chat_list.setIndexWidget(index, widget)

            # 获取聊天标题控件中的按钮对象
            operation_btn = widget.findChildren(QPushButton)

            # 连接按钮的信号与槽
            edit_btn = operation_btn[2]
            edit_btn.clicked.connect(self.edit_chat)

            delete_btn = operation_btn[1]
            delete_btn.clicked.connect(self.delete_chat)

        # 获取选中的聊天数据并显示在主聊天内容窗口中
        chat_db = self.connect_db.get_chat_data()
        chat_data = chat_db[select_row]
        self.show_chat_window(chat_data)

    @pyqtSlot()
    def edit_chat(self):
        # 获取当前聊天项的索引
        current_index = self.chat_list.currentIndex()
        # 获取当前聊天项的控件对象
        current_chat = self.chat_list.indexWidget(current_index)

        # 找到聊天标题的 QLineEdit 控件
        chat_title = current_chat.findChild(QLineEdit)

        # 获取原始的聊天标题
        pre_chat_title = chat_title.text()

        # 设置 QLineEdit 为可编辑
        chat_title.setReadOnly(False)
        chat_title_style = """
            QLineEdit {
                background:transparent;
                border: 1px solid #2563eb;
                color: #fff;
                font-size: 15px;
                padding-left: 2px;
            }
        """
        # 设置编辑框的样式
        chat_title.setStyleSheet(chat_title_style)

        # 获取操作按钮（确认和取消）
        operation_btns = current_chat.findChildren(QPushButton)
        confirm_btn = operation_btns[2]
        cancel_btn = operation_btns[1]

        # 设置按钮图标
        confirm_btn.setIcon(QIcon("icons\create_24dp_FFFFFF.svg"))
        cancel_btn.setIcon(QIcon("icons\delete_24dp_FFFFFF.svg"))

        # 断开按钮的原有连接，防止重复连接
        confirm_btn.clicked.disconnect()
        cancel_btn.clicked.disconnect()

        # 连接按钮的点击事件
        confirm_btn.clicked.connect(lambda: self.confirm_edit(chat_title))
        cancel_btn.clicked.connect(lambda: self.cancel_edit(pre_chat_title, chat_title))

    @pyqtSlot()
    def confirm_edit(self, chat_title):
        # 获取当前选中的聊天索引
        current_index = self.chat_list.currentIndex().row()

        # 获取聊天数据库数据
        chat_db = self.connect_db.get_chat_data()
        # 修改标题
        chat_db[current_index]["title"] = chat_title.text()

        # 保存修改后的数据
        self.connect_db.save_chat_data(chat_db)
        # 更新聊天列表显示
        self.on_chat_list_clicked()

    @pyqtSlot()
    def cancel_edit(self, pre_chat_title, chat_title):
        # 恢复原始标题
        chat_title.setText(pre_chat_title)
        # 更新聊天列表显示
        self.on_chat_list_clicked()

    @pyqtSlot()
    def delete_chat(self):
        # 获取当前聊天项的索引
        current_index = self.chat_list.currentIndex()
        # 获取聊天控件
        current_chat = self.chat_list.indexWidget(current_index)

        # 找到 QLineEdit 控件，显示确认删除的提示
        chat_title = current_chat.findChild(QLineEdit)
        chat_title.setReadOnly(True)
        chat_title_text = chat_title.text()
        chat_title.setText(f'Delete "{chat_title_text}"?')
        chat_title_style = """
            QLineEdit {
                background:transparent;
                border: none;
                color: #fff;
                font-size: 15px;
                padding-left: 2px;
            }
        """
        # 设置标题样式
        chat_title.setStyleSheet(chat_title_style)

        # 获取操作按钮（删除确认和取消）
        operation_btns = current_chat.findChildren(QPushButton)
        chat_icon_btn = operation_btns[0]
        confirm_btn = operation_btns[2]
        cancel_btn = operation_btns[1]

        # 设置按钮图标
        chat_icon_btn.setIcon(QIcon("icons\delete_24dp_FFFFFF.svg"))
        confirm_btn.setIcon(QIcon("icons\check_circle_24dp_FFFFFF.svg"))
        cancel_btn.setIcon(QIcon("icons\cancel_24dp_FFFFFF.svg"))

        # 断开原有的点击事件连接
        confirm_btn.clicked.disconnect()
        cancel_btn.clicked.disconnect()

        # 连接删除确认和取消按钮的事件
        confirm_btn.clicked.connect(self.confirm_delete)
        cancel_btn.clicked.connect(self.cancel_delete)

    @pyqtSlot()
    def confirm_delete(self):
        # 获取当前选中的聊天索引
        current_index = self.chat_list.currentIndex()
        index = current_index.row()

        # 获取聊天数据库数据
        chat_db = self.connect_db.get_chat_data()
        # 删除当前聊天记录
        chat_db.pop(index)

        # 保存更新后的数据库
        self.connect_db.save_chat_data(chat_db)
        # 返回首页并更新聊天列表
        self.show_home_window()
        self.show_chat_list()

    @pyqtSlot()
    def cancel_delete(self):
        # 恢复聊天列表显示
        self.on_chat_list_clicked()

    # 在没有对话的时候展现主页面
    def show_home_window(self):
        grid_layout = self.clear_main_scroll_area()
        # 显示一个默认的“新消息”窗口
        home_window = HomeWindow()
        grid_layout.addWidget(home_window)

    # 显示当前选中聊天记录的内容
    def show_chat_window(self, chat_data):
        grid_layout = self.clear_main_scroll_area()
        # 显示聊天窗口
        chat_window = ChatWindow(chat_object=self.message_input, chat_data=chat_data)
        grid_layout.addWidget(chat_window)

    # 更新并显示聊天记录列表
    def show_chat_list(self, selected_index=None):
        # 创建 QStandardItemModel 显示聊天标题列表
        model = QStandardItemModel()
        self.chat_list.setModel(model)
        # 从数据库中获取聊天记录
        chat_list = self.connect_db.get_chat_title_list()

        for chat in chat_list:
            item = QStandardItem()
            model.appendRow(item)

            # 获取当前聊天项的索引
            index = item.index()
            index_text = index.row()

            if index_text == selected_index:
                show_btn_flag = True
                # 设置当前选中项
                self.chat_list.setCurrentIndex(index)
            else:
                show_btn_flag = False

            # 创建自定义小部件来显示聊天标题
            widget = CustomWidget(chat, show_btn_flag)

            # 将小部件设置为聊天列表项
            self.chat_list.setIndexWidget(index, widget)

            # 获取操作按钮并连接事件
            operation_btn = widget.findChildren(QPushButton)
            edit_btn = operation_btn[2]
            edit_btn.clicked.connect(self.edit_chat)

            delete_btn = operation_btn[1]
            delete_btn.clicked.connect(self.delete_chat)  

    # 获得gpt回复
    def get_response(self):
        # 获取用户输入
        message_input = self.message_input.toPlainText().strip()

        chat_db = self.connect_db.get_chat_data()

        if message_input:
            # 调用 OpenAI 接口获取响应
            response_list = langchain_chat.get_response(message_input)
            # response_list = "你好"
            response_str = "".join(response_list)

            # 判断是否有已选中的聊天记录
            if self.chat_list.selectedIndexes():
                # 获取当前选中的聊天记录索引
                current_index = self.chat_list.currentIndex()
                select_row = current_index.row()

                # 将输入和响应添加到聊天记录
                chat_db[select_row]["chat_list"] += [{"input_str": message_input, "out_str": response_str}]
                chat_data = chat_db[select_row]

                # 保存更新后的聊天记录
                self.connect_db.save_chat_data(chat_db)
                self.show_chat_window(chat_data)

            else:
                # 创建新的聊天记录
                chat_data = {
                    "title": message_input,
                    "chat_list": [
                        {
                            "input_str": message_input,
                            "out_str": response_str
                        }
                    ]
                }
                chat_db.insert(0, chat_data)
                self.connect_db.save_chat_data(chat_db)

                # 显示新的聊天记录
                self.show_chat_window(chat_data)
                self.show_chat_list(selected_index=0)

            # 清空输入框
            self.message_input.clear()

        else:
            # 如果没有输入内容，显示提示
            return

        threading.Thread(target=main_Model_solving).start()           

def main_Model_solving():
    with open("database.json", "r") as json_file:
        data_base = json.load(json_file)
    if data_base["calculate"] == 1:
        import subprocess
        python_path = "envs\\pythonForCplex\\python.exe"
        subprocess.run([python_path, 'Model_solving_cplex.py'])
    # NotificationWindow.success('提示', '计算已完成！')
##----------------------------------主窗口----------------------------------##
class MainWidget(QWidget,Ui_ui_main):
    """
    主窗口
    """
    def __init__(self):
        super().__init__()
        self.ui = Ui_ui_main()
        self.setupUi(self)

        self.qsl = QStackedLayout(self.mainBodyContainer)
        # 实例化分页面
        self.home = FrameHomePage(self)
        self.blog = FrameBlogPage()
        self.GPT = FrameGPTPage()
        # 加入到布局中
        self.qsl.addWidget(self.home)
        self.qsl.addWidget(self.blog)
        self.qsl.addWidget(self.GPT)
        # 控制函数
        self.controller()

        ## Shadow effect style
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 550))

        self.centralwidget.setGraphicsEffect(self.shadow)

        #左菜单栏滑动开关
        self.open_close_side_bar_btn.clicked.connect(lambda : self.slideLeftMenu())

    def slideLeftMenu(self):
            # 获取当前左侧菜单宽度
            width = self.left_menu_cont_frame.width()
            
            # 如果菜单已经收缩
            if width == 70:
                # 展开菜单
                newWidth = 220
            else:
                # 恢复菜单
                newWidth = 70

            # 设置动画效果，过渡菜单的宽度
            self.animation = QPropertyAnimation(self.left_menu_cont_frame, b"maximumWidth")
            self.animation.setDuration(250)
            self.animation.setStartValue(width)  # 当前菜单宽度
            self.animation.setEndValue(newWidth)  # 新的菜单宽度
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()


    def controller(self):
        self.pushButton_page1.clicked.connect(self.switch)    
        self.pushButton_page2.clicked.connect(self.switch)
        self.pushButton.clicked.connect(self.switch)

    def switch(self):
        sender = self.sender().objectName()

        index = {
            "pushButton_page1": 0,
            "pushButton_page2": 1,
            "pushButton": 2,
        }

        self.qsl.setCurrentIndex(index[sender])

if __name__ == '__main__':
    DBInit.database_init()
    app = QApplication(sys.argv)
    
    # 实例化主窗口并显示
    main_window = MainWidget()
    main_window.show()

    sys.exit(app.exec_())

