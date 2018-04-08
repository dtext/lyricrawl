from song import Song
from requests import get
import html.parser


class LinkFinder(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.handle_starttag = self.find_top_hit
        self.link = None

    def find_top_hit(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "div" and "class" in attrs and attrs["class"] == "topHit":
            self.handle_starttag = self.find_top_link

    def find_top_link(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "songtext" in attrs["href"]:
            self.link = "http://www.songtexte.com/" + attrs["href"]
            self.handle_starttag = lambda t, a: None

    def error(self, message):
        pass  # todo


def find_url(song: Song):
    response = get(url="http://www.songtexte.com/search",
                   params={
                       "q": "+".join(song.artist.split(" ") + song.title.split(" ")),
                       "c": "all"
                   })
    finder = LinkFinder()
    finder.feed(response.content.decode("utf-8"))
    return finder.link


class LyricsFinder(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.lyrics = ""
        self.collecting = True
        self.handle_data = lambda data: None

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            attrs = dict(attrs)
            if "id" in attrs and attrs["id"] == "lyrics":
                self.collecting = True
                self.handle_data = self.save_lyrics

    def save_lyrics(self, data):
        self.lyrics += str(data)

    def handle_endtag(self, tag):
        if self.collecting and tag == "div":
            self.collecting = False
            self.handle_data = lambda data: None

    def error(self, message):
        pass  # todo


def find_lyrics(song: Song) -> str:
    response = get(find_url(song))
    response_preprocessed = response.content.decode("utf-8").replace("<br>", "")
    finder = LyricsFinder()
    finder.feed(response_preprocessed)
    return finder.lyrics
