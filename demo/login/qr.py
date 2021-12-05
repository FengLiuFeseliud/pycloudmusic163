from pycloudmusic163 import LoginMusic163
import time

login = LoginMusic163()

# 获取key
key = login.login_qr_key()
# 打印key
# ('c13526fa-....', 'https://music.163.com/login?codekey=....')
# 用第二个地址生成二维码 这里可以去 https://cli.im/ 来生成
print(key)
# 轮查二维码 803为登录成功
while True:
    code, music163, cookie = login.login_qr(key)
    if code == 803:
        print("登录成功!")
        break

    if code == 800:
        # 二维码失效退出
        print("二维码失效")
        exit()

    if code == 801:
        print("等待扫码...")
    
    if code == 802:
        print("等待app授权...")

    time.sleep(3)

# 验证登录成功 打印用户名称 用户签名 用户id
my = music163.my()
print(my.name, my.signature, my.id)
