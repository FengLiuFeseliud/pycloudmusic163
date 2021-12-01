# pycloudmusic163

​		使用 Python 快速调用网易云音乐 api

### 参考

> [NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)
>
> 

### 安装

```python
pip install pycloudmusic163
```



### 简单使用

> 获取歌单
>
> ```python
> from pycloudmusic163 import Music163
> 
> # 默认请求头
> headers = Music163.music163_headers
> headers["cookie"] += "用户cookie"
> music163 = Music163(headers=headers)
> 
> # https://music.163.com/playlist?id=6843808070
> playlist = music163.playlist("6843808070") # 歌单id
> # 打印歌单标题 歌单作者 歌单简介
> print(playlist.name, playlist.user_str, playlist.description)
> for music in playlist:
>  # 打印歌单每一首歌的标题 歌手
>  print(music.name_str, music.artist_str)
> ```
>
> 二维码登录
>
> ```python
> from pycloudmusic163 import LoginMusic163
> import time
> 
> login = LoginMusic163()
> # 获取key
> key = login.login_qr_key()
> # 打印key
> # ('c13526fa-....', 'https://music.163.com/login?codekey=....')
> # 用第二个地址生成二维码 这里可以去 https://cli.im/ 来生成
> print(key)
> # 轮查二维码 803为登录成功
> while True:
>  code, music163, cookie = login.login_qr(key)
>  if code == 803:
>      break
>  time.sleep(3)
> 
> # 验证登录成功 打印用户名称 用户签名 用户id
> my = music163.my()
> print(my.name, my.signature, my.id)
> ```
>
> 

# 使用文档



## 1.登录

> **from pycloudmusic163 import LoginMusic163**
>
> **`LoginMusic163() `初始化 login 对象**
>
> ### login 对象
>
> `login.login_email(self, email, password)` 邮箱登录
>
> **参数说明:** 
>
> email：邮箱
> password：密码
>
> 错误码：501 未注册 502 密码错误
>
> 成功返回Music163对象， cookie 失败返回错误码
>
>  
>
> `login.login_captcha(phone, country_code="86")`  发送手机验证码
>
> **参数说明:** 
>
> phone： 手机号

> country_code： 国家码 (用于国外手机号登录)
>
> 成功返回0，失败返回错误码
>
>  
>
> `login.login_cellphone(phone, password, captcha=False, country_code="86")` 手机/验证码 登录
>
> **参数说明:**
>
> phone： 手机号
> password： 验证参数
> captcha： True 时为验证码登录 password 值为验证码，False 时为密码登录 password 值为密码
> country_code： 国家码 (用于国外手机号登录)
> 成功返回Music163对象, cookie，失败返回错误码
>
>  
>
> `login.login_qr_key()` 获取二维码 key
>
> `login.login_qr(qr_key)`  二维码登录，查询二维码状态
>
> **参数说明:**
>
> qr_key：二维码 key
>
> 状态码：801 等待扫码， 802 授权中， 800 二维码不存在或已过期， 803 登录成功
> 成功返回状态码, Music163对象, cookie，失败返回状态码

## 2.获取对象

> ​	from pycloudmusic163 import Music163
>
> **`Music163(headers=headers)` 初始化 music163 对象**
>
> 可以通过 `Music163.music163_headers`  获取一个初始请求头
>
> 然后传入cookie登录`headers["cookie"] += "用户cookie"`
>
> 使用 login 对象登录成功也会返回一个 music163 对象
>
>  
>
> `music163.my()` 获取当前cookie用户信息并实例化my对像
>
> cookie无效返回200，成功返回my对像，失败返回错误码
>
>  
>
> `music(id_)` 获取歌曲并实例化music对像
>
> **参数说明:**
>
> id_：歌曲id 支持多 id (使用列表)
>
> 成功返回music对像列表， 失败返回错误码









