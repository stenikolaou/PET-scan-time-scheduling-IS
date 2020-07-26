from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtGui import QIcon
import petapp as pa

class Ui_Login(object):
    def warning(self, title, message):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(QIcon("icons8-system-task-40.png"))
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def login(self):

        username=self.username.text()
        password=self.password.text()

        if username=="admin" and password=="pass":
            Login.hide()
            def main():

                self.app = QApplication(sys.argv)
                self.window = pa.PetApp()
                self.window.show()
                self.app.exec_()

            if __name__ == '__main__':
                main()
        else:
            self.warning("Warning", "Wrong username/password!")

    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(341, 469)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons8-enter-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Login.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(Login)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widget = QtWidgets.QWidget(Login)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 248, 249))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(25, 25, 40))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(204, 51, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(25, 25, 40))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(25, 25, 40))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 248, 249))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(25, 25, 40))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(204, 51, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(25, 25, 40))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(25, 25, 40))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(204, 51, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(25, 25, 40))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(204, 51, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(204, 51, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(204, 51, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(25, 25, 40))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(25, 25, 40))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.widget.setPalette(palette)
        self.widget.setStyleSheet(".QWidget{background-color: rgb(25,25, 40);}")
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(9, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 15, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(100, 150))
        self.label.setMaximumSize(QtCore.QSize(150, 150))
        self.label.setStyleSheet("image: url(:/icons/icons/rocket_48x48.png);")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/icons/icons8-enter-100.png"))
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setContentsMargins(50, 35, 59, -1)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setStyleSheet("color: rgb(231, 231, 231);\n"
"font: 15pt \"Verdana\";")
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/icons/icons8-user-shield-32.png"))
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.username = QtWidgets.QLineEdit(self.widget)
        self.username.setMinimumSize(QtCore.QSize(0, 40))
        self.username.setStyleSheet("QLineEdit {\n"
"      color: rgb(231, 231, 231);\n"
"      font: 15pt \"Verdana\";\n"
"      border: None;\n"
"      border-bottom-color: white;\n"
"      border-radius: 10px;\n"
"      padding: 0 8px;\n"
"      background: rgb(25, 25, 40);\n"
"      selection-background-color: darkgray;\n"
"}")
        self.username.setObjectName("username")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.username)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setStyleSheet("border: 2px solid white;")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.line)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setStyleSheet("color: rgb(231, 231, 231);\n"
"font: 15pt \"Verdana\";")
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/icons/icons8-password-32.png"))
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.password = QtWidgets.QLineEdit(self.widget)
        self.password.setMinimumSize(QtCore.QSize(0, 40))
        self.password.setStyleSheet("QLineEdit {\n"
"      color: white;\n"
"      font: 15pt \"Verdana\";\n"
"      border: None;\n"
"      border-bottom-color: white;\n"
"      border-radius: 10px;\n"
"      padding: 0 8px;\n"
"      background: rgb(25, 25, 40);\n"
"      selection-background-color: darkgray;\n"
"}")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.password)
        self.line_2 = QtWidgets.QFrame(self.widget)
        self.line_2.setStyleSheet("border: 2px solid white;")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.line_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_2.setItem(4, QtWidgets.QFormLayout.SpanningRole, spacerItem)
        self.loginButton = QtWidgets.QPushButton(self.widget)
        self.loginButton.setEnabled(True)
        self.loginButton.clicked.connect(self.login)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginButton.sizePolicy().hasHeightForWidth())
        self.loginButton.setSizePolicy(sizePolicy)
        self.loginButton.setMinimumSize(QtCore.QSize(0, 60))
        self.loginButton.setAutoFillBackground(False)
        self.loginButton.setStyleSheet("color: rgb(231, 231, 231);\n"
"font: 17pt \"Verdana\";\n"
"border: 2px solid purple;\n"
"padding: 5px;\n"
"border-radius: 3px;\n"
"opacity: 200;\n"
"")
        self.loginButton.setAutoDefault(False)
        self.loginButton.setDefault(False)
        self.loginButton.setFlat(False)
        self.loginButton.setObjectName("loginButton")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.loginButton)
        self.verticalLayout_3.addLayout(self.formLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.horizontalLayout_3.addWidget(self.widget)
        self.horizontalLayout_3.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Login "))
        self.loginButton.setText(_translate("Login", "Login"))
        self.loginButton.setShortcut(_translate("Login", "Enter"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Login = QtWidgets.QWidget()
    ui = Ui_Login()
    ui.setupUi(Login)
    Login.show()
    sys.exit(app.exec_())

