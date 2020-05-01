import sys

from window import DownloadWidget
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = DownloadWidget()
    sys.exit(app.exec_())
