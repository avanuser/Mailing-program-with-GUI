# SendMail class

from PySide2.QtCore import Qt
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon

#################################

label_style = """
              vertical-align: middle;
              color: #555555;
              """

#################################


class SendMail(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setTitle('Mailing settings')
        # add layout
        layout = QGridLayout(self)
        #
        # Line 0:
        #
        self.info_label = QLabel()
        self.info_label.setMinimumWidth(100)
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label, 0, 0)
        #
        self.from_mail_label = QLabel('From e-mail: ')
        self.from_mail_label.setStyleSheet(label_style)
        layout.addWidget(self.from_mail_label, 0, 1)
        #
        self.from_mail = QLineEdit()
        self.from_mail.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.from_mail, 0, 2)
        #
        self.btn_go = QToolButton()                                     
        self.btn_go.setCheckable(False)                                  
        self.btn_go.setChecked(False)
        self.btn_go.setAutoRaise(False)
        self.btn_go.setIcon(QIcon("res/go.png"))
        layout.addWidget(self.btn_go, 0, 3)
        #
        # Line 1:
        #
        self.cc_mail_label = QLabel('CC e-mail: ')
        self.cc_mail_label.setStyleSheet(label_style)
        layout.addWidget(self.cc_mail_label, 1, 1)
        #
        self.cc_mail = QLineEdit()
        self.cc_mail.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.cc_mail, 1, 2)
        #
        # Line 2:
        #
        self.pass_label = QLabel('Password: ')
        self.pass_label.setStyleSheet(label_style)
        layout.addWidget(self.pass_label, 2, 1)
        #
        self.passwd = QLineEdit()
        self.passwd.setAlignment(Qt.AlignCenter)
        self.passwd.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.passwd, 2, 2)
        #
        # Line 3:
        #
        self.host_label = QLabel('SMTP host: ')
        self.host_label.setStyleSheet(label_style)
        layout.addWidget(self.host_label, 3, 1)
        #
        self.host = QLineEdit()
        self.host.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.host, 3, 2)
        #
        # Line 4:
        #
        self.port_label = QLabel('SMTP port: ')
        self.port_label.setStyleSheet(label_style)
        layout.addWidget(self.port_label, 4, 1)
        #
        self.port = QLineEdit()
        self.port.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.port, 4, 2)
        #
