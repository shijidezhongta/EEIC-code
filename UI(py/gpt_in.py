# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gpt_in.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1127, 157)
        Form.setStyleSheet("#Form{\n"
" background:#3c4856\n"
"}\n"
"\n"
"#label_2{\n"
"    color: white;  /* 设置字体颜色为白色 */\n"
"    font-family: \'SimSun\', sans-serif;  /* 设置字体为宋体 */\n"
"    font-size: 20px;  /* 设置字体大小为28px */\n"
"}")
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(0, 10, 0, 10)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(40, 40))
        self.label.setMaximumSize(QtCore.QSize(120, 120))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.label.setFont(font)
        self.label.setStyleSheet("#label {\n"
"    font-size: 36px;                 /* 字体大小 */\n"
"}")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/GPT/account_circle_24dp_FFFFFF_FILL0_wght400_GRAD0_opsz24.svg"))
        self.label.setScaledContents(True)
        self.label.setWordWrap(True)
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 81, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.label_in = QtWidgets.QLabel(self.frame)
        self.label_in.setMinimumSize(QtCore.QSize(600, 0))
        self.label_in.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_in.setStyleSheet("#label_in{\n"
"    color: white;                    /* 白色文字 */\n"
"    border: none;  /* 半透明白色边框，边框变细 */\n"
"    border-radius: 10px;             /* 圆角效果 */\n"
"    padding: 10px 20px;              /* 内边距 */\n"
"    font-size: 24px;                 /* 字体大小 */\n"
"    font-weight: bold;               /* 加粗字体 */\n"
"}")
        self.label_in.setScaledContents(False)
        self.label_in.setWordWrap(True)
        self.label_in.setObjectName("label_in")
        self.gridLayout.addWidget(self.label_in, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_in.setText(_translate("Form", "TextLabel"))
import gpt_rc
