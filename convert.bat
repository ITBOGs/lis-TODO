python -m PyQt5.uic.pyuic -x design_MainWindow.ui -o design_MainWindow.py
python -m PyQt5.uic.pyuic -x design_dlg_create_table.ui -o design_dlg_create_table.py
pyrcc5 file.qrc -o file_rc.py