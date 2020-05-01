import datetime
import youtube_dl

__options = {
    'nocheckcertificate': True,  # Important, youtube-dl will throw SSL errors otherwise.
    'noplaylist': True  # Prevents downloading all videos if a playlist id is appended.
}


def download_info(url):
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
            res = f"Title: {video_info['title']}\n" \
                  f"Uploaded by: {video_info['uploader']}\n" \
                  f"Views: {formatted_views}\n" \
                  f"Length: {formatted_length}"
        except youtube_dl.utils.DownloadError as dl_error:
            err = f"Could not download video info.\n{dl_error}"

    return res, err
