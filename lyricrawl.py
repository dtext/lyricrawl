from time import sleep
import os

from errors import LyricsNotFoundError
from lyrics import find_lyrics
from spotify import currently_playing


def main():
    try:
        while True:
            # request currently playing song from spotify
            (song, progress_ms) = currently_playing()

            if song is not None:
                clear_console()
                title = "\"{title}\" by {artist}".format(title=song.title, artist=song.artist)
                #  "Title" by Artist
                print("\n  " + title)
                try:
                    # lyrics, indented
                    print("  " + find_lyrics(song).replace("\n", "\n  "))
                    print("\n\n  (Lyrics provided by songtexte.com)")
                except LyricsNotFoundError:
                    print("  Sadly, the lyrics for this song cannot be found.")

                wait_time = 1 + (song.duration - progress_ms) // 1000  # remaining time + small buffer
                wait_time = min(5, wait_time)
            else:
                wait_time = 5

            # wait for the specified time, waking up periodically to check for CTRL + C
            for i in range(wait_time):
                sleep(1)
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        print("\nAn error occured during execution. Exiting now. Error details:\n")
        raise e


def clear_console():
    return os.system("cls") if os.name == "win32" else os.system("clear")


if __name__ == "__main__":
    main()
