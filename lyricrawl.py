from time import sleep
import os

from lyrics import find_lyrics
from spotify import currently_playing


def main():
    try:
        while True:
            # request currently playing song from spotify
            (song, progress_ms) = currently_playing()

            if song is not None:
                # print lyrics
                clear_console()
                print(find_lyrics(song))
                wait_time = 2 + (song.duration - progress_ms) // 1000  # remaining + 2 second buffer
            else:
                wait_time = 10

            # wait for the specified time, waking up periodically to check for CTRL + C
            for i in range(wait_time):
                sleep(1)
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        print("An error occured during execution:")
        print(str(e))
        return 1


def clear_console():
    return os.system("cls") if os.name == "win32" else os.system("clear")


if __name__ == "__main__":
    main()
