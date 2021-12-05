from pycloudmusic163 import Music163

# 动态操作

# cookie登录
headers = Music163.music163_headers
headers["cookie"] += r"用户cookie"
music163 = Music163(headers)

my = music163.my()
if type(my) == int:
    print(f"cookie无效 请检查...")
    exit()

event = my.event()
print(f"当前登录用户:{my.name}, id:{my.id}")


code = event.send("Python: 你好!")
if code != 0:
    print(f"发送失败... 错误码:{code}")
    exit()

print("发送成功!")