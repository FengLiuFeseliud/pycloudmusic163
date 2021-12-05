from pycloudmusic163 import LoginMusic163

login = LoginMusic163()

phone = input("手机号:")
# 检查是否存在该用户
phone_in = login.check_cellphone(phone)
if phone_in is None or type(phone_in) == int:
    print(f"不存在该用户或者api错误 信息:{phone_in}")
    exit()

# 登入
code, music163, cookie = login.login_cellphone(phone, input("密码:"))
if code != 200:
    # 失败打印错误码
    print(f"登录失败 错误码:{code}")
    exit()


# 验证登录成功 打印用户名称 用户签名 用户id
my = music163.my()
print(my.name, my.signature, my.id)