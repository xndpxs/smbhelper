import sys
from PySide6 import QtWidgets
from smbhelper_functions import SmbHelper

app = QtWidgets.QApplication(sys.argv)
window =SmbHelper(app)
window.show()

app.exec()

