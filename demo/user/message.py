from pycloudmusic163 import Music163

# 私信操作

# cookie登录
headers = Music163.music163_headers
headers["cookie"] += r"用户cookie"
music163 = Music163(headers)

my = music163.my()
if type(my) == int:
    print(f"cookie无效 请检查...")
    exit()

message = my.message()
print(f"当前登录用户:{my.name}, id:{my.id}")

toUser = input("发送至 (用户uid):")
code = message.send("Python: 你好!", toUser)
if type(code) == int:
    print(f"发送失败... 错误码:{code}")
    exit()

print("发送成功!")