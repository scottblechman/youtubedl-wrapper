import datetime
import youtube_dl

# Passed to youtube-dl as flags
__options = {
    'nocheckcertificate': True,  # Stops youtube-dl from throwing SSL errors
    'noplaylist': True  # Prevents downloading all videos if a playlist id is appended
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

    with youtube_dl.YoutubeDL(__options) as ydl:
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
        __options['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        __options['outtmpl'] = f'{path}/%(uploader)s - %(title)s.%(ext)s'
        with youtube_dl.YoutubeDL(__options) as ydl:
            try:
                res = ydl.download([url])
            except youtube_dl.utils.DownloadError as dl_error:
                err = f"Could not download video info.\n{dl_error}"

    return res, err


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

    __options['outtmpl'] = f'{path}/%(uploader)s - %(title)s.%(ext)s'
    __options['format'] = 'bestaudio[ext=m4a]/best[ext=m4a]'
    with youtube_dl.YoutubeDL(__options) as ydl:
        try:
            res = ydl.download([url])
        except youtube_dl.utils.DownloadError as dl_error:
            err = f"Could not download audio.\n{dl_error}"

    return res, err
