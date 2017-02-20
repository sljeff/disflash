from tornado.httpclient import AsyncHTTPClient, HTTPResponse
from tornado.gen import coroutine
import os

@coroutine
def get_util(util_name, request_handler):
    """
    :type util_name: str
    :type request_handler: tornado.web.RequestHandler
    :rtype: None
    """
    if util_name.startswith('get_ip'):
        conn = AsyncHTTPClient()
        for _ in range(10):
            res = yield conn.fetch('https://jsonip.com/')  # type: HTTPResponse
            if res.code == 200:
                break

        request_handler.set_status(res.code, reason=res.reason)
        del res.headers['Transfer-Encoding']
        for name, value in res.headers.items():
            request_handler.set_header(name, value)
        request_handler.write(res.body)
        request_handler.finish()
        # ip = request_handler.request.remote_ip
        # request_handler.write({'ip': ip})
        return

    file_path = os.path.abspath(os.path.dirname(__file__))

    if util_name.startswith('get_flvjs'):
        request_handler.set_header('Content-Type', 'application/javascript')
        flv_path = os.path.join(file_path, 'flv.min.js')
        with open(flv_path, 'r') as f:
            content = f.read()
            request_handler.write(content)
        yield request_handler.flush()
        return
