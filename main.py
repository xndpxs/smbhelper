import sys
from PySide6.QtWidgets import QApplication
from views.smb_view import SmbView


def main():
    app = QApplication(sys.argv)
    window = SmbView(app)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
