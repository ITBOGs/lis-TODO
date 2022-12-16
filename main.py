import sys
from typing import Union

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
			self.refresh_task_list()

			self.ui.btn_refresh_category_list.clicked.connect(lambda: self.refresh_category_list())
			self.ui.btn_refresh_task_list.clicked.connect(lambda: self.refresh_task_list())
			self.ui.btn_add_category.clicked.connect(lambda: self.create_category())
			self.ui.btn_add_task.clicked.connect(lambda: self.create_task_menu())
			self.ui.btn_del_task.clicked.connect(lambda: self.del_task())
			self.ui.btn_save.clicked.connect(lambda: self.create_task())
			self.ui.btn_cancel.clicked.connect(lambda: self.cancel_create_task())
			self.ui.btn_edit_task.clicked.connect(lambda: self.edit_task_menu())
			self.ui.btn_cancel_edit.clicked.connect(lambda: self.cancel_edit_task())
			self.ui.btn_save_edit.clicked.connect(lambda: self.edit_task())

			self.ui.lis_wid_category.itemDoubleClicked.connect(lambda: self.refresh_task_list())
			self.ui.lis_wid_task.itemDoubleClicked.connect(lambda: self.view_task())

			self.ui.btn_save.hide()
			self.ui.btn_cancel.hide()
			self.ui.btn_save_edit.hide()
			self.ui.btn_cancel_edit.hide()
			self.ui.led_name_task.setDisabled(True)
			self.ui.ted_description_task.setDisabled(True)

			self.resize(900, 350)
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
		self.ui.led_name_task.clear()
		self.ui.ted_description_task.clear()

		if self.ui.lis_wid_category.count() != 0:
			category_name = self.ui.lis_wid_category.currentItem().text()
			lis_task = sql_query.get_task(category_name)

			first_item = None

			for lis_name in lis_task:
				if not first_item:
					first_item = QListWidgetItem(*lis_name)
					self.ui.lis_wid_task.addItem(first_item)
				else:
					self.ui.lis_wid_task.addItem(*lis_name)

			self.ui.lis_wid_task.setCurrentItem(first_item)
		else:
			self.mes_box('Не выбрана категория')

	def create_category(self) -> None:
		dlg_create_table = DlgCreateCategory()
		dlg_create_table.exec()

		self.refresh_category_list()

	def create_task_menu(self) -> None:
		self.ui.ted_description_task.clear()
		self.ui.led_name_task.clear()

		self.ui.led_name_task.setDisabled(False)
		self.ui.ted_description_task.setDisabled(False)

		self.ui.lis_wid_task.setCurrentItem(None)
		self.ui.lis_wid_task.setDisabled(True)

		self.ui.btn_save.show()
		self.ui.btn_cancel.show()

		self.ui.btn_del_task.hide()
		self.ui.btn_complete_task.hide()
		self.ui.btn_edit_task.hide()
		self.ui.btn_add_task.hide()
		self.ui.btn_refresh_task_list.hide()

	def create_task(self) -> None:
		category_name = self.ui.lis_wid_category.currentItem().text()
		task_name = self.ui.led_name_task.text()
		description = self.ui.ted_description_task.toPlainText()

		if category_name and task_name and description:
			sql_query.insert_task(task_name, description, category_name)
			self.cancel_create_task()
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
		self.refresh_task_list()

		self.ui.btn_save.hide()
		self.ui.btn_cancel.hide()

		self.ui.btn_del_task.show()
		self.ui.btn_complete_task.show()
		self.ui.btn_edit_task.show()
		self.ui.btn_add_task.show()
		self.ui.btn_refresh_task_list.show()

		self.ui.led_name_task.setDisabled(True)
		self.ui.ted_description_task.setDisabled(True)

	def del_task(self) -> None:
		category_name = self.ui.lis_wid_category.currentItem().text()
		task_name = self.ui.lis_wid_task.currentItem().text()

		if category_name and task_name:
			if self.mes_box(f'Удалить задачу {task_name} в категории {category_name}', True):
				sql_query.del_task(category_name, task_name)

				self.refresh_task_list()

	def edit_task_menu(self) -> None:
		self.ui.ted_description_task.clear()
		self.ui.led_name_task.clear()

		self.view_task()

		self.ui.led_name_task.setDisabled(False)
		self.ui.ted_description_task.setDisabled(False)

		self.ui.lis_wid_task.setDisabled(True)

		self.ui.btn_save_edit.show()
		self.ui.btn_cancel_edit.show()

		self.ui.btn_del_task.hide()
		self.ui.btn_complete_task.hide()
		self.ui.btn_edit_task.hide()
		self.ui.btn_add_task.hide()
		self.ui.btn_refresh_task_list.hide()

	def edit_task(self) -> None:
		category_name = self.ui.lis_wid_category.currentItem().text()
		task_name_new = self.ui.led_name_task.text()
		task_name_old = self.ui.lis_wid_task.currentItem().text()
		description = self.ui.ted_description_task.toPlainText()

		if task_name_new and description:
			sql_query.update_task(task_name_new, description, category_name, task_name_old)

			self.cancel_edit_task()
		else:
			if not task_name_new:
				self.ui.led_name_task.setText('Введите название')
			if not description:
				self.ui.ted_description_task.setText('Введите описание')

	def cancel_edit_task(self) -> None:
		self.ui.ted_description_task.clear()
		self.ui.led_name_task.clear()

		self.ui.lis_wid_task.setDisabled(False)
		self.refresh_task_list()

		self.ui.btn_save_edit.hide()
		self.ui.btn_cancel_edit.hide()

		self.ui.btn_del_task.show()
		self.ui.btn_complete_task.show()
		self.ui.btn_edit_task.show()
		self.ui.btn_add_task.show()
		self.ui.btn_refresh_task_list.show()

		self.ui.led_name_task.setDisabled(True)
		self.ui.ted_description_task.setDisabled(True)

	def view_task(self) -> None:
		category_name = self.ui.lis_wid_category.currentItem().text()
		task_name = self.ui.lis_wid_task.currentItem().text()

		if category_name and task_name:
			task_data = list(sql_query.get_task_details(category_name, task_name)[0])

			self.ui.led_name_task.setText(task_data[0])
			self.ui.ted_description_task.setText((task_data[1]))

	@staticmethod
	def mes_box(mes_text: str, accept_mode: bool = False) -> Union[bool, None]:
		if accept_mode:
			msg = QMessageBox()
			msg.setWindowTitle('Подтвердите действие')
			msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
			msg.setText(mes_text)

			return_value = msg.exec()
			return return_value == QMessageBox.Ok
		else:
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
