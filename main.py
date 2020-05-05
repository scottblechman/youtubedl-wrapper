import sys

from download import set_service
from progress_service import ProgressService
from window import DownloadWidget
from PyQt5.QtWidgets import QApplication


def progress_updated(percent, eta):
    """Automatically called when the progress service receives an update.
    :param percent: Download completion, between 0.0 and 1.0
    :param eta: Time remaining in hh:mm:ss
    """

    if widget:
        widget.update_progress(percent, eta)


widget = None

if __name__ == '__main__':
    service = ProgressService()

    service.subscribe(progress_updated)
    set_service(service)    # Make service available to download.py

    app = QApplication(sys.argv)
    widget = DownloadWidget()
    sys.exit(app.exec_())
