# pycloudmusic163

​		使用 Python 快速调用网易云音乐 api

### 参考

> [NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)
>
> 



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









