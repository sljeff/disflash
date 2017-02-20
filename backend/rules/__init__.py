from importlib import import_module
from tornado.gen import coroutine
from tornado.web import asynchronous
import os
import sys

__all__ = ['get_script', 'proxy']
_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(_file_path)

# add rules
_rules = []
for dir_name in os.listdir(_file_path):
    if os.path.isdir(os.path.join(_file_path, dir_name)) and not dir_name.startswith('_'):
        _rules.append(import_module(dir_name))


# functions

@coroutine
def get_script(url, request_handler):
    """
    :type url: str
    :type request_handler: tornado.web.RequestHandler
    """
    request_handler.set_header('Content-Type', 'application/javascript')
    for rule in _rules:
        result = yield rule.script(url, request_handler)
        if result is True:
            break
    if result is False:
        script = _not_match_script()
        request_handler.write(script)
        yield request_handler.flush()


def proxy(url, request_handler):
    """
    :type url: str
    :type request_handler: tornado.web.RequestHandler
    """
    for rule in _rules:
        result = rule.proxy(url, request_handler)
        if result is True:
            break
    if result is False:
        request_handler.finish()


def _not_match_script():
    no_match_path = os.path.join(_file_path, 'not_match_script.js')
    with open(no_match_path, 'r') as f:
        script = f.read()
    return script
