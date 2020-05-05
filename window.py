from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QGridLayout, QLabel, QLineEdit, QMessageBox, QProgressBar, QPushButton, \
    QWidget, QApplication

from download import download_video, download_audio


class DownloadType(Enum):
    """When downloading video data, identifies which file format to use."""
    VIDEO = 1
    AUDIO = 2


class DownloadWidget(QWidget):
    """PyQt5 widget for downloading video and audio from a URL."""
    url_input = None        # Editable text field
    time_remaining = None   # ETA in hh:mm:ss format
    progress_bar = None     # Percent of download completed

    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.setFixedSize(320, 240)
        self.setWindowTitle("YouTube DL")

        video_url_label = QLabel("Video URL:")
        self.url_input = QLineEdit()

        self.time_remaining = QLabel()
        self.time_remaining.setAlignment(Qt.AlignCenter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

        download_video_button = QPushButton("Download Video")
        download_video_button.clicked.connect(self.open_dialog_video)
        download_audio_button = QPushButton("Download Audio")
        download_audio_button.clicked.connect(self.open_dialog_audio)

        grid = QGridLayout()
        grid.addWidget(video_url_label, 0, 0)
        grid.addWidget(self.url_input, 0, 1)
        grid.addWidget(self.time_remaining, 1, 0, 1, 2)
        grid.addWidget(self.progress_bar, 2, 0, 1, 2)

        grid.addWidget(download_video_button, 3, 0, 1, 2)
        grid.addWidget(download_audio_button, 4, 0, 1, 2)

        self.setLayout(grid)
        self.show()

    def update_progress(self, percent_downloaded, time_remaining):
        print(f"\n ETA: {time_remaining}\n")
        if time_remaining == 'Download completed.':
            self.time_remaining.setText(time_remaining)
        else:
            self.time_remaining.setText(f"Time Remaining: {time_remaining}")
        self.progress_bar.setValue(min(int(percent_downloaded * 100), 100))
        QApplication.processEvents()

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
