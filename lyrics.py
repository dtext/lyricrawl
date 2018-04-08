from song import Song


def find_lyrics(song: Song) -> str:
    return """
  \"{title}\" by {artist}
  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  Roses are red
  Violets are blue
  This string is empty
  and so are you
    """.format(title=song.title, artist=song.artist)
