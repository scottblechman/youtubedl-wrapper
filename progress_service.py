class ProgressService:
    """Class for passing download status state from download to window
    Attributes:
        callbacks: List of functions called on update
        percent_downloaded: Download completion, between 0.0 and 1.0
        time_remaining: Time remaining in hh:mm:ss
    """
    def __init__(self):
        self.callbacks = []
        self.percent_downloaded = 0.0
        self.time_remaining = ''

    def subscribe(self, callback):
        """Adds the function callback to list of functions to call on update."""
        self.callbacks.append(callback)

    def unsubscribe(self, callback):
        """Removes the function callback from the list of functions to call on update."""
        self.callbacks.remove(callback)

    def notify(self):
        """Calls all callback functions with current state."""
        for callback in self.callbacks:
            callback(self.percent_downloaded, self.time_remaining)

    def update_download_status(self, percent_downloaded, time_remaining):
        """Update state and pass to callback functions."""
        self.percent_downloaded = percent_downloaded
        self.time_remaining = time_remaining
        self.notify()
