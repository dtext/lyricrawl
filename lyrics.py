from song import Song
import requests
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
    response = requests.get(url="http://www.songtexte.com/search",
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
        self.counter = 1

    def handle_starttag(self, tag, attrs):
        self.counter += 1

    def handle_data(self, data):
        self.lyrics += data

    def handle_endtag(self, tag):
        self.counter -= 1
        if self.counter < 1:
            def nop(*args, **kwargs):
                pass
            self.handle_data = nop
            self.handle_starttag = nop
            self.handle_endtag = nop

    def error(self, message):
        pass  # todo


def find_lyrics(song: Song) -> str:
    response = requests.get(find_url(song)).content.decode("utf-8")
    response_preprocessed = response.split("<div id=\"lyrics\">")[1].replace("<br>", "\n")
    finder = LyricsFinder()
    finder.feed(response_preprocessed)
    return finder.lyrics
