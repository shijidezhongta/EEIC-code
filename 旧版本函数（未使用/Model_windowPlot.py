import sys
from random import randint
from PyQt5.QtChart import QChartView, QChart, QBarSeries, QBarSet, QBarCategoryAxis, QStackedBarSeries, QLineSeries,QValueAxis
from PyQt5.QtCore import Qt, QPointF, QRectF, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QGraphicsLineItem, QWidget, QHBoxLayout, QLabel, QVBoxLayout, QGraphicsProxyWidget

import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout
from PyQt5.QtChart import QChartView, QLineSeries, QChart, QValueAxis
from PyQt5.QtGui import QPainter

import Model_solving_cplex
class ToolTipItem(QWidget):
    def __init__(self, color, text, parent=None):
        super(ToolTipItem, self).__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        clabel = QLabel(self)
        clabel.setMinimumSize(12, 12)
        clabel.setMaximumSize(12, 12)
        clabel.setStyleSheet("border-radius:6px;background: rgba(%s,%s,%s,%s);" % (
            color.red(), color.green(), color.blue(), color.alpha()))
        layout.addWidget(clabel)
        self.textLabel = QLabel(text, self, styleSheet="color:white;")
        layout.addWidget(self.textLabel)

    def setText(self, text):
        self.textLabel.setText(text)


class ToolTipWidget(QWidget):
    Cache = {}

    def __init__(self, *args, **kwargs):
        super(ToolTipWidget, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("ToolTipWidget{background: rgba(50, 50, 50, 100);}")
        layout = QVBoxLayout(self)
        self.titleLabel = QLabel(self, styleSheet="color:white;")
        layout.addWidget(self.titleLabel)

    def updateUi(self, title, bars):
        self.titleLabel.setText(title)
        for bar, value in bars:
            if bar not in self.Cache:
                item = ToolTipItem(
                    bar.color(),
                    (bar.label() or "-") + ":" + str(value), self)
                self.layout().addWidget(item)
                self.Cache[bar] = item
            else:
                self.Cache[bar].setText(
                    (bar.label() or "-") + ":" + str(value))
            brush = bar.brush()
            color = brush.color()
            self.Cache[bar].setVisible(color.alphaF() == 1.0)  # 隐藏那些不可用的项
        self.adjustSize()  # 调整大小


class GraphicsProxyWidget(QGraphicsProxyWidget):
    def __init__(self, *args, **kwargs):
        super(GraphicsProxyWidget, self).__init__(*args, **kwargs)
        self.setZValue(999)
        self.tipWidget = ToolTipWidget()
        self.setWidget(self.tipWidget)
        self.hide()

    def width(self):
        return self.size().width()

    def height(self):
        return self.size().height()

    def show(self, title, bars, pos):
        self.setGeometry(QRectF(pos, self.size()))
        self.tipWidget.updateUi(title, bars)
        super(GraphicsProxyWidget, self).show()


class ChartView(QChartView):
    def __init__(self, names, data, *args, **kwargs):
        super(ChartView, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        self.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.categories = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 
                           '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
        self.iniChart(names, data)

        # 提示widget
        self.toolTipWidget = GraphicsProxyWidget(self._chart)

        # line 宽度需要调整
        self.lineItem = QGraphicsLineItem(self._chart)
        pen = QPen(Qt.gray)
        self.lineItem.setPen(pen)
        self.lineItem.setZValue(998)
        self.lineItem.hide()

        # 一些固定计算，减少mouseMoveEvent中的计算量
        axisX, axisY = self._chart.axisX(), self._chart.axisY()
        self.category_len = len(axisX.categories())
        self.min_x, self.max_x = -0.5, self.category_len - 0.5
        self.min_y, self.max_y = axisY.min(), axisY.max()
        self.point_top = self._chart.mapToPosition(QPointF(self.min_x, self.max_y))

    def mouseMoveEvent(self, event):
        super(ChartView, self).mouseMoveEvent(event)
        pos = event.pos()
        x = self._chart.mapToValue(pos).x()
        y = self._chart.mapToValue(pos).y()
        index = round(x)
        serie = self._chart.series()[0]
        bars = [(bar, bar.at(index))
                for bar in serie.barSets() if self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y]

        if bars:
            right_top = self._chart.mapToPosition(QPointF(self.max_x, self.max_y))
            step_x = round((right_top.x() - self.point_top.x()) / self.category_len)
            posx = self._chart.mapToPosition(QPointF(x, self.min_y))
            self.lineItem.setLine(posx.x(), self.point_top.y(), posx.x(), posx.y())
            self.lineItem.show()
            title = self.categories[index] if 0 <= index < len(self.categories) else ""
            t_width = self.toolTipWidget.width()
            t_height = self.toolTipWidget.height()
            x = pos.x() - t_width if self.width() - pos.x() - 20 < t_width else pos.x()
            y = pos.y() - t_height if self.height() - pos.y() - 20 < t_height else pos.y()
            self.toolTipWidget.show(title, bars, QPoint(x, y))
        else:
            self.toolTipWidget.hide()
            self.lineItem.hide()

    def iniChart(self, names, data):
        # 创建图表和视图
        chart_bar = QChart()
        chart_bar.setTitle("堆叠柱状图")
        series = QStackedBarSeries()

        self._chart = QChart(title="柱状图堆叠")
        self._chart.setAcceptHoverEvents(True)
        self._chart.setAnimationOptions(QChart.SeriesAnimations)

        series = QStackedBarSeries(self._chart)

        for name in names:
            bar = QBarSet(name)
            for day_data in data:
                bar.append(day_data[names.index(name)])  # 使用不同的值
            series.append(bar)

        self._chart.addSeries(series)
        self._chart.createDefaultAxes()  # 创建默认的轴

        axis_x = QBarCategoryAxis(self._chart)
        axis_x.append(self.categories)
        self._chart.setAxisX(axis_x, series)
        axis_x.setTitleText("时间(h)")  # 

        # 设置自定义 Y 轴范围
        axis_y = QValueAxis(self._chart)
        axis_y.setRange(-300, 700)  # 设置 Y 轴的范围
        axis_y.setTitleText("功率 (kW)")  # 可选：设置 Y 轴标题
        self._chart.setAxisY(axis_y, series)

        legend = self._chart.legend()
        legend.setVisible(True)
        self.setChart(self._chart)


class LineChartDialog(QDialog):
    def __init__(self, names, data):
        super(LineChartDialog, self).__init__()
        self.setWindowTitle('负荷数据图表')
        self.setGeometry(250, 250, 1800, 1000)

        # 创建 ChartView
        self.chart_view = ChartView(names, data)
        
        layout = QVBoxLayout()
        layout.addWidget(self.chart_view)
        self.setLayout(layout)


def create_bar_chart(names, data):
    dialog = LineChartDialog(names, data)  # 创建新窗口并传入数据
    dialog.exec_()  # 显示窗口


# if __name__ == '__main__':
#     app = QApplication(sys.argv)

#     # 假设您有多个系列（例如，每小时的负荷数据），下面是一些示例
#     names,ST = test_copy.Model_solving()
#     create_bar_chart(names, ST.T)

#     sys.exit(app.exec_())

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("主窗口")
        self.setGeometry(100, 100, 400, 200)

        # 创建一个按钮
        self.button = QPushButton("显示图表")
        self.button.clicked.connect(self.on_button_clicked)  # 连接按钮点击事件

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_button_clicked(self):
        names, ST = Model_solving_cplex.Model_solving()  # 取得数据
        create_bar_chart(names, ST.T)  # 显示图表窗口

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()  # 创建主窗口实例
    main_window.show()  # 显示主窗口
    sys.exit(app.exec_())  # 运行应用程序
