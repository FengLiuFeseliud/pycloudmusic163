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
>     # 打印歌单每一首歌的标题 歌手
>     print(music.name_str, music.artist_str)
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
>     code, music163, cookie = login.login_qr(key)
>     if code == 803:
>       break
>     time.sleep(3)
> 
> # 验证登录成功 打印用户名称 用户签名 用户id
> my = music163.my()
> print(my.name, my.signature, my.id)
> ```
>

***


# 使用文档

**以下很长注意善用搜索 Ctrl+F**（第一次写这么长的文档...，呜，倒了）

## 0.错误码

> ```
> 400: 参数错误
> 404: api不存在
> -460: 出现-460 尝试在cookie加上 "appver=2.7.1.198277; os=pc;"
> 250: 风险提示 异常
> ```

## 1.登录

> `from pycloudmusic163 import LoginMusic163`
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
>
>  
>
> `login.check_captcha(phone, captcha, country_code="86")` 校验验证码
>
> **参数说明:**
>
> phone：手机号
> captcha：验证码
> country_code： 国家码 (用于国外手机号登录)
> 校验成功返回 True ，校验失败返回 False，api 错误返回错误码
>
>  
>
> `login.check_cellphone(phone, country_code="86")` 检查手机号是否被注册
>
> **参数说明:**
>
> phone：手机号
> country_code： 国家码 (用于国外手机号登录)
> 未注册返回  None，被注册返回用户名，api 错误返回错误码
>
> 
>
> `login.register(name, phone, password, captcha, country_code="86")`  手机注册/修改密码
>
> **参数说明:**
>
> name：昵称
>
> phone：手机号
>
> password：密码
>
> captcha：验证码
>
> country_code：国家码 (用于国外手机号)
>
> 没有测试过的接口，返回啥我也不知道
>
>  
>
> `login.replace_cellphone(phone, captcha, old_captcha, country_code="86")` 更换绑定手机
>
> **参数说明:**
>
> phone：手机号
>
> captcha：新手机验证码
>
> old_captcha：原手机验证码
>
> country_code：国家码 (用于国外手机号)
>
> 没有测试过的接口，返回啥我也不知道

## 2.获取对象

> `from pycloudmusic163 import Music163`
>
> **`Music163(headers=headers)` 初始化 music163 对象**
>
> 可以通过 `Music163.music163_headers`  获取一个初始请求头
>
> 然后传入 cookie 登录`headers["cookie"] += "用户cookie"`
>
> 使用 login 对象登录成功也会返回 music163 对象
>
> 
>
> `music163.my()` 获取当前 cookie 用户信息并实例化 my 对像
>
> cookie 无效返回200，成功返回 my 对像，失败返回错误码
>
> 
>
> `music163.music(id_)` 获取歌曲并实例化 music 对像
>
> **参数说明:**
>
> id_：歌曲id 支持多 id (使用列表)
>
> 成功返回 music 对像列表， 失败返回错误码
>
>  
>
> `music163.user(id_)` 获取用户并实例化 user 对像
>
> **参数说明:**
>
> id_：用户id
>
> 成功返回 user 对像，失败返回错误码
>
>  
>
> `music163.my()` 获取当前 cookie 用户信息并实例化 my 对像
>
> **参数说明:**
>
> 成功返回 my 对像，失败返回错误码，cookie 无效返回200
>
>  
>
> `music163.playlist(id_)` 获取歌单并实例化 playlist 对像
>
> **参数说明:**
>
> id_：歌单 id
>
> 成功返回 playlist 对像，失败返回错误码
>
>  
>
> `music163.artist(id_)` 获取歌手并实例化 artist 对像
>
> **参数说明:**
>
> id_：歌手 id
>
> 成功返回 artist 对像，失败返回错误码
>
>  
>
> `music163.album(id_)` 获取专辑并实例化 album 对像
>
> 该方法实例化的 album 对像只有 id 和专辑相关接口
>
> 暂时没有直接获取专辑信息的方法
>
> 不推荐这样获取 album 对像
>
> **参数说明:**
>
> id_：专辑 id
>
> 返回 album 对像
>
>  
>
> `music163.mv(id_)` 获取 mv 并实例化 mv 对像
>
> **参数说明:**
>
> id_：mv id
>
> 成功返回mv对像，失败返回错误码
>
>  
>
> `music163.dj(id_)` 获取电台并实例化 dj 对像
>
> **参数说明:**
>
> id_：电台 id
>
> 成功返回 dj 对像，失败返回错误码

## 3.对象方法

> ## 注意
>
> **歌单，专辑，动态，云盘，歌手**  都支持保存在 `self.music_list` 的数据可以直接遍历该对像获取
>
> **歌曲， 歌单，专辑，MV，动态**  都支持评论，因此都支持以下方法
>
> `comment(hot=True, page=0, limit=20, before_time=0)`  该对象的评论
>
> `comment_floor(comment_id, page=0, limit=20)`  楼层评论
>
> `comment_like(comment_id, in_)`  评论点赞
>
> `comment_add(content)`  发送评论
>
> `comment_delete(comment_id)`  删除评论
>
> `comment_reply(content, comment_id)`  回复评论
>
> **以下是这些方法的参数说明:**
>
> hot：热门评论 True 全部评论 False
>
> before_time：分页参数，取上一页最后一项的 time 获取下一页数据(获取超过5000条评论的时候需要用到)
>
> page：页数
>
> limit：一页获取数量
>
> comment_id：一律为评论id (comment返回的评论中的commentId)
>
> content：一律为评论内容
>
> in_：True 点赞，False 取消点赞
>
>   
>
> **歌单，专辑，MV，歌手，电台**  都支持 收藏，因此支持`self.subscribe`方法
>
> `subscribe(in_)`  对像 收藏/取消收藏
>
> **参数说明:**
>
> in_：True 收藏 False 取消收藏
>
> 成功返回0 失败返回错误码
>
>  
>
> **MV，歌手，歌曲**  都支持获取相似，因此支持`self.similar`方法
>
> `similar()` 该对象的相似
>
> 
>
> ### **music163 对像**
>
> `music163.search(key, type_=1, page=0, limit=30)` 搜索
>
> 返回的大部分内容都可以直接生成对象，不用二次请求
>
> 从 pycloudmusic163.object 导入类后， 可以这样直接生成 `类(请求头, 一条数据)` 
>
> 所有对象都继承于 Link Link.headers 即可以获取用于生成这个对像的请求头
>
> **参数说明:**
>
> key：搜索内容
>
> type_：搜索类型
>
> page：页数
>
> limit：一页获取数量
>
> 成功返回内容 失败返回错误码
>
> type_ 搜索类型如下
>
> ```
> 1: 单曲 
> 10: 专辑
> 100: 歌手
> 1000: 歌单
> 1002: 用户
> 1004: MV
> 1006: 歌词
> 1009: 电台
> 1014: 视频
> ```
>
> 
>
> `music163.personalized_playlist(limit=30)` 推荐歌单
>
> **参数说明:**
>
> limit：一页获取数量 (不支持 offset)
>
> 成功返回内容 失败返回错误码
>
> 
>
> `music163.personalized_new_song(areaId=0, limit=10)` 推荐新歌
>
> **参数说明:**
>
> limit：一页获取数量 (不支持 offset)
>
> 成功返回内容 失败返回错误码
>
> 
>
> `music163.personalized_dj()` 推荐电台
>
> **参数说明:**
>
> 成功返回内容 失败返回错误码
>
> 
>
> `music163.home_page(refresh=True, cursor=None)` 首页-发现 app 主页信息
>
> **参数说明:**
>
> refresh：是否刷新数据
>
> cursor：上一条数据返回的 cursor
>
> 成功返回内容 失败返回错误码
>
> 
>
> `music163.top_artist_list(type_=1, page=0, limit=100)`  歌手榜
>
> **参数说明:**
>
> type_：地区类型
>
> page：页数
>
> limit：一页获取数量
>
> 成功返回内容 失败返回错误码
>
> ```
> 地区类型
> 1: 华语
> 2: 欧美
> 3: 韩国
> 4: 日本
> ```
>
> 
>
> `music163.top_song(type_=0)`  新歌速递
>
> **参数说明:**
>
> type_：地区类型
>
> ```
> 地区类型
> 全部:0 
> 华语:7 
> 欧美:96 
> 日本:8 
> 韩国:16
> ```
>
> 
>
> ### **user 对象**
>
> ```python
> from pycloudmusic163 import Music163
> from pycloudmusic163.object import user
> user = user(Music163.music163_headers, {})
> 
> # user 对象的属性
> 
> # 用户uid
> user.id
> # 用户名称
> user.name
> # 用户签名
> user.signature
> # 用户等级
> user.level
> # 头像
> user.cover
> # 会员 0 无
> user.vip
> ```
>
> 
>
> `user.like_music()`  获取该 user 对象喜欢的歌曲 (返回 playlist 对象)
>
> `user.playlist(page=0, limit=30)`   获取该 user 对象的歌单
>
> **参数说明:**
>
> page：页数
>
> music_id：一页获得数量
>
> 成功返回 playlist 对象列表，失败返回错误码
>
> 
>
> `user.record(type_=True, music_object=True)`   获取该 user 对象听歌榜单
>
> **参数说明:**
>
> type_：True 所有时间，False 最近一周
>
> music_object：True 将 song 转为 music 对象返回，False 将 song 以字典返回
>
> 成功返回数据 失败返回错误码
>
> ```json
> 返回数据的格式
> [
>  {
>  	播放次数
>      "song": music 数据/music 对象
> 	},
> 	{
>  	播放次数
>      "song": music 数据/music 对象
> 	},
>  ...
> ]
> ```
>
> 
>
> `user.follow(follow_in=True)`  关注该 user 对象用户 
>
> **参数说明:**
>
> follow_in：True 时关注，False 取消关注
>
> 成功返回0，失败返回错误码
>
> 
>
> ### **my 对象**
>
> 该对象继承于 user ，支持 user 所有方法属性
>
> ```python
> from pycloudmusic163 import Music163
> from pycloudmusic163.object import my
> my = my(Music163.music163_headers, {})
> 
> # my 对象扩展的属性
> 
> # 登录ip
> my.login_ip
> # 登录时间戳
> my.login_time
> # 登录时间戳转字符串，格式 "%Y/%m/%d %H:%M:%S"
> my.login_time_str
> ```
>
> 
>
> `my.recommend_playlist()`  获取日推
>
> `my.recommend_resource()`  获取每日推荐歌单
>
> `my.fm()`  私人fm，实例化一个fm对象并返回
>
> `my.message()`  私信，实例化一个message对象并返回
>
> `my.event()`  动态，实例化一个event对象并返回
>
> `my.sublist_artist(page=0, limit=25)`  查看该 my 对象收藏的歌手
>
> `my.sublist_album(page=0, limit=25)`  查看该 my 对象用户收藏的专辑
>
> `my.sublist_dj(page=0, limit=25)`   查看该 my 对象用户收藏的电台
>
> `my.sublist_mv(page=0, limit=25)`  查看该 my 对象用户收藏的 MV
>
> `my.sublist_topic(page=0, limit=50)`  查看该 my 对象用户收藏的专题
>
> **以上 sublist 方法的参数说明:**
>
> page：页数
>
> limit：一页获得数量
>
> 
>
> `my.cloud(page=0, limit=30)`  获取云盘数据，并实例化一个cloud对象返回
>
> **参数说明:**
>
> page：页数
>
> music_id：一页获得数量
>
> 
>
> `my.sign(type_=True)`  使用该 my 对象签到
>
> **参数说明:**
>
> type_：True 为安卓端签到3点经验，False 为网页签到2点经验
>
> 成功返回0，失败返回错误码
>
> 
>
> `playmode_intelligence(self, music_id, sid=None, playlist_id=None)`  心动模式/智能播放
>
> **参数说明:**
>
> music_id：歌曲id
>
> sid：可选 要开始播放的歌曲的id
>
> playlist_id：歌单id 默认使用喜欢的歌曲歌单
>
> 成功返回数据 失败返回错误码
>
> 
>
> ### **message 对象**
>
> 使用 my 对象生成，也可以如下生成
>
> ```python
> from pycloudmusic163 import Music163
> from pycloudmusic163.object import message
> 
> # 如下生成无法保证 cookie 有效性, 使用 my 对象生成保证了 cookie 有效性
> headers = Music163.music163_headers
> headers["cookie"] += "用户cookie"
> message = message(headers, "用户uid")
> ```
>
> 
>
> `message.comments(before_time=-1, limit=30)`  获取回复我
>
> **参数说明:**
>
> before_time：取上一页最后一个歌单的 updateTime，获取下一页数据
>
> limit：一页获取量
>
> 成功返回数据 失败返回错误码
>
> 
>
> `message.forwards(page=0, limit=30)`  获取@我
>
> **参数说明:**
>
> page：页数
>
> limit：一页获取量
>
> 成功返回数据 失败返回错误码
>
> 
>
> `message.notices(last_time=-1, limit=30)`  获取通知
>
> **参数说明:**
>
> last_time：传入上一次返回结果的 time，将会返回下一页的数据
>
> limit：一页获取量
>
> 成功返回数据 失败返回错误码
>
> 
>
> `message.private_new()`  获取最接近联系人
>
> `message.private_history(id_, page=0, limit=30, user_object=True)`  获取指定用户历史私信
>
> **参数说明:**
>
> id_：用户id
>
> page：页数
>
> limit：一页获取量
>
> user_object：True 将 user 转为 user 对象返回，False 将 user 以 json 返回
>
> 成功返回数据 失败返回错误码
>
> ```json
> 返回数据的格式
> [
>  {
>  	私信数据
>      "fromUser": user 数据/user 对象
>      "toUser": user 数据/user 对象
> 	},
> 	{
>  	私信数据
>      "fromUser": user 数据/user 对象
>      "toUser": user 数据/user 对象
> 	},
>  ...
> ]
> ```
>
> 
>
> `message.private(page=0, limit=30, user_object=True)` 获取私信列表
>
> **参数说明:**
>
> page：页数
>
> limit：一页获取量
>
> user_object：True 将 user 转为 user 对象返回，False 将 user 以 json 返回
>
> 成功返回数据 失败返回错误码
>
> 返回数据的格式同`message.private_history`
>
> 
>
> `message.send(msg, to_user_id, user_object=True)`  发送私信
>
> `message.send_music(msg, id_, to_user_id, user_object=True)`  发送私信 带歌曲
>
> `message.send_album(msg, id_, to_user_id, user_object=True)`  发送私信 带专辑
>
> `message.send_playlist(msg, id_, to_user_id, user_object=True)`  发送私信 带歌单
>
> **以上发送私信的参数说明:**
>
> id_：用户id
>
> page：页数
>
> limit：一页获取量
>
> id_：需一起发送的资源 id
>
> user_object：True 将 user 转为 user 对象返回，False 将 user 以 json 返回
>
> 成功返回第一位发送给的用户历史私信 失败返回错误码
>
> 
>
> ### **event 对象**
>
> 使用 my 对象生成，也可以如下生成
>
> ```python
> from pycloudmusic163 import Music163
> from pycloudmusic163.object import event
> 
> # 如下生成无法保证 cookie 有效性, 使用 my 对象生成保证了 cookie 有效性
> headers = Music163.music163_headers
> headers["cookie"] += "用户cookie"
> event = event(headers)
> ```
>
> 
>
> `event.event(last_time=-1, limit=30)`  获取下一页动态 保存至self.music_list
>
> 参数说明:
>
> last_time：传入上一次返回结果的 time,将会返回下一页的数据
>
> limit：一页获取量
>
> 成功返回0 失败返回错误码
>
> 
>
> `event.user_event(user_id, last_time=-1, limit=30)`  获取下一页动态 保存至self.music_list
>
> 参数说明:
>
> user_id：用户id
>
> last_time：传入上一次返回结果的 time,将会返回下一页的数据
>
> limit：一页获取量
>
> 成功返回0 失败返回错误码
>
> 
>
> `event.del_(ev_id)` 删除cookie用户动态
>
> 参数说明:
>
> ev_id：动态id
>
> 成功返回0 失败返回错误码
>
> 
>
> `event.send(msg)`  发送动态
>
> `event.send_music(msg, id_)` 发送动态 带歌曲
>
> `event.send_playlist(msg, id_)`  发送动态 带歌单
>
> `event.send_mv(msg, id_)`  发送动态 带MV
>
> `event.send_dj(msg, id_)`  发送动态 带电台
>
> `event.send_dj_music(msg, id_)`  发送动态 带电台节目
>
> **以上发送动态的参数说明:**
>
> msg：内容，140 字限制，支持 emoji，@用户名
>
> id_：需一起发送的资源 id
>
> 成功返回0 失败返回错误码
>
> 
>
> ### **_event 对象**
>
> 遍历 event 对象时生成，迭代返回
>
> ```python
> from pycloudmusic163 import Music163
> from pycloudmusic163.object import _event
> music = _event(Music163.music163_headers, {})
> 
> # _event 对象的属性
> 
> # 资源类型
> _event.data_type
> # 动态发布用户
> _event.user
> # 动态发布用户转字符串
> _event.user_str
> # 动态内容
> _event.msg
> # 动态图片
> _event.pics
> # 动态话题
> _event.act_name
> # 动态类型
> _event.type
> # 动态类型转字符串
> _event.type_str
> # 动态id
> _event.id
> # 动态id(ev_id)
> _event.ev_id
> # 动态分享数
> _event.share_coun
> # 动态评论数
> _event.comment_count
> # 动态点赞数
> _event.like_count
> # 动态时间
> _event.event_time
> ```
>
> 
>
> `_event.forward(msg)` 指定该  _event 对象转发到cookie用户
>
> 参数说明:
>
> msg：内容
>
> ev_id：转发动态id
>
> 成功返回0 失败返回错误码
>
>  
>
> ### **fm对象**
>
> 使用 my 对象生成，也可以如下生成
>
> ```python
> from pycloudmusic163 import Music163
> from pycloudmusic163.object import fm
> 
> # 如下生成无法保证 cookie 有效性, 使用 my 对象生成保证了 cookie 有效性
> headers = Music163.music163_headers
> headers["cookie"] += "用户cookie"
> fm = fm(headers)
> ```
>
> 
>
> `fm.read()` 获取fm歌曲
>
> `fm.write(id_)` 将歌曲扔进垃圾桶 (优化推荐)
>
> **参数说明:**
>
> id_：歌曲id
>
> 成功返回 (0,垃圾桶歌曲数) 失败返回错误码
>
>  
>
> ### **cloud 对象**
>
> ```python
> from pycloudmusic163 import Music163
> from pycloudmusic163.object import cloud 
> cloud = cloud(Music163.music163_headers, {})
> 
> # cloud 对象的属性
> 
> # 云盘歌曲数
> cloud.cloud_count
> # 云盘最大容量
> cloud.max_size
> # 云盘已用容量
> cloud.size
> # 云盘当时页歌曲数据
> cloud.music_list
> ```
>
> 
>
> `cloud.get(page=0, limit=30)`  获取云盘数据 保存至self.music_list
>
> **参数说明:**
>
> page：页数
>
> limit：一页获取量
>
> 成功返回0 失败返回错误码
>
>  
>
> `cloud.music(id_)` 获取云盘歌曲详细数据
>
> **参数说明:**
>
> id_：云盘歌曲id 支持多id使用列表 (self.music_list中的songId)
>
> 成功返回数据 失败返回错误码
>
>  
>
> `cloud.del_(id_)` 删除云盘歌曲
>
> **参数说明:**
>
> id_：云盘歌曲id 支持多id使用列表 (self.music_list中的songId)
>
> 成功返回0 失败返回错误码
>
> 
>
> ### **cloud_music 对象**
>
> 遍历 cloud 对象时生成，迭代返回
>
> ```python
> from pycloudmusic163 import Music163
> from pycloudmusic163.object import music
> music = music(Music163.music163_headers, {})
> 
> # cloud_music 对象的属性
> 
> # 云盘歌曲id
> self.id
> # 标题
> self.name
> # 歌曲大小
> self.file_size
> # 歌曲文件名
> self.file_name
> # 歌手
> self.artist
> # 专辑
> self.album
> # 封面
> self.cover
> # 上传时间
> self.add_time
> ```
>
> 
>
> `cloud_music.set_music_data(id_, user_id)` 云盘歌曲信息匹配纠正 (不知道怎么用)
>
> **参数说明:**
>
> id_：要匹配的歌曲 id
>
> user_id：用户 id
>
> 成功返回数据 失败返回错误码
>
> 
>
> 下载该 music 对象歌曲 (使用 app 播放接口)  这个接口相当于在 app 中点击播放
>
> `cloud_music.play(download_path, son_path="", chunk_size=1024, download_callback=None, quality=None)`
>
> **参数说明:**
>
> 参数参考`music.music_download`
>
> 
>
> ### **music 对象**
>
> ```python
> from pycloudmusic163 import Music163
> from pycloudmusic163.object import music
> music = music(Music163.music163_headers, {})
> 
> # music 对象的属性
> 
> # 资源类型
> music.data_type
> # 歌曲id
> music.id
> # 标题列表 [大标题, 副标题]
> music.name
> # 标题转字符串
> music.name_str
> # 作者列表 [作者, 作者, ...]
> music.artist
> # 作者列表转字符串
> music.artist_str
> # 专辑列表
> music.album_data
> # 专辑列表转字符串
> music.album_str
> # 所有音质
> music.quality
> # mv id
> music.mv_id
> # 发表时间
> music.publish_time
> # True时获取完成资源链接后直接返回(不进行下载)
> music.not_download = False
> ```
>
> 
>
> `music.similar_playlist()`  该 music 对象的相似歌单
>
> `music.similar_user()`  最近5个听了这 music 对象的用户
>
> `music.album()`  实例化该对像专辑 album 对像 并返回 album 对像
>
> `music.mv()`  获取该对像 mv 实例化 mv 对像 并返回 mv 对像
>
> `music.like(like)`  红心该 music 对象与取消红心
>
> **参数说明:**
>
> like：红心 True 取消红心 False
>
> 成功返回0 失败返回错误码
>
> 
>
> `music.lyric()` 该 music 对象的歌词
>
> **参数说明:**
>
> 成功返回(类型码,歌词) 失败返回错误码
>
> ```
> 类型码
> 0 滚动歌词 
> 1 不滚动歌词 
> 2 纯音乐 
> 3 暂无歌词
> ```
>
> 
>
> 下载该 music 对象歌曲 (使用 app 下载接口) 这个接口相当于在 app 中点击下载
>
> `music.music_download(download_path, son_path="", chunk_size=1024, download_callback=None, quality=None)`
>
> **参数说明:**
>
> download_path：下载目录
>
> son_path：下载至 下载目录下的子目录
>
> chunk_size：字节流大小
>
> download_callback：文件保存前回调 可设置文件名 默认文件名格式  **id_大标题.mp3**
>
> quality：音质
>
> 成功下载返回0 获取下载 url 失败时返回错误码
>
> download_callback 详细使用查看继承类（Link）download 方法说明
>
> 错误码 -105需要会员
>
> 
>
> 下载该 music 对象歌曲 (使用 app 播放接口)  这个接口相当于在 app 中点击播放，会员歌曲返回试听
>
> `music.play(download_path, son_path="", chunk_size=1024, download_callback=None, quality=None)`
>
> **参数说明:**
>
> 参数参考`music.music_download`
>
> 
>
> ### **playlist 对象**
>
> ```python
> from pycloudmusic163 import Music163
> from pycloudmusic163.object import playlist
> playlist = playlist(Music163.music163_headers, {})
> 
> # playlist 对象的属性
> 
> # 资源类型
> playlist.data_type
> # 歌单id
> playlist.id
> # 歌单标题
> playlist.name
> # 歌单封面
> playlist.cover
> # 歌单创建者
> playlist.user
> # 歌单创建者转字符串
> playlist.user_str
> # 歌单tags列表
> playlist.tags
> # 歌单tags转字符串
> playlist.tags_str
> # 歌单描述
> playlist.description
> # 歌单播放量
> playlist.play_count
> # 歌单收藏量
> playlist.subscribed_count
> # 歌单创建时间
> playlist.create_time
> # 歌单歌曲
> playlist.music_list
> ```
>
> 
>
> `playlist.add(music_id)`  向 playlist 对像添加歌曲
>
> **参数说明:**
>
> music_id：歌曲i d 支持多歌曲 id (使用列表)
>
> 成功返回0，失败返回错误码
>
> 
>
> `playlist.del_(self, music_id)`  向 playlist 对像删除歌曲
>
> **参数说明:**
>
> music_id：歌曲 id 支持多歌曲 id (使用列表)
>
> 成功返回0，对像剩余歌曲数，失败返回错误码
>
> 
>
> `playlist.subscribers(page=0, limit=20)`  查看歌单收藏者
>
> **参数说明:**
>
> page：页数
>
> music_id：一页获得数量
>
> 成功返回数据，失败返回错误码
>
> 
>
> ### **artist对象**
>
> ```python
> from pycloudmusic163 import Music163
> from pycloudmusic163.object import artist
> artist = artist(Music163.music163_headers, {})
> 
> # artist 对象的属性
> 
> # 歌手id
> artist.id
> # 歌手
> artist.name
> # 歌手简介
> artist.brief_desc_str
> artist.brief_desc
> # 专辑数
> artist.album_size
> # 单曲数
> artist.music_size
> # mv数
> artist.mv_size
> # 头像
> artist.cover
> ```
>
>   
>
> `artist.song_top()` 获取该对像热门50首 保存至self.music_list
>
> `artist.song(hot=True, page=0, limit=100)`  获取该对像歌曲 保存至self.music_list
>
> **参数说明:**
>
> hot：True 按热度排序 False 按时间排序
>
> page：页数
>
> limit：一页获取数量
>
> 成功返回0 失败返回错误码
>
>  
>
> `artist.album(page=0, limit=30)`  获取该对像专辑
>
> **参数说明:**
>
> page：页数
>
> limit：一页获取数量
>
> 成功返回数据, 失败返回错误码
>
> 
>
> ### **album对象**
>
> ```python
> from pycloudmusic163 import Music163
> from pycloudmusic163.object import album
> album = album(Music163.music163_headers, {})
> 
> # album 对象的属性
> 
> # 专辑id
> album.id
> # 专辑标题
> album.name
> # 专辑封面
> album.cover
> ```
>
> 
>
> `album.song()`  获取该对像专辑内容 保存至self.music_list (初始化 album 对象时会调用一次)
>
> 
>
> ### **mv对象**
>
> ```python
> from pycloudmusic163 import Music163
> from pycloudmusic163.object import mv
> mv = mv(Music163.music163_headers, {})
> 
> # mv 对象的属性
> 
> mv.data_type
> # mv id
> mv.id
> # mv标题
> mv.name
> # mv介绍
> mv.desc
> # mv歌手
> mv.artists
> mv.artists_str
> # mv tags
> mv.tags
> mv.tags_str
> # mv封面
> mv.cover
> # mv播放数
> mv.play_count
> # mv收藏数
> mv.subscribe_count
> # mv评论数
> mv.comment_count
> # mv分享数
> mv.share_count
> # mv质量
> mv.quality
> # 发布时间
> mv.publish_time
> # True时获取完成资源链接后直接返回(不进行下载)
> mv.not_download
> ```
>
>   
>
> 获取播放该mv对象指定的视频文件 参数参考`music.music_download`
>
> `mv.play(download_path, son_path="", chunk_size=1024, download_callback=None, quality=1080)`
>
> 
>
> ### **dj对象**
>
> ```python
> from pycloudmusic163 import Music163
> from pycloudmusic163.object import dj
> dj = dj(Music163.music163_headers, {})
> 
> # dj 对象的属性
> 
> # 电台标题
> dj.name
> # 电台id
> dj.id
> # 电台封面
> dj.cover
> # 电台创建者
> dj.user
> dj.user_str
> # 电台描述
> dj.description
> # 电台tags
> dj.tags
> # 电台分享量
> dj.share_count
> # 电台收藏量
> dj.subscribed_count
> # 电台单曲数
> dj.music_count
> dj.create_time
> ```
>
>  
>
> `dj.music(page=0, limit=30, asc=False)` 获取电台节目 保存在self.music_list
>
> **参数说明:**
>
> page：页数
>
> limit：一页获取数量
>
> asc：False 时间正序 True 时间倒序
>
> 成功返回0, 失败返回错误码
>
> 
>
> ### **dj_music对象**
>
> ```python
> from pycloudmusic163 import Music163
> from pycloudmusic163.object import dj_music
> dj_music = dj(Music163.music163_headers, {})
> 
> # dj_music 对象的属性
> 
> dj_music.data_type
> # 电台节目id
> dj_music.id
> # 电台节目标题
> dj_music.name
> # 电台节目简介
> dj_music.description
> # 电台节目封面
> dj_music.cover
> # 电台节目创建时间
> dj_music.create_time
> # 电台节目播放量
> dj_music.play_count
> # 电台节目点赞量
> dj_music.like_count
> # 电台节目评论量
> dj_music.comment_count
> ```
>
> 
>
> 下载该 music 对象歌曲 (使用 app 播放接口)  这个接口相当于在 app 中点击播放
>
> `dj_music.play(download_path, son_path="", chunk_size=1024, download_callback=None, quality=None)`
>
> **参数说明:**
>
> 参数参考`music.music_download`
