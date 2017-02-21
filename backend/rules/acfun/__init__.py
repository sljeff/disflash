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
    if url_path.find('acfun.cn') == -1:
        raise Return(False)

    script_path = os.path.join(_file_path, 'acfun_html5.js')
    with open(script_path, 'r') as f:
        content = f.read()
        request_handler.write(content)
    yield request_handler.flush()
    raise Return(True)

def proxy(url_path, request_handler):
    return False
