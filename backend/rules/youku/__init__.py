# coding: utf-8
import os
from tornado.gen import coroutine, Return
from tornado.httpclient import HTTPClient, HTTPError

__all__ = ['script', 'proxy']
_file_path = os.path.abspath(os.path.dirname(__file__))


@coroutine
def script(url_path, request_handler):
    """
    :type url_path: str
    :type request_handler: tornado.web.RequestHandler
    :rtype: bool
    """
    if not url_path.startswith('http://v.youku.com/v_show/'):
        Return(False)

    request_handler.set_header('Content-Type', 'application/javascript')
    script_path = os.path.join(_file_path, 'youku_html5.js')
    with open(script_path, 'r') as f:
        content = f.read()
        request_handler.write(content)
    yield request_handler.flush()
    Return(True)


def proxy(url_path, request_handler):
    """
    :type url_path: str
    :type request_handler: tornado.web.RequestHandler
    :rtype: bool
    """
    if url_path.startswith('http://play-ali.youku.com/play/get.json'):
        real_url = request_handler.request.uri.split('/proxy/')[1]
        headers = {}
        for n, v in request_handler.request.headers.items():
            headers[n] = v
        headers['Referer'] = 'http://m.youku.com/video/id_{}.html'.format(real_url[real_url.rfind('?vid=') + 5:-5])
        headers['Origin'] = 'http://m.youku.com'
        headers['Host'] = url_path.split('/')[2]
        headers['Cookie'] = headers.get('X-Cookie')
        del headers['X-Cookie']

        conn = HTTPClient()
        for _ in range(10):
            try:
                res = conn.fetch(real_url, headers=headers)
            except HTTPError:
                continue
            else:
                break
        request_handler.write(res.body)
        request_handler.flush()
        return True
    if url_path.startswith('http://k.youku.com/player/getFlvPath/'):
        real_url = request_handler.request.uri.split('/proxy/')[1]
        headers = {}
        for n, v in request_handler.request.headers.items():
            headers[n] = v
        headers['Host'] = url_path.split('/')[2]
        headers['Origin'] = 'http://m.youku.com'

        import requests
        for _ in range(10):
            res = requests.get(real_url, stream=True, headers=headers)
            if res.status_code == 200:
                break
            else:
                if _ == 8:
                    break
                res.close()
                continue

        r_headers = {n: v for n, v in res.headers.items() if not n.startswith('Access')}
        for n, v in r_headers.items():
            request_handler.set_header(n, v)
        try:
            for chunk in res.iter_content(4096):
                if not chunk:
                    break
                request_handler.write(chunk)
                request_handler.flush()
        finally:
            request_handler.finish()
            return True

    return False

