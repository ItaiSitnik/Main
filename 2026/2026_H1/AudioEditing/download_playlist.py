import sys

import yt_dlp


def download_audio_as_mp3(url):
    """
    Downloads the best audio from a given URL and converts it to MP3.
    """

    # These are the options for yt-dlp
    # 'format': 'bestaudio/best' -> Selects the best audio-only stream
    # 'postprocessors': ...     -> Defines what to do after downloading
    # 'key': 'FFmpegExtractAudio' -> Tells it to use ffmpeg to extract audio
    # 'preferredcodec': 'mp3'   -> Sets the desired output format
    # 'preferredquality': '192' -> Sets the audio bitrate
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": "%(title)s.%(ext)s",  # Saves file as 'Video Title.mp3'
    }

    print(f"Starting download for: {url}")

    try:
        # Create the YoutubeDL object with the options
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Start the download
            ydl.download([url])
        print("\nDownload complete!")
        print("File saved as an MP3 in the script's directory.")

    except yt_dlp.utils.DownloadError as e:
        print(f"\nAn error occurred during download: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


# --- Main execution ---
if __name__ == "__main__":
    # Get the URL from the user
    video_url = input("Enter the video URL: ")

    if not video_url:
        print("No URL provided. Exiting.")
        sys.exit(1)

    download_audio_as_mp3(video_url)
