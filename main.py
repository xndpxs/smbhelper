import sys
import os
from PySide6.QtWidgets import QApplication
from views.smb_view import SmbView


def main():
    # Verificar si el usuario es root
    if os.geteuid() != 0:
        print("Este programa debe ejecutarse como root.")
        sys.exit(1)

    app = QApplication(sys.argv)
    window = SmbView(app)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
