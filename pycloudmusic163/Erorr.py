class Music163(Exception):
    pass


class Music163ObjectException(Music163):

    def __str__(self):
        return "musicObject无法使用subscribe 请改用playlistObject add() del_()"
