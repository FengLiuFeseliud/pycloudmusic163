from pycloudmusic163 import LoginMusic163

login = LoginMusic163()

email = input("邮箱:")
# 登入
code, music163, cookie = login.login_email(email, input("密码:"))
if code != 200:
    # 失败打印错误码
    print(f"登录失败 错误码:{code}")
    exit()

# 验证登录成功 打印用户名称 用户签名 用户id
my = music163.my()
print(my.name, my.signature, my.id)