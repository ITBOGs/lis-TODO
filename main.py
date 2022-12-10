import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QListWidgetItem

from design_MainWindow import Ui_MainWindow
from sqlquery import SqlQuery

from createCategoryWindow import DlgCreateCategory

class LisTodo(QMainWindow):
	def __init__(self, flag_db: int):
		super(LisTodo, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		if flag_db:
			sql_query.create_table()
			self.refresh_category_list()

			self.ui.btn_refresh_category_list.clicked.connect(lambda: self.refresh_category_list())
			self.ui.btn_refresh_task_list.clicked.connect(lambda: self.refresh_task_list())
			self.ui.btn_add_category.clicked.connect(lambda: self.create_category())
		else:
			self.setWindowTitle('Нет подключения к БД')
			self.mes_box('Нет подключения к БД')

	def refresh_category_list(self) -> None:
		self.ui.lis_wid_category.clear()
		lis_category = sql_query.get_category()

		first_item = None

		for category_name in lis_category:
			if not first_item:
				first_item = QListWidgetItem(*category_name)
				self.ui.lis_wid_category.addItem(first_item)
			else:
				self.ui.lis_wid_category.addItem(*category_name)

		self.ui.lis_wid_category.setCurrentItem(first_item)

	def refresh_task_list(self) -> None:
		self.ui.lis_wid_task.clear()

		if self.ui.lis_wid_category.count() != 0:
			category_name = self.ui.lis_wid_category.currentItem().text()
			lis_task = sql_query.get_task(category_name)

			for task_name in lis_task:
				self.ui.lis_wid_task.addItem(*task_name)
		else:
			self.mes_box('Не выбрана категория')

	def create_category(self):
		dlg_create_table = DlgCreateCategory()
		dlg_create_table.exec()

		self.refresh_category_list()

	@staticmethod
	def mes_box(mes_text: str) -> None:
		msg = QMessageBox()
		msg.setWindowTitle('Предупреждение')
		msg.setText(mes_text)

		msg.exec()

	def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
		sql_query.db_disconnect()


if __name__ == '__main__':
	sql_query = SqlQuery()

	app = QApplication(sys.argv)
	window = LisTodo(sql_query.db_connect())
	window.show()

	sys.exit(app.exec())
