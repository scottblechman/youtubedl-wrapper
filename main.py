import sys

from download import set_subject
from progress_service import ProgressService
from window import DownloadWidget
from PyQt5.QtWidgets import QApplication


def progress_updated(percent, eta):
    if widget:
        widget.update_progress(percent, eta)


widget = None

if __name__ == '__main__':
    service = ProgressService()

    service.subscribe(progress_updated)
    set_subject(service)

    app = QApplication(sys.argv)
    widget = DownloadWidget()
    sys.exit(app.exec_())
