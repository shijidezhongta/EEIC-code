from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QTimer
from UI.gpt_in import Ui_Form as Input_Form
from UI.gpt_out import Ui_Form as Out_Form


class InputWidget(QWidget):
    def __init__(self, parent=None, chat_obj=None):
        super().__init__(parent)
        self.input_ui = Input_Form()
        self.input_ui.setupUi(self)
        self.input_label = self.input_ui.label_in

    def set_input_text(self, input_str):
        self.input_label.setText(input_str)


class OutWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.out_ui = Out_Form()
        self.out_ui.setupUi(self)

        self.out_label = self.out_ui.label_2

    def set_output_text(self, out_str):
        self.out_label.setText(out_str)


class ChatWindow(QWidget):
    def __init__(self, parent=None, chat_object=None, chat_data=None):
        super().__init__(parent)

        self.chat_object = chat_object
        self.chat_data = chat_data

        self.main_verticalLayout = QVBoxLayout(self)
        self.main_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.main_verticalLayout.setSpacing(0)
        self.main_verticalLayout.setObjectName("main_verticalLayout")

        self.chats_data = {
            "title": "",
            "chat_list": []
        }

        if self.chat_data:
            self.chats_data["title"] = self.chat_data["title"]
            self.chats_data["chat_list"] += self.chat_data["chat_list"]


        self.show_chats()

    def show_chats(self):
        chat_list = self.chats_data.get("chat_list")
        for chat in chat_list:
            input_str = chat.get("input_str")
            input_widget = InputWidget(chat_obj=self.chat_object)
            input_widget.set_input_text(input_str)
            # input_widget.setFixedHeight(130)  # 统一高度
            input_widget.adjustSize()  # 调整大小以适应内容
            self.main_verticalLayout.addWidget(input_widget)

            out_str = chat.get("out_str")
            out_widget = OutWidget()
            out_widget.set_output_text(out_str)
            # out_widget.setFixedHeight(150)  # 统一高度  
            out_widget.adjustSize()  # 调整大小以适应内容          
            self.main_verticalLayout.addWidget(out_widget)

        spacerItem = QSpacerItem(20, 293, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_verticalLayout.addItem(spacerItem)
        self.setLayout(self.main_verticalLayout)
    #     # 使用 QTimer 延迟滚动到底部，确保布局更新完毕
    #     QTimer.singleShot(20, self.scroll_to_bottom)

    #     # 更新布局
    #     self.setLayout(self.main_verticalLayout)

    # def scroll_to_bottom(self):
    #     """滚动到最底部，确保最新消息可见"""
    #     if self.scroll_area:
    #         self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
