from enum import Enum
from PyQt5.QtWidgets import QFileDialog, QGridLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QWidget

from download import download_video, download_audio


class DownloadType(Enum):
    """When downloading video data, identifies which file format to use."""
    VIDEO = 1
    AUDIO = 2


class DownloadWidget(QWidget):
    """PyQt5 widget for downloading video and audio from a URL."""
    url_input = None    # Editable text field

    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.setFixedSize(320, 240)
        self.setWindowTitle("youtube-dl")

        video_url_label = QLabel("Video URL:")
        self.url_input = QLineEdit()

        download_video_button = QPushButton("Download Video")
        download_video_button.clicked.connect(self.open_dialog_video)
        download_audio_button = QPushButton("Download Audio")
        download_audio_button.clicked.connect(self.open_dialog_audio)

        grid = QGridLayout()
        grid.addWidget(video_url_label, 0, 0)
        grid.addWidget(self.url_input, 0, 1)

        grid.addWidget(download_video_button, 1, 0, 1, 2)
        grid.addWidget(download_audio_button, 2, 0, 1, 2)

        self.setLayout(grid)
        self.show()

    def open_dialog_video(self):
        """Presents a native dialog to select the directory to save the video file to."""
        if not self.url_input or self.url_input == '':
            # No URL was provided, display a message to the user.
            alert = QMessageBox()
            alert.setText("Please provide a URL.")
            alert.exec_()
        else:
            path = str(QFileDialog.getExistingDirectory(self, "Save Video"))
            if path:
                # User selected a directory, download the video
                self.download(DownloadType.VIDEO, path)

    def open_dialog_audio(self):
        """Presents a native dialog to select the directory to save the audio file to."""
        if not self.url_input or self.url_input == '':
            # No URL was provided, display a message to the user.
            alert = QMessageBox()
            alert.setText("Please provide a URL.")
            alert.exec_()
        else:
            path = str(QFileDialog.getExistingDirectory(self, "Save Audio"))
            if path:
                # User selected a directory, download the audio
                self.download(DownloadType.AUDIO, path)

    def download(self, dl_type, path):
        url = self.url_input.text()
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
