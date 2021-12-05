from pycloudmusic163 import LoginMusic163

login = LoginMusic163()
# 505  昵称已被占用
phone = input("手机号:")
# 发送验证码
login.login_captcha(phone)
while True:
    captcha = input("验证码:")
    if captcha == "exit":
        exit()

    # 验证码校验
    captcha_in = login.check_captcha(phone, captcha)
    if captcha_in:
        break

    print("验证码校验失败... 请重试")

password = input("密码:")
while True:
    code, music163, cookie = login.register(input("昵称:"), phone, password, captcha)
    if code == 200:
        print("注册成功")
        break

    if code == 505:
        print("昵称已被占用... 请重试")
    
# 验证登录成功 打印用户名称 用户签名 用户id
my = music163.my()
print(my.name, my.signature, my.id)