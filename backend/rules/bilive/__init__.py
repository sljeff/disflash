# coding: utf-8
import os
from tornado.gen import coroutine, Return

__all__ = ['script', 'proxy']
_file_path = os.path.abspath(os.path.dirname(__file__))

@coroutine
def script(url_path, request_handler):
    """
    :type url_path: str
    :type request_handler: tornado.web.RequestHandler
    :rtype: bool
    """
    if url_path.find('live.bilibili.com') == -1:
        raise Return(False)

    script_path = os.path.join(_file_path, 'bilive_html5.js')
    with open(script_path, 'r') as f:
        content = f.read()
        request_handler.write(content)
    yield request_handler.flush()
    raise Return(True)


def proxy(url_path, request_handler):
    """
    :type url_path: str
    :type request_handler: tornado.web.RequestHandler
    :rtype: bool
    """
    # if url_path.find('live.bilibili.com/msg/send') != -1:
    #     headers = {
    #         'Host': 'live.bilibili.com',
    #         'Connection': 'keep-alive',
    #         'Content-Length': '69',
    #         'Origin': 'http://static.hdslb.com',
    #         'X-Requested-With': 'ShockwaveFlash/24.0.0.221',
    #         'User-Agent': request_handler.request.headers.get('User-Agent'),
    #         'Content-Type': 'application/x-www-form-urlencoded',
    #         'Accept': '*/*',
    #         'DNT': '1',
    #         'Referer': 'http://static.hdslb.com/live-static/swf/LivePlayerEx_1.swf',
    #         'Accept-Encoding': 'gzip, deflate',
    #         'Accept-Language': 'zh-CN,zh;q=0.8',
    #         'Cookie': request_handler.request.headers.get('X-Cookie'),
    #     }
    #     import requests
    #     import time
    #     arr = request_handler.request.uri.split('/')
    #     msg = arr[-1] if arr[-1] != '' else arr[-2]
    #     res = requests.post('https://live.bilibili.com/msg/send', data={
    #         'color': 16777215,
    #         'fontsize': 25,
    #         'mode': 1,
    #         'msg': msg,
    #         'rnd': int(time.time()),
    #         'roomid': request_handler.get_argument('roomid'),
    #     }, headers=headers)
    #     request_handler.set_header('Content-Type', 'application/json')
    #     request_handler.write(res.content)
    #     request_handler.flush()
    #     return True

    return False
