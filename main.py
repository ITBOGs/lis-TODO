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
			self.ui.btn_add_task.clicked.connect(lambda: self.create_task_menu())
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

	def create_task_menu(self):
		self.ui.ted_description_task.clear()
		self.ui.led_name_task.clear()

		self.ui.lis_wid_task.setDisabled(True)

		self.ui.btn_edit_task.setText('Создать задачу')
		self.ui.btn_del_task.setText('Отмена')
		self.ui.btn_complete_task.hide()

		self.ui.btn_edit_task.clicked.connect(lambda: self.create_task())
		self.ui.btn_del_task.clicked.connect(lambda: self.cancel_create_task())

	def create_task(self) -> None:
		category_name = self.ui.lis_wid_category.currentItem().text()
		task_name = self.ui.led_name_task.text()
		description = self.ui.ted_description_task.toPlainText()

		if category_name and task_name and description:
			sql_query.insert_task(task_name, description, category_name)

		else:
			if not category_name:
				self.mes_box('Не выбрана категория')
			if not task_name:
				self.ui.led_name_task.setText('Введите название')
			if not description:
				self.ui.ted_description_task.setText('Введите описание')

	def cancel_create_task(self) -> None:
		self.ui.ted_description_task.clear()
		self.ui.led_name_task.clear()

		self.ui.lis_wid_task.setDisabled(False)

		self.ui.btn_edit_task.setText('Изменить задачу')
		self.ui.btn_del_task.setText('Удалить задачу')
		self.ui.btn_complete_task.show()

		self.ui.btn_edit_task.disconnect()
		self.ui.btn_del_task.disconnect()
		# self.ui.btn_edit_task.clicked.connect(lambda: self.create_task())
		# self.ui.btn_del_task.clicked.connect(lambda: self.cancel_create_task())


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
