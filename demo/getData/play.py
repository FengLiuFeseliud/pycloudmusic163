from pycloudmusic163 import Music163
from pycloudmusic163.object import dj_music

# 获取资源文件

# cookie登录
headers = Music163.music163_headers
headers["cookie"] += r"用户cookie"
music163 = Music163(headers)

my = music163.my()
if type(my) == int:
    print(f"cookie无效 请检查...")
    exit()

print(f"当前登录用户:{my.name}, id:{my.id}")

path = input("保存路径:")
# 获取music
# http://music.163.com/song?id=511975950&userid=492346933
music = music163.music("511975950")[0]
music.play(path)

# 获取mv
# http://music.163.com/mv/?id=5442389&userid=492346933
mv = music163.mv("5442389")
mv.play(path)

# 获取电台节目
# http://music.163.com/radio/?id=342290050&userid=492346933
dj = music163.dj("342290050")
# 获取第一首电台节目
dj_music = dj_music(my.headers, dj.music_list[0])
dj_music.play(path)