# This is a Qt mailing program
# v1.0

from PySide2.QtWidgets import *

import sys
import threading

import smtplib
from email.mime.text import MIMEText
from email.header import Header

from email_box import SendMail


###############################################################

win_title = 'Mailing program'

window_min_height = 600
window_min_width = 500

coder = 'utf-8'

label_style = """
              vertical-align: middle;
              color: #555555;
              font-size: 12px;
              """

log_style = """
            background-color: #000000;
            color: #FFFFFF;
            font-family: Titillium;
            font-size: 12px;
            """

def_mail = 'ceo@company.com'
def_cc_mail = 'cto@company.com'
def_pass = 'mypassword!'
def_host = '192.168.1.1'
def_port = '465'

def_subject = 'Hello!'
def_letter = 'how are you today?'


###############################################################


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(win_title)
        self.statusBar().showMessage('Welcome!')
        # create menu
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu("File")
        file_menu.addAction("Open emails list")
        file_menu.triggered[QAction].connect(self.file_open)
        # central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        # self.setMinimumSize(window_min_width, window_min_height)
        vbox = QVBoxLayout(central_widget)
        # create subject label and field
        self.subject_label = QLabel('Subject:')
        self.subject_label.setStyleSheet(label_style)
        self.subject_field = QLineEdit(def_subject)
        # create letter label and field
        self.letter_label = QLabel('Letter:')
        self.letter_label.setStyleSheet(label_style)
        self.letter_field = QTextEdit(def_letter)
        # create term for log
        self.log_label = QLabel('Log:')
        self.log_label.setStyleSheet(label_style)
        self.term = QTextEdit()
        self.term.setReadOnly(True)
        self.term.setStyleSheet(log_style)
        # create email box
        self.send_mail = SendMail()
        self.send_mail.from_mail.setText(def_mail)
        self.send_mail.cc_mail.setText(def_cc_mail)
        self.send_mail.passwd.setText(def_pass)
        self.send_mail.host.setText(def_host)
        self.send_mail.port.setText(def_port)
        # 
        self.send_mail.btn_go.clicked.connect(self.start)
        # 
        vbox.addWidget(self.subject_label)
        vbox.addWidget(self.subject_field)
        vbox.addWidget(self.letter_label)
        vbox.addWidget(self.letter_field)
        vbox.addWidget(self.log_label)
        vbox.addWidget(self.term)
        vbox.addWidget(self.send_mail)
        #
        self.mail_list = []
        self.lock = 0    # used to lock button when mailing in progress
        
    def start(self):
        if not self.lock:
            t1 = threading.Thread(target=self.checking)
            t1.start()
        
    def checking(self):
        if not self.mail_list:
            self.term.insertPlainText('Please select file with e-mails\' list first!\r')
            self.term.ensureCursorVisible()
        else:
            subj = self.subject_field.text()
            msg = self.letter_field.toPlainText()
            host = self.send_mail.host.text()
            port = self.send_mail.port.text()
            from_email = self.send_mail.from_mail.text()
            cc_email = self.send_mail.cc_mail.text()
            pw = self.send_mail.passwd.text()
            if not subj:
                self.term.insertPlainText('Please fill in "Subject" field\r')
                self.term.ensureCursorVisible()
            if not msg:
                self.term.insertPlainText('Please fill in "Letter" field\r')
                self.term.ensureCursorVisible()
            if not host:
                self.term.insertPlainText('Please fill in "SMTP host" field\r')
                self.term.ensureCursorVisible()
            if not from_email:
                self.term.insertPlainText('Please fill in "From e-mail" field\r')
                self.term.ensureCursorVisible()
            if subj and msg and host and from_email:
                self.lock = 1    # lock button
                self.send_to_many(self.mail_list, from_email, cc_email, subj, msg, host, port, pw)

    def send_to_many(self, to_list, from_mail, cc_mail, sbj, text, smtp_host, smtp_port, pword):
        login_ok = 0
        self.send_mail.info_label.setStyleSheet('color: green;')
        self.send_mail.info_label.setText('In progress...')
        # Try to login to SMTP server
        try:
            s = smtplib.SMTP_SSL(smtp_host)
            s.login(from_mail, pword)
            login_ok = 1
        except Exception:
            self.term.insertPlainText('FAILED to login to SMTP server!\r')
            self.term.ensureCursorVisible()
            self.send_mail.info_label.setStyleSheet('color: red;')
            self.send_mail.info_label.setText('FAILED login to server')
        if login_ok:
            for item in to_list:
                try:
                    if item[0] and item[1]:
                        self.term.insertPlainText('Sending to: '+ item[0]+ ', '+ item[1]+ '...\r')
                        self.term.ensureCursorVisible()
                        msg = 'Hello ' + item[0].strip() + ', ' + text    # item[0] is a name
                        m = MIMEText(msg, 'plain', coder)
                        m['Subject'] = Header(sbj, coder)
                        m['From'] = from_mail.strip()
                        m['To'] = item[1].strip()    # item[1] is an e-mail
                        m['CC'] = cc_mail.strip()
                        to_addr = [item[1].strip()] + [cc_mail.strip()]    # add CC address
                        s.sendmail(from_mail, to_addr, m.as_string())
                except Exception:
                    self.term.insertPlainText('ERROR sending e-mail to ' + item[0] + ', ' + item[1] + '\r')
                    self.term.ensureCursorVisible()
            s.quit()
            self.term.insertPlainText('\rDONE\r\r')
            self.term.ensureCursorVisible()
            self.send_mail.info_label.setStyleSheet('color: green;')
            self.send_mail.info_label.setText('DONE')
            self.mail_list = []
        self.lock = 0

    def closeEvent(self, event):
        event.accept()

    def file_open(self):
        name = QFileDialog.getOpenFileName(self, 'Open')
        f_name = name[0]    # name of file to open (to parse)
        f_data = self.read_from_file(f_name)
        self.mail_list = self.convert_data(f_data)
    
    def read_from_file(self, filename):
        try:
            File = open(filename, 'r')
            data = File.read()
            File.close()
        except Exception:
            self.term.insertPlainText('Can not read file '+ filename + '\r')
            self.term.ensureCursorVisible()
            data = None
        return data

    def convert_data(self, data):
        new_data = []
        data = data.replace('\r', '\n')    # replace '\r' with '\n'
        data_list = data.split('\n')    # split data using separator '\n'
        for line in data_list:
            if len(line):
                line = line.split(';')
                new_data.append(line)
        return new_data


def main():
    app = QApplication([])
    main_win = MainWindow()
    main_win.resize(window_min_width, window_min_height)
    main_win.show()
    # sys.exit(app.exec())  # PySide6
    sys.exit(app.exec_())  # PySide2


if __name__ == '__main__':
    main()
