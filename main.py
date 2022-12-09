import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from design_MainWindow import Ui_MainWindow
from sqlquery import SqlQuery


class LisTodo(QMainWindow):
	def __init__(self):
		super(LisTodo, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.table_verification()

	def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
		sql_query.db_disconnect()

	def table_verification(self):
		table1 = sql_query.table_exists('tasks')
		table2 = sql_query.table_exists('categories')

		if not (table1 and table2):
			msg = QMessageBox()
			msg.setWindowTitle('Предупреждение')
			msg.setText('Не найдено необходимых таблиц')

			self.setWindowTitle('Нет подключения к БД')
			self.ui.pushButton.disconnect()

			msg.exec()


if __name__ == '__main__':
	sql_query = SqlQuery()

	if sql_query.db_connect():
		app = QApplication(sys.argv)
		window = LisTodo()
		window.show()

		sys.exit(app.exec())
