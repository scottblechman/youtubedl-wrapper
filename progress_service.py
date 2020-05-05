class ProgressService:
    def __init__(self):
        self.observers = []
        self._percent_downloaded = 0.0
        self._time_remaining = ''

    def subscribe(self, obs):
        self.observers.append(obs)

    def unsubscribe(self, obs):
        self.observers.remove(obs)

    def notify(self):
        for obs in self.observers:
            obs(self._percent_downloaded, self._time_remaining)

    def update_download_status(self, percent_downloaded, time_remaining):
        self._percent_downloaded = percent_downloaded
        self._time_remaining = time_remaining
        self.notify()
