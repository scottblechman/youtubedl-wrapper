import datetime
import youtube_dl

progress_subject = None


def set_subject(subject):
    global progress_subject
    progress_subject = subject


# noinspection PyUnresolvedReferences
def __progress_hook(download):
    """
    Called automatically on download update. Updates the progress service_subject with the percent completed.
    :param download: File download status at discrete point in time
    """
    if progress_subject:
        percent_downloaded = 0.0
        time_remaining = ''
        if download['status'] == 'finished':
            percent_downloaded = 100.0
            time_remaining = 'Download completed.'
        elif download['status'] == 'downloading':
            percent_downloaded = float(download['_percent_str'].lstrip().strip('%')) / 100
            time_remaining = download['_eta_str']
        progress_subject.update_download_status(percent_downloaded, time_remaining)


# Passed to youtube-dl as flags
_options = {
    'nocheckcertificate': True,  # Stops youtube-dl from throwing SSL errors
    'noplaylist': True,  # Prevents downloading all videos if a playlist id is appended
    'progress_hooks': [__progress_hook]
}


def __get_metadata(url):
    """Extract video metadata (title, uploader, etc.) from a provided URL.

    :param url: User-inputted string from window.
    :return: Video info (None if error), error data if any.
    """
    if not url or url == '':
        return None, "Could not download video info.\nNo URL was provided."

    res = None  # Video metadata
    err = None  # Error

    with youtube_dl.YoutubeDL(_options) as ydl:
        try:
            video_info = ydl.extract_info(url, download=False)  # With download=False, only metadata is returned

            formatted_views = f"{video_info['view_count']:,}"
            formatted_length = str(datetime.timedelta(seconds=video_info['duration']))
            if video_info['duration'] < 3600:   # Trim videos under an hour to just mm:ss
                formatted_length = formatted_length[-5:]

            res = {'title': video_info['title'], 'uploader': video_info['uploader'],
                   'views': formatted_views, 'length': formatted_length}
        except youtube_dl.utils.DownloadError as dl_error:
            err = f"Could not download video info.\n{dl_error}"

    return res, err


# noinspection PyTypeChecker
def download_video(url, path):
    """Download MP4 video from a provided URL.

        :param url: User-inputted string from window.
        :param path: File path to save video to.
        :return: Video (None if error), error data if any.
        """
    if not url or url == '':
        return None, "Could not download video.\nNo URL was provided."

    res = None  # Video data
    err = None  # Error

    data, error = __get_metadata(url)
    if not error:
        _options['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        _options['outtmpl'] = f'{path}/%(uploader)s - %(title)s.%(ext)s'
        with youtube_dl.YoutubeDL(_options) as ydl:
            try:
                res = ydl.download([url])
            except youtube_dl.utils.DownloadError as dl_error:
                err = f"Could not download video info.\n{dl_error}"

    return res, err


# noinspection PyTypeChecker
def download_audio(url, path):
    """Download MP3 audio from a provided URL.

            :param url: User-inputted string from window.
            :param path: File path to save audio to.
            :return: Audio (None if error), error data if any.
            """
    if not url or url == '':
        return None, "Could not download video.\nNo URL was provided."

    res = None  # Audio data
    err = None  # Error

    _options['outtmpl'] = f'{path}/%(uploader)s - %(title)s.%(ext)s'
    _options['format'] = 'bestaudio[ext=m4a]/best[ext=m4a]'
    _options['postprocessors'] = [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': '192',
      }]
    with youtube_dl.YoutubeDL(_options) as ydl:
        try:
            res = ydl.download([url])
        except youtube_dl.utils.DownloadError as dl_error:
            err = f"Could not download audio.\n{dl_error}"

    return res, err
