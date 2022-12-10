from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog

from design_dlg_create_table import Ui_dlg_create_category
from sqlquery import SqlQuery


class DlgCreateCategory(QDialog):
	def __init__(self):
		super(DlgCreateCategory, self).__init__()
		self.ui = Ui_dlg_create_category()
		self.ui.setupUi(self)

		self.sql_query = SqlQuery()  # Не нравится мне это двойное подключение к БД, но пока поебать
		self.sql_query.db_connect()

		self.setWindowTitle('Создать категорию')
		self.ui.btn_ok.clicked.connect(lambda: self.create_category())
		self.ui.btn_cancel.clicked.connect(lambda: self.cancel())

	def create_category(self):
		if self.ui.led_category_name.text():
			self.sql_query.insert_category(self.ui.led_category_name.text())
			self.close()
		else:
			self.ui.led_category_name.setText('Введите название')

	def cancel(self) -> None:
		self.close()

	def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
		self.sql_query.db_disconnect()
