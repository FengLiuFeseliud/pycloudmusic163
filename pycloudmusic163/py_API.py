import hashlib
import os
import requests


class Link:

    # music163通用请求头
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://music.163.com',
        'Host': 'music.163.com',
        'cookie': "appver=2.7.1.198277; os=pc;",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }
    # md5对象
    __hl = hashlib.md5()
    # 字符编码
    __encoding = "utf-8"
    # 一次请求的requests对像
    req = None

    def __init__(self, headers):
        self.__headers = headers

    def set_headers(self, headers):
        self.__headers = headers

    def get_headers(self):
        return self.__headers

    def set_encoding(self, encoding):
        self.__encoding = encoding

    def cookie_key(self, key):
        cookie_key_ = {}
        for key_ in self.__headers["cookie"].split('; '):
            key_data = key_.split("=")
            if key.count(key_data[0]) != 0:
                if len(key) == 1:
                    return key_data[1]
                cookie_key_[key_data[0]] = key_data[1]

        return cookie_key_

    def md5(self, str_):
        self.__hl.update(str_.encode(encoding='utf-8'))
        return self.__hl.hexdigest()

    def link(self, api, mode="GET", data=None, files=None, json=True):
        if mode == "GET":
            with requests.get(api, headers=self.__headers, data=data, files=files) as req:
                req.encoding = self.__encoding
                data = req.json() if json else req.text
        elif mode == "POST":
            with requests.post(api, headers=self.__headers, data=data, files=files) as req:
                req.encoding = self.__encoding
                data = req.json() if json else req.text

        self.req = req
        return data

    def download(self, download_path, download_list, download_callback, chunk_size=1024, file_callback=None):
        """
        下载

        :param download_path:下载目录
        :param download_list:可以下载所以本模块调用返回的url列表
        :param chunk_size:字节流大小
        :param download_callback:文件保存前回调 可以处理响应,设置文件名 (requests对象,文件目录)
        :param file_callback:文件保存后回调(requests对象, 文件名, 下载目录)
        """
        path = "%s/%s" % (download_path, download_list[0])
        if not os.path.exists(path):
            os.makedirs(path)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        }

        for url in download_list[1]:
            with requests.get(url, headers=headers, stream=True) as req:
                download_file, download_str = download_callback(req, path)
                if download_file is not None:
                    with open("%s/%s" % (path, download_file), "wb") as file:
                        for chunk in req.iter_content(chunk_size):
                            file.write(chunk)
                    if file_callback is not None:
                        file_callback(req, download_file, path)