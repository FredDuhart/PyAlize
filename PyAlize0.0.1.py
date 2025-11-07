import os
import sys
sys.path.append(os.getcwd())
from Qt_gui.PyAlize_Qt import MainWindow
from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet  # Feuille de style Material


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Appliquer le thème Qt-Material
    apply_stylesheet(app, theme="dark_pink.xml")

    window = MainWindow()
    window.resize(1050, 400)
    window.show()
    sys.exit(app.exec())