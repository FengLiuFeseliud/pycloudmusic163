from pycloudmusic163 import Music163

# 云盘操作

# cookie登录
headers = Music163.music163_headers
headers["cookie"] += r"用户cookie"
music163 = Music163(headers)

my = music163.my()
if type(my) == int:
    print(f"cookie无效 请检查...")
    exit()

cloud = my.cloud()
print(f"当前登录用户:{my.name}, id:{my.id}")

# 显示云盘数据
print(f"云盘歌曲数:{cloud.cloud_count}, 云盘已用空间:{cloud.size}")
# 打印云盘第一页数据
for music in cloud:
    print(music.name, music.artist, music.id)