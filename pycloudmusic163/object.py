import time
from pycloudmusic163.py_API import Link
from pycloudmusic163 import Erorr

"""
 出现-460错误 尝试再cookie加上 "appver=2.7.1.198277; os=pc;"
"""

# music163 api
MUSIC163_API = "https://music.163.com"


# 基础类
class music163_object(Link):
    # 数据类型
    data_type = [
        "R_SO_4_",  # 歌曲
        "R_MV_5_",  # mv
        "A_PL_0_",  # 歌单
        "R_AL_3_",  # 专辑
        "A_DJ_1_",  # 电台节目
        "R_VI_62_",
        "A_EV_2_"
    ]

    def __init__(self, headers):
        super().__init__(headers)
        self.id = None
        self.name = None

    def comment(self, hot=True, page=0, limit=20, before_time=0):
        """
        该对象的评论

        :param hot:热门评论 True 全部评论 False
        :param page:页数
        :param limit:一页获取数量
        :param before_time:分页参数,取上一页最后一项的 time 获取下一页数据(获取超过5000条评论的时候需要用到)
        :return:成功返回数据 失败返回错误码
        """
        api = MUSIC163_API + ("/api/v1/resource/hotcomments" if hot else "/api/v1/resource/comments")
        post_data = {
            "rid": self.id, "limit": limit, "offset": limit * page, "beforeTime": before_time
        }
        data = self.link(api + "/%s%s" % (self.data_type, self.id), data=post_data, mode="POST")

        if hot:
            return data['hotComments'] if data["code"] == 200 else data["code"]
        else:
            return data['comments'] if data["code"] == 200 else data["code"]

    def comment_floor(self, comment_id, page=0, limit=20):
        """
        楼层评论

        :param comment_id:楼层评论id (comment返回的评论中的commentId)
        :param page:页数
        :param limit:一页获取数量
        :return:成功返回数据 失败返回错误码
        """
        api = MUSIC163_API + "/api/resource/comment/floor/get"
        post_data = {
            "parentCommentId": comment_id, "threadId": "%s%s" % (self.data_type, self.id), "limit": limit,
            "offset": limit * page
        }
        data = self.link(api, data=post_data, mode="POST")
        return data["data"] if data["code"] == 200 else data["code"]

    def __comment_set(self, mode, post_data):
        api = MUSIC163_API + "/api/resource/comments/" + mode
        post_data_ = {
            "threadId": "%s%s" % (self.data_type, self.id)
        }
        post_data.update(post_data_)
        data = self.link(api, data=post_data, mode="POST")
        return 0 if data["code"] == 200 else data["code"]

    def comment_add(self, content):
        """
        发送评论

        :param content:评论内容
        :return:成功返回0 失败返回错误码
        """
        post_data = {
            "content": content
        }
        return self.__comment_set("add", post_data)

    def comment_delete(self, comment_id):
        """
        删除评论

        :param comment_id:评论id
        :return:成功返回0 失败返回错误码
        """
        post_data = {
            "commentId": comment_id
        }
        return self.__comment_set("delete", post_data)

    def comment_reply(self, content, comment_id):
        """
        回复评论

        :param content:评论内容
        :param comment_id:评论id
        :return:成功返回0 失败返回错误码
        """
        post_data = {
            "commentId": comment_id,
            "content": content
        }
        return self.__comment_set("reply", post_data)

    @staticmethod
    def set_list_str(list_, and_="/"):
        data_str = ""
        for data in list_:
            data_str += "%s%s" % (data, and_)
        return data_str.rstrip(and_)

    def subscribe(self, in_):
        """
        对像 收藏/取消收藏

        :param in_:True 收藏 False 取消收藏
        :return:成功返回0 失败返回错误码
        """

        subscribe_mode = {
            "A_PL_0_": MUSIC163_API + "/api/playlist" + ('/subscribe' if in_ else '/unsubscribe'),
            "R_AL_3_": MUSIC163_API + "/api/album" + ("/sub" if in_ else "/unsub"),
        }

        api, post_data = "", {
            "id": self.id
        }

        if self.data_type == "R_SO_4_":
            raise Erorr.Music163ObjectException()

        data = self.link(subscribe_mode[self.data_type], data=post_data, mode="POST")
        return 0 if data["code"] == 200 else data["code"]


# 迭代工具类
class music_list_fun(Link):

    def __init__(self, headers):
        super().__init__(headers)
        # 存储music数据
        self.music_list = None
        self.data_len_ = None

    def __iter__(self):
        self.data_len_ = len(self.music_list) if self.music_list is not None else 1
        self.index = 0
        return self

    def __next__(self):
        if self.index == self.data_len_ - 1:
            raise StopIteration

        data = self.music_list[self.index]
        self.index += 1
        return music(self.get_headers(), data)


# music对象基础
class music_in(music163_object):

    def __init__(self, headers):
        super().__init__(headers)
        self.quality = None
        self.not_download = False

    def _download_music(self, api, post_data, download_path, son_path="", chunk_size=1024, download_callback=None):
        data = self.link(api, data=post_data, mode="POST")
        if data["code"] != 200:
            return data["code"]

        if type(data["data"]) == dict:
            if data['data']['code'] != 200:
                return data['data']["code"]
            music_url = data['data']['url']
        else:
            if data['data'][0]['code'] != 200:
                return data['data'][0]["code"]
            music_url = data['data'][0]['url']

        if self.not_download:
            return music_url

        if download_callback is None:
            def download_callback(req, path):
                return "%s_%s.mp3" % (self.id, self.name[0]), None

        self.download(download_path, [son_path, [music_url]], download_callback, chunk_size=chunk_size)
        return 0

    def play(self, download_path, son_path="", chunk_size=1024, download_callback=None, quality=None):
        """
        获取播放该music对象指定的歌曲文件\n
        参数参考music_download
        """
        api = "https://interface3.music.163.com/api/song/enhance/player/url"
        post_data = {
            "ids": '[' + str(self.id) + ']',
            "br": self.quality[quality]['br'] if quality is not None else 999000
        }
        return self._download_music(api, post_data, download_path, son_path, chunk_size, download_callback)


# 用户 user对象
class user(music_list_fun, Link):

    def __init__(self, headers, user_data):
        super().__init__(headers)
        # 用户uid
        self.id = user_data["profile"]["userId"]
        # 用户名称
        self.name = user_data["profile"]["nickname"]
        # 用户签名
        self.signature = user_data["profile"]["signature"]
        # 用户等级
        self.level = user_data["level"] if "level" in user_data else None
        # 头像
        self.cover = user_data["profile"]['avatarUrl']
        # 会员 0 无
        self.vip = user_data["profile"]["vipType"]

    def playlist(self, page=0, limit=30):
        """
        获取该对象的歌单

        :param page:页数
        :param limit:一页获取数量
        :return:成功返回0 失败返回错误码
        """
        api = MUSIC163_API + "/api/user/playlist"
        post_data = {
            "uid": self.id, "limit": limit, "offset": limit * page, "includeVideo": True
        }
        data = self.link(api, data=post_data, mode="POST")
        if data["code"] != 200:
            return data["code"]
        return [playlist(self.get_headers(), PlayList) for PlayList in data['playlist']]

    def like_music(self):
        """
        获取该对象喜欢的歌曲 保存至self.music_list

        :return:成功返回0 失败返回错误码
        """
        data = self.playlist(limit=1)
        if type(data) == int:
            return data
        like_list_id = data[0].id

        api = MUSIC163_API + "/api/v6/playlist/detail"
        post_data = {"id": like_list_id, "n": 100000}
        data = self.link(api, data=post_data, mode="POST")
        if data["code"] != 200:
            return data["code"]
        self.music_list = data['playlist']["tracks"]
        return 0

    def record(self, type_=True, music_object=True):
        """
        获取该对象听歌榜单

        :param type_:True 所有时间 False 最近一周
        :param music_object:True 将song转为music对象返回 False 将song以json返回
        :return:成功返回数据 失败返回错误码
        """
        api = MUSIC163_API + "/api/v1/play/record"
        post_data = {
            "uid": self.id, "type": 0 if type_ else 1
        }
        data = self.link(api, data=post_data, mode="POST")
        if data['code'] != 200:
            return data['code']

        if not music_object:
            return data["allData"] if type_ else data["weekData"]

        list_data = []
        for music_ in data["allData"] if type_ else data["weekData"]:
            list_data.append({
                "play_count": music_["playCount"],
                "score": music_["score"],
                "song": music(self.get_headers(), music_["song"])
            })
        return list_data


# 当前使用cookie的用户 my对象
class my(user):

    def __init__(self, headers, user_data):
        super().__init__(headers, user_data)
        # 登录ip
        self.login_ip = user_data["profile"]["lastLoginIP"]
        # 登录时间
        self.login_time = int(user_data["profile"]["lastLoginTime"] / 1000)
        self.login_time_str = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(self.login_time))

    def sign(self, type_=True):
        """
        使用该对象签到

        :param type_:True为安卓端签到 3点经验 False为网页签到,2点经验
        """
        api = MUSIC163_API + "/api/point/dailyTask"
        post_data = {
            "type": 0 if type_ else 1
        }
        data = self.link(api, data=post_data, mode="POST")
        return 0 if data["code"] == 200 else data["code"]

    def recommend_playlist(self):
        """
        获取日推 保存至self.music_list

        :return:成功返回0 失败返回错误码
        """
        api = MUSIC163_API + "/api/v3/discovery/recommend/songs"
        data = self.link(api, mode="POST")
        if data["code"] != 200:
            return data["code"]
        self.music_list = data["data"]["dailySongs"]
        return 0

    def recommend_resource(self):
        """
        获取每日推荐歌单

        :return:成功返回数据 失败返回错误码
        """
        api = MUSIC163_API + "/api/v1/discovery/recommend/resource"
        data = self.link(api, mode="POST")
        return data["recommend"] if data["code"] == 200 else data["code"]

    def fm(self):
        """
        私人fm 实例化一个fm对象 并返回
        """
        return fm(self.get_headers())


# 私人fm fm对象
class fm(Link):

    def __init__(self, headers):
        super().__init__(headers)

    def read(self):
        """
        获取fm歌曲

        :return:成功返回music对像列表 失败返回错误码
        """
        api = MUSIC163_API + "/api/v1/radio/get"
        data = self.link(api, mode="POST")
        return data["data"] if data["code"] == 200 else data["code"]

    def write(self, id_):
        """
        将歌曲扔进垃圾桶 (优化推荐)

        :param id_:歌曲id
        :return:成功返回 (0,垃圾桶歌曲数) 失败返回错误码
        """
        api = MUSIC163_API + "/api/radio/trash/add"
        post_data = {
            "songId": id_
        }
        data = self.link(api + "?alg=RT&songId=%s&time=%s" % (id_, int(time.time())), data=post_data, mode="POST")
        return 0, data['count'] if data["code"] == 200 else data["code"]


# 歌手 artist对象
class artist(music_list_fun, Link):

    def __init__(self, headers, artist_data):
        super().__init__(headers)
        # 歌手id
        self.id = artist_data["id"]
        # 歌手
        self.name = artist_data["name"]
        # 歌手简介
        self.brief_desc_str = artist_data["briefDesc"]
        self.brief_desc = artist_data["briefDesc"].split("\n")
        # 专辑数
        self.album_size = artist_data["albumSize"]
        # 单曲数
        self.music_size = artist_data["musicSize"]
        # mv数
        self.mv_size = artist_data["mvSize"]
        # 头像
        self.cover = artist_data["cover"]

    def song(self, hot=True, page=0, limit=100):
        """
        获取该对像歌曲 保存至self.music_list

        :param hot:True 按热度排序 False 按时间排序
        :param page:页数
        :param limit:一页获取数量 默认100
        :return:成功返回0 失败返回错误码
        """
        api = MUSIC163_API + "/api/v1/artist/songs"
        post_data = {
            "id": self.id,
            "order": 'hot' if hot else "time",
            "offset": limit * page,
            "limit": limit,
            "private_cloud": True,
            "work_type": 1
        }
        data = self.link(api, data=post_data, mode="POST")
        if data["code"] != 200:
            return data["code"]
        self.music_list = data['songs']
        return 0

    def song_top(self):
        """
        获取该对像热门50首 保存至self.music_list

        :return:成功返回0 失败返回错误码
        """
        api = MUSIC163_API + "/api/artist/top/song"
        post_data = {
            "id": self.id
        }
        data = self.link(api, data=post_data, mode="POST")
        if data["code"] != 200:
            return data["code"]
        self.music_list = data["songs"]
        return 0

    def album(self, page=0, limit=30):
        """
        获取该对像专辑

        :param page:页数
        :param limit:一页获取数量 默认30
        """
        api = MUSIC163_API + "/api/artist/albums"
        post_data = {
            "limit": limit, "offset": limit * page, "total": True,
        }
        data = self.link(api + "/%s" % self.id, data=post_data, mode="POST")
        return data["hotAlbums"] if data["code"] == 200 else data["code"]


# 歌单 playlist对象
class playlist(music_list_fun, music163_object):

    def __init__(self, headers, playlist_data):
        super().__init__(headers)

        # 资源类型
        self.data_type = self.data_type[2]
        # 歌单id
        self.id = playlist_data["id"]
        # 歌单标题
        self.name = playlist_data["name"]
        # 歌单封面
        self.cover = playlist_data['coverImgUrl']
        # 歌单创建者
        self.user = playlist_data['creator']
        self.user_str = playlist_data['creator']["nickname"]
        # 歌单tags
        self.tags = playlist_data['tags']
        self.tags_str = self.set_list_str(playlist_data['tags'])
        # 歌单描述
        self.description = playlist_data["description"]
        # 歌单播放量
        self.play_count = playlist_data["playCount"]
        # 歌单收藏量
        self.subscribed_count = playlist_data["subscribedCount"]
        # 歌单创建时间
        self.create_time = playlist_data["createTime"]
        # 歌单歌曲
        self.music_list = playlist_data["tracks"]

    def __tracks(self, mode, music_id):
        if type(music_id) != list:
            music_id = [str(music_id)]
        api = MUSIC163_API + "/api/playlist/manipulate/tracks"
        post_data = {
            "op": mode, "pid": self.id, "trackIds": str(music_id), "imme": "true"
        }
        data = self.link(api, data=post_data, mode="POST")
        return data

    def add(self, music_id):
        """
        向对像添加歌曲

        :param music_id:歌曲id 支持多歌曲id (使用列表)
        :return:成功返回0 失败返回错误码
        """
        data = self.__tracks("add", music_id)
        return 0 if data["code"] == 200 else data["code"]

    def del_(self, music_id):
        """
        向对像删除歌曲

        :param music_id:歌曲id 支持多歌曲id (使用列表)
        :return:成功返回0,对像剩余歌曲数 失败返回错误码
        """
        data = self.__tracks("del", music_id)
        return 0, data["count"] if data["code"] == 200 else data["code"]


# 专辑 album对象
class album(music_list_fun, music163_object):

    def __init__(self, headers, album_data):
        super().__init__(headers)
        self.data_type = self.data_type[3]
        self.id = album_data["id"]
        self.name = album_data["name"]
        self.cover = album_data['picUrl']
        # 初始化专辑内容
        self.song()

    def song(self):
        """
        获取该对像专辑内容 保存至self.music_list

        :return:成功返回0 失败返回错误码
        """
        api = MUSIC163_API + "/api/v1/album"
        data = self.link(api + "/%s" % self.id, mode="POST")
        if data["code"] != 200:
            return data["code"]
        self.music_list = data["songs"]
        return 0


# 歌曲 music对象
class music(music_in):

    def __init__(self, headers, music_data):
        super().__init__(headers)
        # 资源类型
        self.data_type = self.data_type[0]
        # 歌曲id
        self.id = music_data['id']
        # 标题列表 [大标题, 副标题]
        self.name = [music_data['name'], music_data["alia"][0] if music_data["alia"] != [] else ""]
        self.name_str = self.name[0] + self.name[1]
        # 作者列表 [作者, 作者, ...]
        self.artist = [{"id": artist["id"], "name": artist["name"]} for artist in music_data['ar']]
        self.artist_str = self.set_list_str([author["name"] for author in self.artist])
        # 专辑列表
        self.album_data = music_data["al"]
        if "tns" in self.album_data:
            self.album_str = self.album_data["name"] + " " + (
                self.album_data["tns"][0] if self.album_data["tns"] != [] else "")
        else:
            self.album_str = self.album_data["name"]
        # 所有音质
        self.quality = {3: music_data["h"], 2: music_data["m"], 1: music_data["l"]}
        # mv id
        self.mv_id = music_data["mv"]
        # 发表时间
        if "publishTime" in music_data:
            self.publish_time = music_data["publishTime"]
        else:
            self.publish_time = None

        # True时获取完成资源链接后直接返回(不进行下载)
        self.not_download = False

    def __similar(self, api, limit=50):
        post_data = {
            "songid": self.id, "limit": limit, "offset": 0,
        }
        data = self.link(api, data=post_data, mode="POST")
        return data

    def similar(self, limit=50):
        """
        该music对象的相似歌曲

        :param limit:
        :return:成功返回数据 失败返回错误码
        """
        data = self.__similar(MUSIC163_API + "/api/v1/discovery/simiSong", limit)
        return data['songs'] if data["code"] == 200 else data["code"]

    def similar_playlist(self, limit=50):
        """
        该music对象的相似歌单
        参数参考similar
        """
        data = self.__similar(MUSIC163_API + "/api/discovery/simiPlaylist", limit)
        return data['playlists'] if data["code"] == 200 else data["code"]

    def like(self, like):
        """
        红心该music对象与取消红心

        :param like:红心 True 取消红心 False
        :return:成功返回0 失败返回错误码
        """
        api = MUSIC163_API + "/api/radio/like"
        post_data = {
            "alg": 'itembased', "trackId": self.id, "like": like, "time": '3'
        }
        data = self.link(api, data=post_data, mode="POST")
        return 0 if data["code"] == 200 else data["code"]

    def lyric(self):
        """
        该music对象的歌词
        类型码 -> 0 滚动歌词 1 不滚动歌词 2 纯音乐 3 暂无歌词

        :return:成功返回(类型码,歌词) 失败返回错误码
        """
        api = MUSIC163_API + "/api/song/lyric"
        post_data = {
            "id": self.id, "lv": -1, "kv": -1, "tv": -1,
        }
        code, data = 0, self.link(api, data=post_data, mode="POST")
        if data["code"] != 200:
            return data["code"]

        if data["lrc"]["lyric"] != "":
            if data["lrc"]["version"] == 8:
                code, data = 0, {
                    "trans_user": data["transUser"], "lyric_user": data["lyricUser"], "lyric": data["lrc"]["lyric"],
                    "tlyric": data["tlyric"]["lyric"]
                }
            else:
                code, data = 0, {
                    "trans_user": data["transUser"], "lyric_user": data["lyricUser"], "lyric": data["lrc"]["lyric"],
                    "tlyric": data["tlyric"]["lyric"]
                }

        elif 'nolyric' in data or (not data["sfy"] and not data["qfy"]):
            code, data = 2, {}
        else:
            code, data = 3, {}

        return code, data

    def music_download(self, download_path, son_path="", chunk_size=1024, download_callback=None, quality=None):
        """
        下载该music对象指定的歌曲\n
        错误码 -105需要会员\n
        download_callback 详细使用查看继承类 download方法说明

        :param download_path:下载目录
        :param son_path:下载至 下载目录下的子目录
        :param chunk_size:字节流大小
        :param download_callback:文件保存前回调 可设置文件名 默认文件名格式 id_大标题.mp3
        :param quality:音质
        :return:成功下载返回0 获取下载url失败时返回错误码
        """
        api = MUSIC163_API + "/api/song/enhance/download/url"
        post_data = {
            "id": self.id,
            "br": self.quality[quality]['br'] if quality is not None else 999000
        }
        return self._download_music(api, post_data, download_path, son_path, chunk_size, download_callback)

    def album(self):
        """
        实例化该对像专辑album对像 并返回album对像
        """
        return album(self.get_headers(), self.album_data)

    def mv(self):
        """
        获取该对像mv实例化mv对像 并返回album对像

        :return:返回mv对像
        """
        if self.mv_id == 0:
            return None
        api = MUSIC163_API + "/api/v1/mv/detail"
        post_data = {
            "id": self.mv_id
        }
        data = self.link(api, data=post_data, mode="POST")
        return mv(self.get_headers(), data) if data["code"] == 200 else data["code"]


# mv mv对象
class mv(music163_object):

    def __init__(self, headers, mv_data):
        super().__init__(headers)
        self.data_type = self.data_type[1]
        # mv id
        self.id = mv_data['data']["id"]
        # mv标题
        self.name = mv_data['data']["name"]
        # mv介绍
        self.desc = mv_data["data"]["desc"]
        # mv歌手
        self.artists = mv_data["data"]["artists"]
        self.artists_str = self.set_list_str([artists['name'] for artists in self.artists])
        # mv tags
        self.tags = mv_data["data"]["videoGroup"]
        self.tags_str = self.set_list_str([tags['name'] for tags in self.tags])
        # mv封面
        self.cover = mv_data["data"]["cover"]
        # mv播放数
        self.play_count = mv_data["data"]["playCount"]
        # mv收藏数
        self.subscribe_count = mv_data["data"]["subCount"]
        # mv评论数
        self.comment_count = mv_data["data"]["commentCount"]
        # mv分享数
        self.share_count = mv_data["data"]["shareCount"]
        # mv质量
        self.quality = mv_data["data"]["brs"]
        # 发布时间
        self.publish_time = mv_data["data"]["publishTime"]


# 电台歌曲 dj_music对象
class dj_music(music_in):

    def __init__(self, headers, dj_music_data):
        super().__init__(headers)
        self.data_type = self.data_type[4]
        self.id = dj_music_data["id"]
        self.name = dj_music_data["name"]
        self.description = dj_music_data["description"]
        self.cover = dj_music_data["coverUrl"]
        self.create_time = dj_music_data["createTime"]
        self.play_count = dj_music_data["listenerCount"]
        self.like_count = dj_music_data["likedCount"]
        self.comment_count = dj_music_data["commentCount"]


# 电台 dj对象
class dj(music_list_fun, Link):

    def __init__(self, headers, dj_data):
        super().__init__(headers)
        # 电台标题
        self.name = dj_data["name"]
        # 电台id
        self.id = dj_data["id"]
        # 电台封面
        self.cover = dj_data['picUrl']
        # 电台创建者
        self.user = dj_data['dj']
        self.user_str = self.user["nickname"]
        # 电台描述
        self.description = dj_data["desc"]
        # 电台tags
        self.tags = dj_data['category']
        # self.tags_str = self.set_list_str(playlist_data['tags'])
        # 电台分享量
        self.share_count = dj_data["shareCount"]
        # 电台收藏量
        self.subscribed_count = dj_data["subCount"]
        # 电台单曲数
        self.music_count = dj_data["programCount"]
        # 电台创建时间
        self.create_time = dj_data["createTime"]

    def __next__(self):
        if self.index == self.data_len_:
            raise StopIteration

        data = self.music_list[self.index]
        self.index += 1
        return dj_music(self.get_headers(), data)

    def music(self, page=0, limit=30, asc=False):
        api = MUSIC163_API + "/api/dj/program/byradio"
        post_data = {
            "radioId": self.id, "limit": limit, "offset": limit * page, "asc": asc
        }
        data = self.link(api, data=post_data, mode="POST")
        if data["code"] != 200:
            return data["code"]

        self.music_list = data["programs"]
        return 0
