# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scrapygui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5.QtCore import QThread, QObject
from PyQt5 import QtCore, QtGui, QtWidgets
from get_item_xlsx import get_excel
import IPPool
import subprocess
import signal


class BackendThread(QObject):
    def __init__(self, p, textEdit):
        self.p = p
        self.textEdit = textEdit
        self.flag = True
        super().__init__()

    # 处理业务逻辑
    def run(self):
        while self.flag:
            if subprocess.Popen.poll(self.p) is None:  # 结束为-1，包含输出为空
                data = self.p.stdout.readline().decode('utf-8').strip()
                print(data)
            else:
                # print("爬虫结束")
                # 杀死子进程
                print("爬虫结束")
                self.p.terminate()
                self.p.kill()
                break

    def stop(self):
        self.flag = False


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.textWritten.emit(str(text))


class Ui_GroupBox(object):

    def __init__(self, group_box):
        self.crawling = False
        self.Crawl_Thread = QThread()
        self.verticalLayoutWidget = QtWidgets.QWidget(group_box)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.label_spider_name = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lineEdit_spider_name = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.label_current_depth = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lineEdit_current_depth = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.label_crawl_depth = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lineEdit_crawl_depth = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.label_keyword = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lineEdit_keyword = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.label_crawl_url = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lineEdit_crawl_url = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.pushButton_addurl = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.label_reviews_num = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lineEdit_min_num = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.label_Tilde = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lineEdit_max_num = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.label_stars = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lineEdit_min_stars = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.label_Tilde1 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lineEdit_max_stars = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.label_price = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lineEdit_min_price = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.label_Tilde2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lineEdit_max_price = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.label_proxy_url = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lineEdit_proxy = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.checkBox_lock_url = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.textEdit = QtWidgets.QTextEdit(group_box)
        self.label_cmd = QtWidgets.QLabel(group_box)
        self.checkBox_flush = QtWidgets.QCheckBox(group_box)
        self.pushButton_start_crawl = QtWidgets.QPushButton(group_box)
        self.pushButton_get_excel = QtWidgets.QPushButton(group_box)

    def setup_ui(self, group_box):
        group_box.setObjectName("GroupBox")
        group_box.resize(974, 652)
        font = QtGui.QFont()
        font.setPointSize(12)
        group_box.setFont(font)
        # 布局layout
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(4, 0, 961, 431))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout.setObjectName("horizontalLayout")
        # 爬虫名称
        self.label_spider_name.setFont(font)
        self.label_spider_name.setObjectName("label_spidername")
        self.horizontalLayout.addWidget(self.label_spider_name)

        self.lineEdit_spider_name.setFont(font)
        self.lineEdit_spider_name.setText(global_params["spider_name"])
        self.lineEdit_spider_name.setObjectName("lineEdit_spidername")
        self.horizontalLayout.addWidget(self.lineEdit_spider_name)
        # url当前深度
        self.label_current_depth.setFont(font)
        self.label_current_depth.setObjectName("label_current_depth")
        self.horizontalLayout.addWidget(self.label_current_depth)

        self.lineEdit_current_depth.setFont(font)
        self.lineEdit_current_depth.setText(str(global_params["start_depth"]))
        self.lineEdit_current_depth.setObjectName("lineEdit_current_depth")
        self.horizontalLayout.addWidget(self.lineEdit_current_depth)
        # 爬取深度
        self.label_crawl_depth.setFont(font)
        self.label_crawl_depth.setObjectName("label_crawl_depth")
        self.horizontalLayout.addWidget(self.label_crawl_depth)

        self.lineEdit_crawl_depth.setFont(font)
        self.lineEdit_crawl_depth.setText(str(global_params["crawl_depth"]))
        self.lineEdit_crawl_depth.setObjectName("lineEdit_crawl_depth")
        self.horizontalLayout.addWidget(self.lineEdit_crawl_depth)
        # 关键词
        self.label_keyword.setFont(font)
        self.label_keyword.setObjectName("label_keyword")
        self.horizontalLayout.addWidget(self.label_keyword)

        self.lineEdit_keyword.setFont(font)
        self.lineEdit_keyword.setText(global_params["keyword"])
        self.lineEdit_keyword.setObjectName("lineEdit_keyword")
        self.horizontalLayout.addWidget(self.lineEdit_keyword)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        # 爬取的url
        self.label_crawl_url.setFont(font)
        self.label_crawl_url.setObjectName("label_crawl_url")
        self.horizontalLayout_2.addWidget(self.label_crawl_url)

        self.lineEdit_crawl_url.setFont(font)
        self.lineEdit_crawl_url.setText("")
        self.lineEdit_crawl_url.setObjectName("lineEdit_crawl_url")
        self.horizontalLayout_2.addWidget(self.lineEdit_crawl_url)
        # 添加爬取url按钮
        self.pushButton_addurl.setFont(font)
        self.pushButton_addurl.setObjectName("pushButton_addurl")
        self.horizontalLayout_2.addWidget(self.pushButton_addurl)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        # 评价数量
        self.label_reviews_num.setFont(font)
        self.label_reviews_num.setObjectName("label_reviews_num")
        self.horizontalLayout_3.addWidget(self.label_reviews_num)
        # 最低评价数量
        self.lineEdit_min_num.setFont(font)
        self.lineEdit_min_num.setText(str(global_params["star_num_min_limit"]))
        self.lineEdit_min_num.setObjectName("lineEdit_min_num")
        self.horizontalLayout_3.addWidget(self.lineEdit_min_num)

        self.label_Tilde.setFont(font)
        self.label_Tilde.setObjectName("label_9")
        self.horizontalLayout_3.addWidget(self.label_Tilde)
        # 最高评价数量
        self.lineEdit_max_num.setFont(font)
        self.lineEdit_max_num.setText(str(global_params["star_num_max_limit"]))
        self.lineEdit_max_num.setObjectName("lineEdit_max_num")
        self.horizontalLayout_3.addWidget(self.lineEdit_max_num)
        # 评分
        self.label_stars.setFont(font)
        self.label_stars.setObjectName("label_stars")
        self.horizontalLayout_3.addWidget(self.label_stars)
        # 最低评分
        self.lineEdit_min_stars.setFont(font)
        self.lineEdit_min_stars.setText(str(global_params["star_min_limit"]))
        self.lineEdit_min_stars.setObjectName("lineEdit_min_stars")
        self.horizontalLayout_3.addWidget(self.lineEdit_min_stars)

        self.label_Tilde1.setFont(font)
        self.label_Tilde1.setObjectName("label_11")
        self.horizontalLayout_3.addWidget(self.label_Tilde1)
        # 最高评分
        self.lineEdit_max_stars.setFont(font)
        self.lineEdit_max_stars.setText(str(global_params["star_max_limit"]))
        self.lineEdit_max_stars.setObjectName("lineEdit_max_stars")
        self.horizontalLayout_3.addWidget(self.lineEdit_max_stars)
        # 价格
        self.label_price.setFont(font)
        self.label_price.setObjectName("label_price")
        self.horizontalLayout_3.addWidget(self.label_price)
        # 最低价格
        self.lineEdit_min_price.setFont(font)
        self.lineEdit_min_price.setText(str(global_params["price_min_limit"]))
        self.lineEdit_min_price.setObjectName("lineEdit_min_price")
        self.horizontalLayout_3.addWidget(self.lineEdit_min_price)

        self.label_Tilde2.setFont(font)
        self.label_Tilde2.setObjectName("label_13")
        self.horizontalLayout_3.addWidget(self.label_Tilde2)
        # 最高价格
        self.lineEdit_max_price.setFont(font)
        self.lineEdit_max_price.setText(str(global_params["price_max_limit"]))
        self.lineEdit_max_price.setObjectName("lineEdit_max_price")
        self.horizontalLayout_3.addWidget(self.lineEdit_max_price)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        # 代理url
        self.label_proxy_url.setFont(font)
        self.label_proxy_url.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_proxy_url)
        # 代理url
        self.lineEdit_proxy.setFont(font)
        self.lineEdit_proxy.setText(global_params["get_ip_url"])
        self.lineEdit_proxy.setObjectName("lineEdit_proxy")
        self.horizontalLayout_4.addWidget(self.lineEdit_proxy)
        self.checkBox_lock_url.setObjectName("checkBox_lock_url")
        self.horizontalLayout_4.addWidget(self.checkBox_lock_url)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.textEdit.setGeometry(QtCore.QRect(10, 440, 731, 191))
        self.textEdit.setObjectName("textEdit")
        self.label_cmd.setGeometry(QtCore.QRect(10, 410, 71, 31))
        self.label_cmd.setObjectName("label_cmd")
        self.checkBox_flush.setGeometry(QtCore.QRect(760, 480, 191, 31))
        self.checkBox_flush.setObjectName("checkBox_flush")
        self.pushButton_start_crawl.setGeometry(QtCore.QRect(780, 530, 141, 31))
        self.pushButton_start_crawl.setObjectName("pushButton_start_crawl")
        self.pushButton_get_excel.setGeometry(QtCore.QRect(780, 590, 141, 31))
        self.pushButton_get_excel.setObjectName("pushButton_get_excel")
        # 绑定各事件
        self.event_connect()
        self.retranslate_ui(group_box)
        QtCore.QMetaObject.connectSlotsByName(group_box)

    def event_connect(self):
        self.pushButton_addurl.clicked.connect(self.addurl)
        self.pushButton_start_crawl.clicked.connect(self.start_crawl)
        self.pushButton_get_excel.clicked.connect(self.get_excel)
        self.checkBox_lock_url.stateChanged.connect(self.lock_url)
        self.checkBox_flush.stateChanged.connect(self.is_flush_changed)

        sys.stdout = EmittingStream(textWritten=self.output_written)
        sys.stderr = EmittingStream(textWritten=self.output_written)

    def addurl(self):
        try:
            url = self.lineEdit_crawl_url.text()
            redis_key = self.lineEdit_spider_name.text() + ":start_urls"
            IPPool.push_url(redis_key, url)
            self.lineEdit_crawl_url.setText("")
            print("成功添加url至", redis_key)
        except:
            print("添加失败")

    def start_crawl(self):
        if not self.crawling:
            global_params["spider_name"] = self.lineEdit_spider_name.text()
            global_params["start_depth"] = int(self.lineEdit_current_depth.text())
            global_params["crawl_depth"] = int(self.lineEdit_crawl_depth.text())
            global_params["keyword"] = self.lineEdit_keyword.text()
            global_params["star_num_min_limit"] = int(self.lineEdit_min_num.text())
            global_params["star_num_max_limit"] = int(self.lineEdit_max_num.text())
            global_params["star_min_limit"] = float(self.lineEdit_min_stars.text())
            global_params["star_max_limit"] = float(self.lineEdit_max_stars.text())
            global_params["price_min_limit"] = float(self.lineEdit_min_price.text())
            global_params["price_max_limit"] = float(self.lineEdit_max_price.text())
            global_params["get_ip_url"] = self.lineEdit_proxy.text()

            self.p = subprocess.Popen("scrapy runspider -a spider_name={} -a start_depth={} -a crawl_depth={}\
            -a keyword={} -a star_num_min_limit={} -a star_num_max_limit={} -a star_min_limit={}\
             -a star_max_limit={} -a price_min_limit={} -a price_max_limit={} -s SCHEDULER_FLUSH_ON_START={} \
             spiders/amazonPostion.py".format(global_params["spider_name"], global_params["start_depth"],
                                              global_params["crawl_depth"], global_params["keyword"],
                                              global_params["star_num_min_limit"], global_params["star_num_max_limit"],
                                              global_params["star_min_limit"], global_params["star_max_limit"],
                                              global_params["price_min_limit"], global_params["price_max_limit"],
                                              global_params["is_flush"]),
                                 shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
            self.changed_ReadOnly(True)
            self.pushButton_start_crawl.setText("停止")
            self.spider = BackendThread(self.p, self.textEdit)
            self.spider.moveToThread(self.Crawl_Thread)
            self.Crawl_Thread.started.connect(self.spider.run)
            self.Crawl_Thread.start()
            self.crawling = True
        else:
            if self.p.poll():
                self.p.send_signal(signal.CTRL_C_EVENT)
                self.p.send_signal(signal.CTRL_C_EVENT)
            self.changed_ReadOnly(False)
            self.pushButton_start_crawl.setText("开始")
            self.crawling = False

    def changed_ReadOnly(self, changed):
        self.lineEdit_spider_name.setReadOnly(changed)
        self.lineEdit_crawl_depth.setReadOnly(changed)
        self.lineEdit_current_depth.setReadOnly(changed)

        self.lineEdit_min_price.setReadOnly(changed)
        self.lineEdit_min_stars.setReadOnly(changed)
        self.lineEdit_min_num.setReadOnly(changed)

        self.lineEdit_max_price.setReadOnly(changed)
        self.lineEdit_max_stars.setReadOnly(changed)
        self.lineEdit_max_num.setReadOnly(changed)

    def get_excel(self):
        if self.crawling:
            print("爬取中无法打印")
        else:
            get_excel(global_params["spider_name"])

    def lock_url(self, state):
        if state == QtCore.Qt.Unchecked:
            self.lineEdit_proxy.setReadOnly(False)
        elif state == QtCore.Qt.Checked:
            self.lineEdit_proxy.setReadOnly(True)

    def is_flush_changed(self, state):
        try:
            if state == QtCore.Qt.Unchecked:
                global_params["is_flush"] = False
            elif state == QtCore.Qt.Checked:
                global_params["is_flush"] = True
        except:
            pass

    def output_written(self, text):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()

    def retranslate_ui(self, GroupBox):
        _translate = QtCore.QCoreApplication.translate
        GroupBox.setWindowTitle(_translate("GroupBox", "GroupBox"))
        self.label_spider_name.setText(_translate("GroupBox", "爬虫名"))
        self.label_current_depth.setText(_translate("GroupBox", "当前分级"))
        self.label_crawl_depth.setText(_translate("GroupBox", "爬取分级"))
        self.label_keyword.setText(_translate("GroupBox", "关键词"))
        self.label_crawl_url.setText(_translate("GroupBox", "网页链接"))
        self.pushButton_addurl.setText(_translate("GroupBox", "addurl"))
        self.label_reviews_num.setText(_translate("GroupBox", "评价数量"))
        self.label_Tilde.setText(_translate("GroupBox", "~"))
        self.label_stars.setText(_translate("GroupBox", "评分"))
        self.label_Tilde1.setText(_translate("GroupBox", "~"))
        self.label_price.setText(_translate("GroupBox", "价格"))
        self.label_Tilde2.setText(_translate("GroupBox", "~"))
        self.label_proxy_url.setText(_translate("GroupBox", "IP代理url"))
        self.checkBox_lock_url.setText(_translate("GroupBox", "锁定"))
        self.label_cmd.setText(_translate("GroupBox", "控制台"))
        self.checkBox_flush.setText(_translate("GroupBox", "清除上次爬取记录"))
        self.pushButton_start_crawl.setText(_translate("GroupBox", "开始爬取"))
        self.pushButton_get_excel.setText(_translate("GroupBox", "打印至Excel"))
        # 设置只能输入int或double类型的数据
        self.lineEdit_min_num.setValidator(QtGui.QIntValidator())
        self.lineEdit_max_num.setValidator(QtGui.QIntValidator())
        self.lineEdit_current_depth.setValidator(QtGui.QIntValidator())
        self.lineEdit_crawl_depth.setValidator(QtGui.QIntValidator())
        self.lineEdit_min_stars.setValidator(QtGui.QDoubleValidator())
        self.lineEdit_max_stars.setValidator(QtGui.QDoubleValidator())
        self.lineEdit_min_price.setValidator(QtGui.QDoubleValidator())
        self.lineEdit_max_price.setValidator(QtGui.QDoubleValidator())
        # 限制spider name输入只能为数字、字母下划线"^\w+$"
        my_regex = QtCore.QRegExp("^\\w+$")
        my_validator = QtGui.QRegExpValidator(my_regex, self.lineEdit_spider_name)
        self.lineEdit_spider_name.setValidator(my_validator)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    global_params = {
        "spider_name": "spider_name", "star_num_min_limit": 0, "star_num_max_limit": 1000,
        "star_min_limit": 4.3, "star_max_limit": 5.0, "price_min_limit": 15, "price_max_limit": 100,
        "crawl_depth": 0, "start_depth": 0, "keyword": "", "is_flush": False,
        "get_ip_url": ""}
    ui = Ui_GroupBox(widget)
    ui.setup_ui(widget)
    widget.show()
    sys.exit(app.exec_())
    # 不同爬虫任务不同名称,爬取不同url时需更换，否则爬取结果将混在一起
    # spider_name = "spider_name"
    # 获取动态ip
    # get_ip_url = ''
    # 获取时间间隔
    # Thread_sleep_time = 5.5
    # 好评数量不小于
    # star_num_min_limit = 0
    # 好评数量不大于
    # star_num_max_limit = 1000
    # 评分不小于
    # star_min_limit = 4.3
    # 评分不大于
    # star_max_limit = 5.0
    # 价格不低于
    # price_min_limit = 0
    # 价格不高于
    # price_max_limit = 0
    # 爬取至几级分类
    # crawl_depth = 0
    # 输入的url的当前类级
    # start_depth = 0
    # 关键词
    # keyword = ''
    # 是否清除之前爬取记录
    # is_flush = False
