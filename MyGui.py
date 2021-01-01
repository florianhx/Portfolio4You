
from PyQt5 import QtCore, QtGui, QtWidgets
from Portfolio4You import main 

#sets up a GUI to get the user inputs that are necessary to create the pdf file
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1000,700)
        self.IT = QtWidgets.QCheckBox(Dialog)
        self.IT.setGeometry(QtCore.QRect(60, 220, 81, 20))
        self.IT.setObjectName("IT")
        self.Finance = QtWidgets.QCheckBox(Dialog)
        self.Finance.setGeometry(QtCore.QRect(60, 250, 81, 20))
        self.Finance.setObjectName("Finance")
        self.Consume = QtWidgets.QCheckBox(Dialog)
        self.Consume.setGeometry(QtCore.QRect(60, 280, 81, 20))
        self.Consume.setObjectName("Consume")
        self.Health = QtWidgets.QCheckBox(Dialog)
        self.Health.setGeometry(QtCore.QRect(60, 310, 81, 20))
        self.Health.setObjectName("Health")
        self.Clean = QtWidgets.QCheckBox(Dialog)
        self.Clean.setGeometry(QtCore.QRect(60, 340, 111, 20))
        self.Clean.setObjectName("Clean")
        self.EM = QtWidgets.QCheckBox(Dialog)
        self.EM.setGeometry(QtCore.QRect(60, 370, 191, 20))
        self.EM.setObjectName("EM")
        self.DIV = QtWidgets.QCheckBox(Dialog)
        self.DIV.setGeometry(QtCore.QRect(60, 400, 211, 20))
        self.DIV.setObjectName("DIV")
        self.Generate = QtWidgets.QPushButton(Dialog)
        self.Generate.setGeometry(QtCore.QRect(60, 480, 131, 28))
        self.Generate.setObjectName("Generate")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(320, 80, 670, 61))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(320, 140, 670, 61))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(320, 250, 421, 111))
        self.label_3.setObjectName("label_3")
        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setGeometry(QtCore.QRect(60, 100, 42, 22))
        self.spinBox.setMaximum(100)
        self.spinBox.setProperty("value", 60)
        self.spinBox.setObjectName("spinBox")
        self.spinBox_2 = QtWidgets.QSpinBox(Dialog)
        self.spinBox_2.setGeometry(QtCore.QRect(60, 160, 42, 22))
        self.spinBox_2.setMaximum(100)
        self.spinBox_2.setProperty("value", 70)
        self.spinBox_2.setObjectName("spinBox_2")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(130, 15, 541, 51))
        self.label_4.setText("")
        self.label_4.setTextFormat(QtCore.Qt.PlainText)
        self.label_4.setObjectName("label_4")


        self.Generate.clicked.connect(self.gedrueckt)

        

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "User Preferences"))
        self.IT.setText(_translate("Dialog", "IT"))
        self.Finance.setText(_translate("Dialog", "Finance"))
        self.Consume.setText(_translate("Dialog", "Consume"))
        self.Health.setText(_translate("Dialog", "Health"))
        self.Clean.setText(_translate("Dialog", "Clean Energy"))
        self.EM.setText(_translate("Dialog", "Emerging Markets"))
        self.DIV.setText(_translate("Dialog", "Prefere Dividend paying Stocks"))
        self.Generate.setText(_translate("Dialog", "Generate Portfolio"))
        self.label.setText(_translate("Dialog", "How much of your indiviual portfolio, should contain highly diversified ETF's ? (MSCI World , S & P 500, Nasdaq100)" ))
        self.label_2.setText(_translate("Dialog", "Choose for the remaining portfolio, the percentage of ETF's in your branch specific portfolio."))
        self.label_3.setText(_translate("Dialog", "Choose the branches you would like to invest in "))


    def gedrueckt(self,Dialog):
        basic=self.spinBox.value() / 100
        etf = self.spinBox_2.value() / 100
        cat_list=  []
        div = False
        if self.IT.isChecked():
            cat_list.append("IT")
        if self.Finance.isChecked():
            cat_list.append("Finance")
        if self.Consume.isChecked():
            cat_list.append("Consume")
        if self.Health.isChecked():
            cat_list.append("Health")
        if self.Clean.isChecked():
            cat_list.append("Clean")
        if self.EM.isChecked():
            cat_list.append("EM")
        if self.DIV.isChecked():
            div = True
        main(cat_list=cat_list,basic=basic,etf=etf,div=div)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

