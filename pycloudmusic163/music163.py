from pycloudmusic163.object import *
from pycloudmusic163.py_API import Link

# music163 api
MUSIC163_API = "https://music.163.com"
MUSIC163_MUSIC_API = "https://interface3.music.163.com"


class LoginMusic163(Link):

    def __init__(self, headers=None):
        super().__init__(headers)
        if headers is None:
            self.headers = self.music163_headers

    def __set_cookie(self):
        cookie = "appver=2.7.1.198277; os=pc;"
        for name, value in self.req.cookies.items():
            cookie += '{0}={1};'.format(name, value)

        headers = self.headers
        headers["cookie"] = cookie
        self.headers = headers
        return Music163(headers), cookie

    def login_email(self, email, password):
        """
        邮箱登录\n
        错误码:501 未注册 502 密码错误\n

        :param email:邮箱
        :param password:密码
        :return:成功返回Music163对象, cookie 失败返回错误码
        """
        api = MUSIC163_API + "/api/login"
        post_data = {
            "username": email,
            "password": self._md5(password),
            "rememberLogin": 'true'
        }
        data = self._link(api, data=post_data, mode="POST")
        if data["code"] != 200:
            return data["code"]

        music163_object, cookie = self.__set_cookie()
        return music163_object, cookie

    def login_captcha(self, phone, country_code="86"):
        """
        发送验证码

        :param phone:手机号
        :param country_code:国家码 (用于国外手机号登录)
        :return:成功返回0 失败返回错误码
        """
        api = MUSIC163_API + "/api/sms/captcha/sent"
        post_data = {
            "ctcode": country_code,
            "cellphone": phone
        }
        data = self._link(api, data=post_data, mode="POST")
        return 0 if data["code"] == 200 else data["code"]

    def login_cellphone(self, phone, password, captcha=False, country_code="86"):
        """
        手机/验证码 登录\n
        错误码:400 手机号格式错误 501 未注册 502 密码错误 503 验证码错误\n

        :param phone:手机号
        :param password:验证参数
        :param captcha:True时为验证码登录 password值为验证码 False时为密码登录 password值为密码
        :param country_code:国家码 (用于国外手机号登录)
        :return:成功返回Music163对象, cookie 失败返回错误码
        """
        if not captcha:
            password = self._md5(password)

        api = MUSIC163_API + "/api/login/cellphone"
        post_data = {
            "phone": phone,
            "countrycode": country_code,
            "captcha" if captcha else "password": password,
            "rememberLogin": 'true'
        }
        data = self._link(api, data=post_data, mode="POST")
        if data["code"] != 200:
            return data["code"]

        music163_object, cookie = self.__set_cookie()
        return music163_object, cookie

    def login_qr_key(self):
        """
        获取二维码key

        :return:成功返回二维码key 失败返回错误码
        """
        api = MUSIC163_API + "/api/login/qrcode/unikey"
        post_data = {
            "type": 1
        }
        data = self._link(api, data=post_data, mode="POST")
        return data["unikey"], "https://music.163.com/login?codekey="+data["unikey"] if data["code"] == 200 else data["code"]

    def login_qr(self, qr_key):
        """
        二维码登录 查询二维码状态

        状态码:801 等待扫码 802 授权中 800 二维码不存在或已过期 803 登录成功
        :return:成功返回状态码, Music163对象, cookie 失败返回状态码
        """
        api = MUSIC163_API + "/api/login/qrcode/client/login"
        post_data = {
            'key': qr_key,
            'type': 1
        }
        data = self._link(api, data=post_data, mode="POST")
        if data["code"] != 803:
            return data["code"], "", ""

        music163_object, cookie = self.__set_cookie()
        return 803, music163_object, cookie

    def logout(self, cookie):
        """
        退出登录
        """
        headers = self.music163_headers
        headers["cookie"] += cookie
        self.headers = headers

        api = MUSIC163_API + "/api/logout"
        data = self._link(api, mode="POST")
        return data if data["code"] == 200 else data["code"]
    
    def check_captcha(self, phone, captcha, country_code="86"):
        """
        校验验证码

        :param phone:手机号
        :param captcha:验证码
        :param country_code:国家码 (用于国外手机号)
        :return:校验成功返回True 校验失败返回False
        """
        api = MUSIC163_API + "/api/sms/captcha/verify"
        post_data = {
            "cellphone": phone, "captcha": captcha,"countrycode": country_code,
        }
        data = self._link(api, data=post_data, mode="POST")
        return data['data'] if data["code"] == 200 else False

    def check_cellphone(self, phone, country_code="86"):
        """
        检查手机号是否被注册

        :param phone:手机号
        :param country_code:国家码 (用于国外手机号)
        :return:未注册返回None 被注册返回用户名 api错误返回错误码
        """
        api = MUSIC163_API + "/api/cellphone/existence/check"
        post_data = {
            "cellphone": phone, "countrycode": country_code,
        }
        data = self._link(api, data=post_data, mode="POST")
        if data["code"] != 200:
            return data["code"]
        
        if data["exist"] == 1:
            return data["nickname"]

        return None
    
    def register(self, name, phone, password, captcha, country_code="86"):
        """
        手机 注册/修改密码

        :param name:昵称
        :param phone:手机号
        :param password:密码
        :param captcha:验证码
        :param country_code:国家码 (用于国外手机号)
        :return:成功返回Music163对象, cookie 失败返回错误码
        """
        api = MUSIC163_API + "/api/register/cellphone"
        post_data = {
            "phone": phone,
            "countrycode": country_code,
            "captcha": captcha,
            "password": self._md5(password),
            "nickname": name,
            "rememberLogin": 'true'
        }
        data = self._link(api, data=post_data, mode="POST")
        return data

    def replace_cellphone(self, phone, captcha, old_captcha, country_code="86"):
        """
        更换绑定手机

        :param phone:手机号
        :param captcha:新手机验证码
        :param old_captcha:原手机验证码
        :param country_code:国家码 (用于国外手机号)
        :return:
        """
        api = MUSIC163_API + "/api/user/replaceCellphone"
        post_data = {
            "cellphone": phone, "captcha": captcha, "oldcaptcha": old_captcha, "ctcode": country_code,
        }
        data = self._link(api, data=post_data, mode="POST")
        return data if data["code"] == 200 else data["code"]



class Music163(Link):
    """
    出现-460错误 尝试再cookie加上 "appver=2.7.1.198277; os=pc;"
    """

    @staticmethod
    def __id_format(id_, dict_str=False):
        if type(id_) == str or type(id_) == int:
            format_str = str([{"id": id_}]) if dict_str else str([id_])
        elif type(id_) == list and dict_str:
            list_ = []
            for data in id_:
                list_.append({"id": data})
            format_str = str(list_)
        else:
            format_str = str(id_)

        return format_str

    def my(self):
        """
        获取当前cookie用户信息并实例化my对像\n
        cookie无效返回200

        :return:成功返回my对像，失败返回错误码
        """
        api = MUSIC163_API + "/api/w/nuser/account/get"
        data = self._link(api, mode="POST")
        if data["code"] != 200 or data["profile"] is None:
            return data["code"]
        return my(self.headers, data)

    def music(self, id_):
        """
        获取歌曲并实例化music对像

        :param id_:歌曲id 支持多id(使用列表)
        :return:成功返回music对像列表, 失败返回错误码
        """
        api = MUSIC163_API + "/api/v3/song/detail"
        post_data = {"c": self.__id_format(id_, dict_str=True)}
        data = self._link(api, data=post_data, mode="POST")
        if data["code"] != 200:
            return data["code"]
        return [music(self.headers, music_data) for music_data in data["songs"]]

    def user(self, id_):
        """
        获取用户并实例化user对像

        :param id_:用户id
        :return:成功返回user对像，失败返回错误码
        """
        api = MUSIC163_API + "/api/v1/user/detail"
        data = self._link(api + "/%s" % id_, mode="POST")
        return user(self.headers, data) if data["code"] == 200 else data["code"]

    def playlist(self, id_):
        """
        获取歌单并实例化playlist对像

        :param id_:歌单id
        :return:成功返回playlist对像，失败返回错误码
        """
        api = MUSIC163_API + "/api/v6/playlist/detail"
        post_data = {"id": id_, "n": 100000}
        data = self._link(api, data=post_data, mode="POST")
        return playlist(self.headers, data['playlist']) if data["code"] == 200 else data["code"]

    def artist(self, id_):
        """
        获取歌手并实例化artist对像

        :param id_:歌手id
        :return:成功返回playlist对像，失败返回错误码
        """
        api = MUSIC163_API + "/api/artist/head/info/get"
        post_data = {
            "id": id_
        }
        data = self._link(api, data=post_data, mode="POST")
        return artist(self.headers, data["data"]['artist']) if data["code"] == 200 else data["code"]

    def album(self, id_):
        """
        实例化专辑album对像 该方法实例化的album对像只有id 和专辑相关接口\n
        暂时没有直接获取专辑信息的方法\n
        不推荐这样获取album对像
        """
        album_data = {
            "id": id_, "name": None, "picUrl": None
        }
        return album(self.headers, album_data)

    def mv(self, id_):
        """
        获取mv并实例化mv对像

        :param id_:mv id
        :return:返回mv对像
        """
        api = MUSIC163_API + "/api/v1/mv/detail"
        post_data = {
            "id": id_
        }
        data = self._link(api, data=post_data, mode="POST")
        return mv(self.headers, data) if data["code"] == 200 else data["code"]

    def dj(self, id_):
        """
        获取电台并实例化dj对像

        :param id_:电台id
        :return:返回dj对像
        """
        api = MUSIC163_API + "/api/djradio/v2/get"
        post_data = {
            "id": id_
        }
        data = self._link(api, data=post_data, mode="POST")
        return dj(self.headers, data['data']) if data["code"] == 200 else data["code"]

    def search(self, key, type_=1, page=0, limit=30):
        """
        搜索\n
        返回的大部分内容都可以直接生成对象,不用二次请求\n
        type_: 1: 单曲, 10: 专辑, 100: 歌手, 1000: 歌单, 1002: 用户, 1004: MV, 1006: 歌词, 1009: 电台, 1014: 视频\n

        :param key:搜索内容
        :param type_:搜索类型
        :param page:页数
        :param limit:一页获取数量
        :return:成功返回内容 失败返回错误码
        """
        api = MUSIC163_API + "/api/cloudsearch/pc"
        post_data = {
            "s": key, "type": type_, "limit": limit, "offset": limit * page, "total": True
        }
        data = self._link(api, data=post_data, mode="POST")
        return data['result'] if data["code"] == 200 else data["code"]
    
    def personalized_playlist(self, limit=30):
        """
        推荐歌单

        :param limit:一页获取数量 (不支持 offset)
        :return:成功返回内容 失败返回错误码
        """
        api = MUSIC163_API + "/api/personalized/playlist"
        post_data = {
            "limit": limit, "total": "true", "n": 1000,
        }
        data = self._link(api, data=post_data, mode="POST")
        return data['result'] if data["code"] == 200 else data["code"]
    
    def personalized_new_song(self, areaId=0, limit=10):
        """
        推荐新歌

        :param limit:一页获取数量 (不支持 offset)
        :return:成功返回内容 失败返回错误码
        """
        api = MUSIC163_API + "/api/personalized/newsong"
        post_data = {
            "type": 'recommend', "limit": limit, "areaId": areaId,
        }
        data = self._link(api, data=post_data, mode="POST")
        return data['result'] if data["code"] == 200 else data["code"]
    
    def personalized_dj(self):
        """
        推荐电台

        :return:成功返回内容 失败返回错误码
        """
        api = MUSIC163_API + "/api/personalized/djprogram"
        data = self._link(api, mode="POST")
        return data['result'] if data["code"] == 200 else data["code"]
    
    def home_page(self, refresh=True, cursor=None):
        """
        首页-发现 app 主页信息

        :param refresh:是否刷新数据
        :param cursor:上一条数据返回的 cursor
        :return:成功返回内容 失败返回错误码
        """
        api = MUSIC163_API + "/api/homepage/block/page"
        post_data = {
            "refresh": refresh, "cursor": cursor
        }
        data = self._link(api, data=post_data, mode="POST")
        return data["data"] if data["code"] == 200 else data["code"]

    def top_artist_list(self, type_=1, page=0, limit=100):
        """
        歌手榜
        type_ 1: 华语, 2: 欧美, 3: 韩国, 4: 日本

        :param type_:地区类型
        :param page:页数
        :param limit:一页获取数量
        :return:成功返回内容 失败返回错误码
        """
        api = MUSIC163_API + "/api/toplist/artist"
        post_data = {
            "type": type_, "limit": limit, "offset": page * limit, "total": "true"
        }
        data = self._link(api, data=post_data, mode="POST")
        if data["code"] != 200:
            return data["code"]

        return data["list"]["artists"]

    def top_song(self, type_=0):
        """
        新歌速递\n
        全部:0 华语:7 欧美:96 日本:8 韩国:16
        
        :param type_:地区类型 id
        :return:成功返回内容 失败返回错误码
        """
        api = MUSIC163_API + "/api/v1/discovery/new/songs"
        post_data = {
            "areaId": type_, "total": "true"
        }
        data = self._link(api, data=post_data, mode="POST")
        return data["data"] if data["code"] == 200 else data["code"]