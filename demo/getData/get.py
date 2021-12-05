from pycloudmusic163 import Music163

# 数据获取

# cookie登录
headers = Music163.music163_headers
headers["cookie"] += r"用户cookie"
music163 = Music163(headers)

my = music163.my()
if type(my) == int:
    print(f"cookie无效 请检查...")
    exit()

print(f"当前登录用户:{my.name}, id:{my.id}")

# 获取music
# http://music.163.com/song?id=511975950&userid=492346933
music = music163.music("511975950")[0]

# 获取歌单
# http://music.163.com/playlist?id=6843808070&userid=492346933
playlist = music163.playlist("6843808070")

# 获取专辑
# http://music.163.com/album?id=83218077&userid=492346933
album = music163.music("1402824752")[0].album()

# 获取歌手
# https://music.163.com/#/artist?id=17401
artist = music163.artist("17401")

# 获取mv
# http://music.163.com/mv/?id=5442389&userid=492346933
mv = music163.mv("5442389")

# 获取电台
# http://music.163.com/radio/?id=342290050&userid=492346933
dj = music163.dj("342290050")

# 打印获取的数据
print(f"music:{music.name_str}, 歌手:{music.artist_str}, id:{music.id}")
print(f"歌单:{playlist.name}, 创建者:{playlist.user_str}, id:{playlist.id}")
print(f"专辑:{album.name}, 封面:{album.cover}, id:{album.id}")
print(f"歌手:{artist.name}, 头像:{artist.cover}, id:{artist.id}")
print(f"mv:{mv.name}, 歌手:{mv.artists_str}, id:{mv.id}")
print(f"dj:{dj.name}, 创建者:{dj.user_str}, id:{dj.id}")
