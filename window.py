from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QWidget

from download import download_info


class DownloadWidget(QWidget):

    search_field = None
    search_button = None

    info_label = None

    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.setFixedSize(640, 480)
        self.setWindowTitle("youtube-dl")

        self.search_field = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search)

        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignCenter)

        grid = QGridLayout()
        grid.addWidget(self.search_field, 0, 0)
        grid.addWidget(self.search_button, 0, 1)

        grid.addWidget(self.info_label, 1, 0, 1, 2)

        self.setLayout(grid)
        self.show()

    def search(self):
        """Verify that the URL to download has valid video info, otherwise displaying an error."""
        url = self.search_field.text()
        res, err = download_info(url)
        if err:
            alert = QMessageBox()
            alert.setText(err)
            alert.exec_()
        else:
            self.info_label.setText(res)
            self.info_label.repaint()   # Needed on macOS to display results when window is focused.
