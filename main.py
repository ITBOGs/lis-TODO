import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from design_MainWindow import Ui_MainWindow
from sqlquery import SqlQuery


class LisTodo(QMainWindow):
	def __init__(self, flag_db: int):
		super(LisTodo, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		if flag_db:
			sql_query.create_table()
		else:
			self.setWindowTitle('Нет подключения к БД')
			self.mes_box('Нет подключения к БД')

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
