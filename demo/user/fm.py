from pycloudmusic163 import Music163
from pycloudmusic163.object import music
from time import sleep

# 私人fm操作

# cookie登录
headers = Music163.music163_headers
headers["cookie"] += r"用户cookie"
music163 = Music163(headers)

my = music163.my()
if type(my) == int:
    print(f"cookie无效 请检查...")
    exit()

fm = my.fm()
print(f"当前登录用户:{my.name}, id:{my.id}")

# 每3秒读取fm数据并打印
fm_list = fm.read()
while True:
    for music_ in fm_list:
        music_ = music163.music(music_["id"])[0]
        print(music_.name_str, music_.artist_str, music_.id)
    sleep(3)
    fm_list = fm.read()