from enum import Enum
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QGridLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QWidget

from download import download_info, download_video, download_audio


class DownloadType(Enum):
    """When downloading video data, identifies which file format to use."""
    VIDEO = 1
    AUDIO = 2


class DownloadWidget(QWidget):
    """PyQt5 widget for displaying video info and performing downloads."""
    search_field = None
    search_button = None

    info_label = None

    download_button = None

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

        self.download_button = QPushButton("Download")
        # self.download_video_button.clicked.connect(self.download_closure(DownloadType.VIDEO))
        self.download_button.clicked.connect(self.save_file_dialog)

        grid = QGridLayout()
        grid.addWidget(self.search_field, 0, 0)
        grid.addWidget(self.search_button, 0, 1)

        grid.addWidget(self.info_label, 1, 0, 1, 2)

        grid.addWidget(self.download_button, 2, 0, 1, 2)

        self.setLayout(grid)
        self.show()

    def save_file_dialog(self):
        options = QFileDialog.Options()
        file_types = "Video Files (*.mp4);;Audio Files (*.wav);;"
        file_name, file_filter = QFileDialog.getSaveFileName(self, "Save As", "", file_types, file_types, options=options)
        if file_name:
            # Append file extension if not provided
            extension = file_filter[-5:-1]
            if file_name[-4:] != extension:
                file_name += extension

            if extension == '.mp4':
                self.download(DownloadType.VIDEO, file_name)

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

    def download(self, dl_type, path):
        url = self.search_field.text()
        if dl_type == DownloadType.VIDEO:
            res, err = download_video(url, path)
            if err:
                alert = QMessageBox()
                alert.setText(err)
                alert.exec_()
            else:
                pass
        elif dl_type == DownloadType.AUDIO:
            res, err = download_audio(url, path)
            if err:
                alert = QMessageBox()
                alert.setText(err)
                alert.exec_()
            else:
                pass
        else:
            # The download type was not an expected value, throw an error.
            alert = QMessageBox()
            alert.setText("Error downloading video data.\n"
                          "Could not determine if video or audio should be downloaded.")
            alert.exec_()
            return
