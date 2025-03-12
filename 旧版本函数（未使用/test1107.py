from PyQt5.QtWidgets import QApplication, QStackedLayout, QWidget,QTableWidget,QTableWidgetItem,QAbstractItemView
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QDialog, QVBoxLayout,QSpacerItem, QSizePolicy
from PyQt5.QtCore import  QThread, pyqtSignal,QTimer,QEvent,Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from Custom_Widgets.Widgets import *
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
import Model_solving_cplex
import Model_windowPlot
# 导入生成的 ui
from main_ui import Ui_ui_main
from one_page import Ui_Form
from two_page import Ui_page_two
from gpt_main import Ui_Form as Ui_Form_gpt
from gpt_in import Ui_Form as Input_Form
from gpt_out import Ui_Form as Out_Form
# from contact_page import Ui_contact_page
import sys
import plot_four_line

##------------------------------多线程函数-------------------------------##
class PlotThread_2(QThread):
    plot_done_signal = pyqtSignal()

    def run(self):
        Model_solving_cplex.Translate_plot_CAES
        self.plot_done_signal.emit()

class PlotThread_1(QThread):
    # 定义信号用于将绘图完成信号发送给主线程
    plot_done_signal = pyqtSignal()
    plot_value_signal = pyqtSignal(object)  # 定义新的信号传递 `value`

    def __init__(self, axes, Pfc, Pel, Pmt, Pcaes_d, Pcaes_g, Pdis, Pcha, Pgen, Ppm, P_w, P_pv, Load_real, total_value):
        super().__init__()
        self.axes = axes  # 接收绘图的目标轴
        self.Pmt = Pmt  # 接收参数
        self.pv = P_pv
        self.w = P_w
        self.Pcaes_d = Pcaes_d
        self.Pcaes_g = Pcaes_g
        self.Ppm = Ppm
        self.Pgen = Pgen
        self.Pfc = Pfc
        self.Pel = Pel
        self.Pdis = Pdis
        self.Pcha = Pcha
        self.Load_real = Load_real
        self.total_value = total_value

    def run(self):
        # 执行绘图操作
        value = Model_solving_cplex.Translate_plot(self.Pmt, self.pv, self.w, self.Pcaes_d, self.Pcaes_g, self.Ppm, self.Pgen, self.Pfc, self.Pel, self.Pdis, self.Pcha, self.Load_real, self.axes, self.total_value)
        self.plot_done_signal.emit()  # 绘图完成后发送信号
        self.plot_value_signal.emit(value)  # 发送 `value` 数值信号

class ProgressThread_1(QThread):
    #进度条函数
    update_progress_signal = pyqtSignal(int)

    def run(self):
        progress_value = 0
        while progress_value <= 100:
            self.update_progress_signal.emit(int(progress_value))
            progress_value += 4.3
            self.msleep(100)  # 每100ms更新一次进度条
        self.update_progress_signal.emit(100)
     
class ComputeDataThread(QThread):
    data_ready_signal = pyqtSignal(list)  # 修改为接收一个列表

    def __init__(self, frame_home_page):
        super().__init__()
        self.frame_home_page = frame_home_page

    def run(self):
        # 计算数据
        value_Pmt, value_pv, value_CAES, value_Pump, value_H2, value_bat, value_w, value_CO2, value_if_demand, value_if_carbon = self.frame_home_page.get_value()
        data = Model_solving_cplex.Model_solving(value_Pmt, value_pv, value_CAES, value_Pump, value_H2, value_bat, value_w, value_CO2, value_if_demand, value_if_carbon)
        labels, ST, Pfc, Pel, Pmt, Pcaes_d, Pcaes_g, Pdis, Pcha, Pgen, Ppm, P_w, P_pv, Load_real, total_value = data
        # 将所有数据打包成一个列表
        self.data_ready_signal.emit([labels, ST, Pfc, Pel, Pmt, Pcaes_d, Pcaes_g, Pdis, Pcha, Pgen, Ppm, P_w, P_pv, Load_real, total_value])

def create_bar_chart(names, data):
    dialog = Model_windowPlot.LineChartDialog(names, data)
    dialog.exec_()

##-------------------------------------界面1-------------------------------##
class FrameHomePage(QWidget, Ui_Form):
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget  # 存储主窗口实例
        # 全局初始化参数
        self.labels = None  # 初始化labels
        self.ST = None  # 初始化ST
        self.Pmt = None  # 接收参数
        self.pv = None
        self.w = None
        self.Pcaes_d = None
        self.Pcaes_g = None
        self.Ppm = None
        self.Pgen = None
        self.Pfc = None
        self.Pel = None
        self.Pdis = None
        self.Pcha = None
        self.Load_real = None
        self.total_value = None

        self.setupUi(self)
        self.retranslateUi(self)
        
        # 绑定按钮点击事件
        self.pushButton_plot.clicked.connect(self.start_computing_data)
        self.pushButton_window.clicked.connect(self.on_button_clicked)   

        # 创建 QGraphicsScene，并添加到 QGraphicsView
        self.scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)

        # 创建 Matplotlib Figure 和 FigureCanvas
        self.figure = Figure(figsize=(7, 6.1), dpi=100)
        # 设置背景为透明
        self.figure.patch.set_facecolor('none')  # 设置画布背景透明
        
        # 创建 Canvas，并设置为透明
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet('background: transparent;')  # 设置画布背景透明        

        self.axes = self.figure.add_subplot(111)

        # 将 FigureCanvas 添加到 QGraphicsScene 中
        self.scene.addWidget(self.canvas)

        # 初始化进度条
        self.progressBar.setValue(0)

    def start_computing_data(self):
        # 清空当前画布
        self.axes.clear()  
        #进度条函数
        self.progress_thread = ProgressThread_1()
        self.progress_thread.update_progress_signal.connect(self.update_progress)
        self.progress_thread.start()

        #数据求解函数
        self.data_thread = ComputeDataThread(self)  # 传入当前实例
        self.data_thread.data_ready_signal.connect(self.on_data_ready)
        self.data_thread.start()  # 启动线程



    def on_data_ready(self, data):
        # self.calculated_data = data  # 存储计算结果
        self.labels, self.ST, self.Pfc, self.Pel, self.Pmt, self.Pcaes_d, self.Pcaes_g, self.Pdis, self.Pcha, self.Pgen, self.Ppm, self.P_w, self.P_pv, self.Load_real, total_value = data

        # 传递数据到主窗口
        self.main_widget.Pel = self.Pel
        self.main_widget.Pfc = self.Pfc
        self.main_widget.Ppm = self.Ppm
        self.main_widget.Pgen = self.Pgen
        self.main_widget.Pdis = self.Pdis
        self.main_widget.Pcha = self.Pcha
        self.main_widget.Pcaes_d = self.Pcaes_d
        self.main_widget.Pcaes_g = self.Pcaes_g
        # # 创建 FrameBlogPage 实例，并传递参数
        self.blog_page = FrameBlogPage(self.Pel, self.Pfc, self.Ppm, self.Pgen, self.Pdis, self.Pcha, self.Pcaes_d, self.Pcaes_g)

        #画源荷储总出力图
        self.plot_thread = PlotThread_1(self.axes,self.Pfc, self.Pel, self.Pmt, self.Pcaes_d, self.Pcaes_g, self.Pdis, self.Pcha, self.Pgen, self.Ppm, self.P_w, self.P_pv, self.Load_real, total_value)  # 将参数传递给绘图线程
        self.plot_thread.plot_done_signal.connect(self.update_plot)  # 绘图完成信号连接到更新画布函数
        self.plot_thread.plot_value_signal.connect(self.display_value_in_text_browser)  # 连接 `value` 显示函数        
        self.plot_thread.start()


    def get_value(self):
        #从窗口里获取数据
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
        return value_Pmt,value_pv,value_CAES,value_Pump,value_H2,value_bat,value_w,value_CO2,value_if_demand,value_if_carbon

    def display_value_in_text_browser(self, value):
        formatted_value = f"{value:.3f}"  # 保留三位小数
        # 将 `value` 显示在 textBrowser_out 中
        self.textBrowser_out.setText(str(formatted_value))
        
    def update_progress(self, value):
        # 更新进度条值
        self.progressBar.setValue(value)

    def update_plot(self): 
        # 绘图完成后，更新画布显示
        self.canvas.draw()

    def on_button_clicked(self):
        create_bar_chart(self.labels, self.ST.T)  # 显示图表窗口 

##------------------------------------界面2-----------------------------##
class FrameBlogPage(QWidget, Ui_page_two):
    def __init__(self, Pel, Pfc, Ppm, Pgen, Pdis, Pcha, Pcaes_d, Pcaes_g):
        super().__init__()
        self.Pel = Pel
        self.Pfc = Pfc
        self.setupUi(self)

        # 创建图形视图

        # 创建 QGraphicsScene，并添加到 QGraphicsView
        self.scene_1 = QGraphicsScene(self)
        self.graphicsView_Ppm.setScene(self.scene_1)
        self.scene_2 = QGraphicsScene(self)
        self.graphicsView_H2.setScene(self.scene_2) 
        self.scene_3 = QGraphicsScene(self)
        self.graphicsView_bat.setScene(self.scene_3)
        self.scene_4 = QGraphicsScene(self)
        self.graphicsView_CAES.setScene(self.scene_4)

        # 为每个场景创建独立的 Figure 和 FigureCanvas
        self.figure_1 = Figure(figsize=(3.5, 2.4))
        self.canvas_1 = FigureCanvas(self.figure_1)
        self.figure_1.patch.set_facecolor('none')  # 设置画布背景透明        
        self.canvas_1 = FigureCanvas(self.figure_1)
        self.canvas_1.setStyleSheet('background: transparent;')  # 设置画布背景透明         
        self.scene_1.addWidget(self.canvas_1)

        self.figure_2 = Figure(figsize=(3.5, 2.4))
        self.canvas_2 = FigureCanvas(self.figure_2)
        self.figure_2.patch.set_facecolor('none')  # 设置画布背景透明        
        self.canvas_2 = FigureCanvas(self.figure_2)
        self.canvas_2.setStyleSheet('background: transparent;')  # 设置画布背景透明         
        self.scene_2.addWidget(self.canvas_2)

        self.figure_3 = Figure(figsize=(3.5, 2.4))
        self.canvas_3 = FigureCanvas(self.figure_3)
        self.figure_3.patch.set_facecolor('none')  # 设置画布背景透明        
        self.canvas_3 = FigureCanvas(self.figure_3)
        self.canvas_3.setStyleSheet('background: transparent;')  # 设置画布背景透明 
        self.scene_3.addWidget(self.canvas_3)

        self.figure_4 = Figure(figsize=(3.5, 2.4))
        self.canvas_4 = FigureCanvas(self.figure_4)
        self.figure_4.patch.set_facecolor('none')  # 设置画布背景透明        
        self.canvas_4 = FigureCanvas(self.figure_4)
        self.canvas_4.setStyleSheet('background: transparent;')  # 设置画布背景透明 
        self.scene_4.addWidget(self.canvas_4)

        # 绑定 TableWidget
        self.tableWidget = self.findChild(QTableWidget, "tableWidget")  # 查找表格组件
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置垂直和水平滚动条的显示策略
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用垂直滚动条
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用水平滚动条

    def update_data(self, Pel, Pfc, Ppm, Pgen, Pdis, Pcha, Pcaes_d, Pcaes_g):
        #获取数据
        self.Pel = Pel
        self.Pfc = Pfc
        self.Ppm = Ppm
        self.Pgen = Pgen
        self.Pdis = Pdis
        self.Pcha = Pcha
        self.Pcaes_d = Pcaes_d
        self.Pcaes_g = Pcaes_g

        # 清空 scene_1 的坐标轴内容并绘图
        self.figure_1.clear()  # 清空当前 Figure 的内容
        self.plot_graph_1()  # 更新图表

        # 清空 scene_2 的坐标轴内容并绘图
        self.figure_2.clear()  # 清空当前 Figure 的内容
        self.plot_graph_2()  # 更新图表

        # 清空 scene_3 的坐标轴内容并绘图
        self.figure_3.clear()  # 清空当前 Figure 的内容
        self.plot_graph_3()  # 更新图表

        # 清空 scene_4 的坐标轴内容并绘图
        self.figure_4.clear()  # 清空当前 Figure 的内容
        self.plot_graph_4()  # 更新图表        

    def plot_graph_1(self):
        # 在 scene_1 的 axes 上绘制图表
        axes = self.figure_1.add_subplot(111)  # 在新创建的 Figure 上添加子图
        plot_four_line.plot_Ppm(axes, self.Ppm, self.Pgen)
        # 更新画布显示
        self.canvas_1.draw()

    def plot_graph_2(self):
        # 在 scene_2 的 axes 上绘制图表
        axes = self.figure_2.add_subplot(111)  # 在新创建的 Figure 上添加子图
        plot_four_line.plot_H2(axes, self.Pel, self.Pfc)
        # 更新画布显示
        self.canvas_2.draw()

    def plot_graph_3(self):
        # 在 scene_3 的 axes 上绘制图表
        axes = self.figure_3.add_subplot(111)  # 在新创建的 Figure 上添加子图
        plot_four_line.plot_bat(axes, self.Pdis, self.Pcha)
        # 更新画布显示
        self.canvas_3.draw()   

    def plot_graph_4(self):
        # 在 scene_4 的 axes 上绘制图表
        axes = self.figure_4.add_subplot(111)  # 在新创建的 Figure 上添加子图
        plot_four_line.plot_CAES(axes, self.Pcaes_d, self.Pcaes_g)
        # 更新画布显示
        self.canvas_4.draw()

    def update_first_row(self, Pel, Pfc, Ppm, Pgen, Pdis, Pcha, Pcaes_d, Pcaes_g):
        # 数据初始化
        self.Pel = Pel
        self.Pfc = Pfc
        self.Ppm = Ppm
        self.Pgen = Pgen
        self.Pdis = Pdis
        self.Pcha = Pcha
        self.Pcaes_d = Pcaes_d
        self.Pcaes_g = Pcaes_g

        # 遍历 Ppm 和 Pgen 数组，将它们显示到表格的第一行
        for i in range(24):
            # 保留三位小数
            self.Ppm[i] = f"{-self.Ppm[i]:.3f}" 
            self.Pgen[i] = f"{-self.Pgen[i]:.3f}"
            self.Pdis[i] = f"{self.Pdis[i]:.3f}"   
            self.Pcha[i] = f"{self.Pcha[i]:.3f}" 
            self.Pfc[i] = f"{self.Pfc[i]:.3f}"
            self.Pel[i] = f"{self.Pel[i]:.3f}"   
            self.Pcaes_g[i] = f"{self.Pcaes_g[i]:.3f}" 
            self.Pcaes_d[i] = f"{self.Pcaes_d[i]:.3f}"                                                 
            # 创建新的 QTableWidgetItem 并设置值
            item_ppm = QTableWidgetItem(str(self.Ppm[i] + self.Pgen[i]))  # 抽水蓄能出力
            item_bat = QTableWidgetItem(str(- self.Pdis[i] - self.Pcha[i]))  # 电化学储能出力
            item_H2 = QTableWidgetItem(str(- self.Pel[i] - self.Pfc[i]))  # 氢储能出力
            item_CAES = QTableWidgetItem(str(- self.Pcaes_d[i] - self.Pcaes_g[i]))  # 压缩空气储能出力
            
            # 设置数值
            self.tableWidget.setItem(0, i, item_ppm)  # 更新抽水蓄能出力
            self.tableWidget.setItem(1, i, item_bat)  # 更新电化学储能出力
            self.tableWidget.setItem(2, i, item_H2)  # 更新氢储能出力
            self.tableWidget.setItem(3, i, item_CAES)  # 更新压缩空气储能出力   



##--------------------------------------------界面3-----------------------------##             
class FrameGPTPage(QWidget, Ui_Form_gpt):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
       # 创建 ChatWindow 实例，并将其添加到 scrollArea 的布局中
        self.chat_window = ChatWindow(scroll_area=self.scrollArea)  # 传递 scrollArea
        self.scrollArea.setWidget(self.chat_window)

        # 监听input_Button点击事件
        self.input_Button.clicked.connect(self.send_text_to_chat)

        # 监听按键事件，允许按 Enter 键时也触发 send_text_to_chat
        self.input_textEdit.installEventFilter(self)  # 安装事件过滤器

    # 事件过滤器方法，监听键盘事件
    def eventFilter(self, source, event):
        if source is self.input_textEdit and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:  # 判断是否是 Enter 键
                self.send_text_to_chat()  # 调用发送消息的方法
                return True  # 表示事件已处理
        return super().eventFilter(source, event)
    
    # 将输入框文本发送到聊天窗口的方法
    def send_text_to_chat(self):
        input_text = self.input_textEdit.toPlainText()  # 获取输入框的文本内容
        if input_text:
            self.chat_window.add_chat_entry(input_text)  # 调用ChatWindow的方法添加聊天记录
            self.input_textEdit.clear()  # 清空输入框

##----------------------------------------GPT聊天窗口界面-------------------------------##
# 输入框窗口部件类
class InputWidget(QWidget):
    def __init__(self, parent=None, chat_obj=None):
        super().__init__(parent)
        # 初始化UI
        self.input_ui = Input_Form()
        self.input_ui.setupUi(self)

        # 将chat_obj传递进来，用于后续操作
        self.chat_obj = chat_obj

        # 获取UI中的控件
        self.input_label = self.input_ui.label_2  # 输入框标签

    # 设置输入文本
    def set_input_text(self, input_str):
        self.input_label.setText(input_str)



# 输出框窗口部件类
class OutWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 初始化UI
        self.out_ui = Out_Form()
        self.out_ui.setupUi(self)

        # 获取UI中的控件
        self.out_label = self.out_ui.label_2  # 输出框标签

    # 设置输出文本
    def set_output_text(self, out_str):
        self.out_label.setText(out_str)  # 将传入的文本显示到标签中

# 聊天窗口类
class ChatWindow(QWidget):
    def __init__(self, parent=None, chat_object=None, chat_data=None,scroll_area = None):
        super().__init__(parent)
        # 保存传入的参数
        self.chat_object = chat_object
        self.chat_data = chat_data
        self.scroll_area = scroll_area  # 获取 scrollArea 实例
        # 保存传入的参数
        self.chat_object = chat_object
        # print(self.chat_object)  # 输出调试信息
        self.chat_data = chat_data

        # 创建主垂直布局管理器
        self.main_verticalLayout = QVBoxLayout(self)
        self.main_verticalLayout.setContentsMargins(0, 0, 0, 0)  # 设置布局的边距为0
        self.main_verticalLayout.setSpacing(0)  # 设置部件之间的间距为0
        self.main_verticalLayout.setObjectName("main_verticalLayout")

        # # 定义样式
        # self.style_str = """
        # QPushButton,
        #     QLabel {
        #         border: none;
        #         padding: 5px;  # 设置控件的内边距
        #     }

        #     QWidget {
        #         background: #fff;  # 设置背景为白色
        #     }
        # """
        # self.setStyleSheet(self.style_str)  # 应用样式

        # 初始化聊天数据
        self.chats_data = {
            # "title": "",  # 聊天标题
            "chat_list": []  # 聊天记录列表
        }

        # 如果传入了chat_data，合并到聊天数据中
        # print(self.chats_data["chat_list"])  # 输出调试信息
        if self.chat_data:
            # self.chats_data["title"] = self.chat_data["title"]
            self.chats_data["chat_list"] += self.chat_data["chat_list"]

    # 新增方法，用于添加新的聊天记录
    def add_chat_entry(self, input_text):
        # 将新的聊天记录添加到 `chat_list`
        self.chats_data["chat_list"].append({
            "input_str": input_text,
            "out_str": "你好"
        })

        # 调用 `show_chats` 更新显示所有聊天记录
        self.show_chats()
 # 显示聊天记录
    def show_chats(self):
        # 清空当前布局中的所有内容
        for i in reversed(range(self.main_verticalLayout.count())):
            widget = self.main_verticalLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # 遍历聊天记录并显示
        for chat in self.chats_data["chat_list"]:
            input_str = chat.get("input_str")
            input_widget = InputWidget(chat_obj=self.chat_object)
            input_widget.set_input_text(input_str)
            input_widget.setFixedHeight(130)  # 统一高度
            self.main_verticalLayout.addWidget(input_widget)

            out_str = chat.get("out_str")
            out_widget = OutWidget()
            out_widget.set_output_text(out_str)
            out_widget.setFixedHeight(150)  # 统一高度            
            self.main_verticalLayout.addWidget(out_widget)

        # 使用 QTimer 延迟滚动到底部，确保布局更新完毕
        QTimer.singleShot(20, self.scroll_to_bottom)

        # 更新布局
        self.setLayout(self.main_verticalLayout)

    def scroll_to_bottom(self):
        """滚动到最底部，确保最新消息可见"""
        if self.scroll_area:
            self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

class QCustomSlideMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 初始化按钮
        self.pushButton_page1 = QPushButton("Page 1", self)
        self.pushButton_page2 = QPushButton("Page 2", self)
        self.pushButton = QPushButton("Page", self)

class MainWidget(QWidget, Ui_ui_main):
    """
    主窗口
    """
    def __init__(self):
        super().__init__()
        # self.setupUi(self)

        self.Pel = np.zeros(24)  # 初始化Pel
        self.Pfc = np.zeros(24)  # 初始化Pfc
        self.Ppm = np.zeros(24)  # 初始化 Pel
        self.Pgen = np.zeros(24)  # 初始化Pel
        self.Pdis = np.zeros(24)  # 初始化Pfc
        self.Pcha = np.zeros(24)  # 初始化 Pel
        self.Pcaes_d = np.zeros(24)  # 初始化Pel
        self.Pcaes_g = np.zeros(24)  # 初始化Pfc

        # 实例化一个堆叠布局
        # 在主界面中找到 QCustomSlideMenu 控件，初始化 leftMenuContainer
        self.leftMenuContainer = QCustomSlideMenu(self)  # self.ui 是从 Ui_ui_main 继承来的 UI 对象

        self.qsl = QStackedLayout(self.leftMenuContainer)
        # 实例化分页面
        self.home = FrameHomePage(self)
        self.blog = FrameBlogPage(self.Pel, self.Pfc, self.Ppm, self.Pgen, self.Pdis, self.Pcha, self.Pcaes_d, self.Pcaes_g)
        self.GPT = FrameGPTPage()
        # 加入到布局中
        self.qsl.addWidget(self.home)
        self.qsl.addWidget(self.blog)
        self.qsl.addWidget(self.GPT)
        # 控制函数
        self.controller()

        self.ui = self
        self.loadJsonStyle(self)

    def controller(self):
        # 实例化 QCustomSlideMenu
        self.leftMenuContainer = QCustomSlideMenu(self)
        self.pushButton_page1 = self.leftMenuContainer.pushButton_page1
        self.pushButton_page2 = self.leftMenuContainer.pushButton_page2 
        self.pushButton = self.leftMenuContainer.pushButton  
        self.pushButton_page1.clicked.connect(self.switch)    
        self.pushButton_page2.clicked.connect(self.switch)
        self.pushButton.clicked.connect(self.switch)


    def loadJsonStyle(widget, ui_data):
        if isinstance(ui_data, dict):
            # 假设这里根据字典内容设置界面样式
            style = ui_data.get("style", "")
            widget.setStyleSheet(style)
        else:
            print("UI data is not a dictionary.")
  

    def switch(self):
        sender = self.sender().objectName()

        index = {
            "pushButton_page1": 0,
            "pushButton_page2": 1,
            "pushButton": 2,
        }

        self.qsl.setCurrentIndex(index[sender])
            # 当切换到 blog 页时，更新数据
        if sender == "pushButton_page2":
            self.blog.update_data(self.Pel, self.Pfc, self.Ppm, self.Pgen, self.Pdis, self.Pcha, self.Pcaes_d, self.Pcaes_g)
            self.blog.update_first_row(self.Pel, self.Pfc, self.Ppm, self.Pgen, self.Pdis, self.Pcha, self.Pcaes_d, self.Pcaes_g)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 实例化主窗口并显示
    main_window = MainWidget()
    main_window.show()
    
    sys.exit(app.exec_())