# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_dlg_create_table.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dlg_create_category(object):
    def setupUi(self, dlg_create_category):
        dlg_create_category.setObjectName("dlg_create_category")
        dlg_create_category.resize(337, 69)
        dlg_create_category.setMaximumSize(QtCore.QSize(577, 69))
        self.verticalLayout = QtWidgets.QVBoxLayout(dlg_create_category)
        self.verticalLayout.setObjectName("verticalLayout")
        self.led_category_name = QtWidgets.QLineEdit(dlg_create_category)
        self.led_category_name.setObjectName("led_category_name")
        self.verticalLayout.addWidget(self.led_category_name)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_ok = QtWidgets.QPushButton(dlg_create_category)
        self.btn_ok.setObjectName("btn_ok")
        self.horizontalLayout.addWidget(self.btn_ok)
        self.btn_cancel = QtWidgets.QPushButton(dlg_create_category)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(dlg_create_category)
        QtCore.QMetaObject.connectSlotsByName(dlg_create_category)

    def retranslateUi(self, dlg_create_category):
        _translate = QtCore.QCoreApplication.translate
        dlg_create_category.setWindowTitle(_translate("dlg_create_category", "Dialog"))
        self.btn_ok.setText(_translate("dlg_create_category", "Создать"))
        self.btn_cancel.setText(_translate("dlg_create_category", "Отмена"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlg_create_category = QtWidgets.QDialog()
    ui = Ui_dlg_create_category()
    ui.setupUi(dlg_create_category)
    dlg_create_category.show()
    sys.exit(app.exec_())
