import sys
from design_MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication


class lis_todo(QMainWindow):
	def __init__(self):
		super(lis_todo, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = lis_todo()
	window.show()

	sys.exit(app.exec())
