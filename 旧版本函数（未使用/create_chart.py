import sys
from random import randint
from PyQt5.QtChart import QChartView, QChart, QBarSeries, QBarSet, QBarCategoryAxis, QStackedBarSeries, QLineSeries,QValueAxis
from PyQt5.QtCore import Qt, QPointF, QRectF, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QGraphicsLineItem, QWidget, QHBoxLayout, QLabel, QVBoxLayout, QGraphicsProxyWidget

#---------------------------------------柱状图---------------------------#
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
        self.categories = ['1', '2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']
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

    def handleMarkerClicked(self):
        marker = self.sender()
        if not marker:
            return
        bar = marker.barset()
        if not bar:
            return
        brush = bar.brush()
        color = brush.color()
        alpha = 0.0 if color.alphaF() == 1.0 else 1.0
        color.setAlphaF(alpha)
        brush.setColor(color)
        bar.setBrush(brush)

        brush = marker.labelBrush()
        color = brush.color()
        alpha = 0.4 if color.alphaF() == 1.0 else 1.0
        color.setAlphaF(alpha)
        brush.setColor(color)
        marker.setLabelBrush(brush)

        brush = marker.brush()
        color = brush.color()
        color.setAlphaF(alpha)
        brush.setColor(color)
        marker.setBrush(brush)

    def handleMarkerHovered(self, status):
        marker = self.sender()
        if not marker:
            return
        bar = marker.barset()
        if not bar:
            return
        pen = bar.pen()
        if not pen:
            return
        pen.setWidth(pen.width() + (1 if status else -1))
        bar.setPen(pen)

    def handleBarHoverd(self, status, index):
        bar = self.sender()
        pen = bar.pen()
        if not pen:
            return
        pen.setWidth(pen.width() + (1 if status else -1))
        bar.setPen(pen)
#iniChart(self, names, data)
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
            bar.hovered.connect(self.handleBarHoverd)

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
        for marker in legend.markers():
            marker.clicked.connect(self.handleMarkerClicked)
            marker.hovered.connect(self.handleMarkerHovered)
        self.setChart(self._chart)
            # 图表视图设置
        view = QChartView(chart_bar)
        view.setRenderHint(QPainter.Antialiasing)
        

def create_bar_chart(names, data):
    app = QApplication(sys.argv)
    view = ChartView(names, data)
    view.show()
    sys.exit(app.exec_())


#-------------------------------------------折线图—---------------------------------#
def create_line_chart(data):
    app = QApplication(sys.argv)
    
    chart = QChart()
    chart.setTitle('负荷数据')

    # 创建一个线系列并添加数据
    series = QLineSeries()
    series.setName("负荷")  # 设置折线标签
    for x, y in data:
        series.append(x, y)

    chart.addSeries(series)

    # 设置默认坐标轴
    chart.createDefaultAxes()

    # 创建并设置y轴范围
    y_axis = QValueAxis()
    y_axis.setRange(0, 500)  # 设置y轴范围，例如150到350
    chart.setAxisY(y_axis, series)  # 将y轴设置到系列上
    chart.setAxisX(QValueAxis(), series)  # 也可以设置x轴范围，虽然这里不强制

    # 创建图表视图并显示
    view = QChartView(chart)
    view.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
    view.resize(800, 600)
    view.show()
    
    sys.exit(app.exec_())