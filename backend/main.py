# coding: utf-8
from tornado.web import RequestHandler, Application
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from tornado import ioloop, httpserver, gen
import os
import rules
import df_util
import sys

executor = ThreadPoolExecutor(10)
file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(file_path)


class BaseHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Credentials', 'true')

        xheaders = self.request.headers.get('Access-Control-Request-Headers')
        if xheaders is not None:
            self.set_header('Access-Control-Allow-Headers', xheaders)
            self.set_header('Access-Control-Expose-Headers', xheaders)

        origin = self.request.headers.get('Origin')
        allow_origin = origin or '*'
        self.set_header('Access-Control-Allow-Origin', allow_origin)

    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass

    def options(self, *args, **kwargs):
        self.set_status(200, 'OK')


class ScriptHandler(BaseHandler):
    @gen.coroutine
    def get(self, url_path):
        self.set_header('Content-Type', 'application/javascript')
        yield rules.get_script(url_path, self)


class ProxyHandler(BaseHandler):
    executor = executor
    @run_on_executor
    def get(self, url_path):
        """
        :type url_path: str
        """
        self.request.headers['Host'] = url_path.split('/')[2]
        rules.proxy(url_path, self)


class UtilHandler(BaseHandler):
    @gen.coroutine
    def get(self, util_name):
        yield df_util.get_util(util_name, self)


# build application
settings = {
    'static_path': os.path.join(file_path, 'static')
}

app = Application([
    (r'/getscript/(.*)', ScriptHandler),
    (r'/proxy/(.*)', ProxyHandler),
    (r'/util/(.*)', UtilHandler),
], **settings)

# start server
cr_path = os.path.join(file_path, 'rules', '__gen_cer')
main_server = httpserver.HTTPServer(app, ssl_options={
    "certfile": os.path.join(cr_path, 'localhost.pem'),
    "keyfile": os.path.join(cr_path, 'localhost.key')
})
main_server.listen(9527)
ioloop.IOLoop.current().start()
