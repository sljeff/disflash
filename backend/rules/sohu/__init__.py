from tornado.gen import coroutine, Return
import os

__all__ = ['script', 'proxy']
_file_path = os.path.abspath(os.path.dirname(__file__))


@coroutine
def script(url, request_handler):
    if url.find('tv.sohu.com') != -1:
        script_path = os.path.join(_file_path, 'sohu_html5.js')
        with open(script_path, 'r') as f:
            content = f.read()
            request_handler.write(content)
        yield request_handler.flush()
        raise Return(True)
    raise Return(False)


def proxy(url, request_handler):
    if url.startswith('http://m.tv.sohu.com'):
        real_url = request_handler.request.uri.split('/proxy/')[1]
        headers = {}
        for n, v in request_handler.request.headers.items():
            headers[n] = v
        headers['Host'] = url.split('/')[2]
        if headers.get('Origin') is not None:
            del headers['Origin']

        import requests
        for _ in range(10):
            res = requests.get(real_url, headers=headers)
            if res.status_code == 200:
                break
            else:
                if _ == 10:
                    break
                res.close()
                continue

        request_handler.set_header('Set-Cookie', res.headers.get('Set-Cookie'))
        request_handler.set_header('Content-Type', 'application/json')
        request_handler.write(res.text)
        request_handler.flush()
        return True

    if url.startswith('http://hot.vrs.sohu.com/'):
        real_url = request_handler.request.uri.split('/proxy/')[1]
        headers = {}
        for n, v in request_handler.request.headers.items():
            headers[n] = v
        headers['Host'] = url.split('/')[2]
        headers['Origin'] = 'http://m.tv.sohu.com'

        import requests
        for _ in range(10):
            res = requests.get(real_url, headers=headers)
            if res.status_code == 200:
                break
            else:
                if _ == 10:
                    break
                res.close()
                continue

        r_headers = {n: v for n, v in res.headers.items() if not n.startswith('Access') and n.find('Encoding') == -1}
        for n, v in r_headers.items():
            request_handler.set_header(n, v)
        result = add_proxy_to_m3u8(res.text)
        request_handler.write(result)
        request_handler.finish()
        return True

    if url.startswith('sohum3u8/'):
        real_url = request_handler.request.uri.split('/sohum3u8/')[1]
        headers = {}
        for n, v in request_handler.request.headers.items():
            headers[n] = v
        headers['Host'] = real_url.split('/')[2]
        headers['Origin'] = 'http://m.tv.sohu.com'
        if headers.get('X-Cookie') is not None:
            headers['Cookie'] = headers.get('X-Cookie')
            del headers['X-Cookie']
        if headers.get('DNT') is not None:
            del headers['DNT']
        headers['Referer'] = 'http://m.tv.sohu.com/v3357313.shtml?aid=9142496&channeled=1210010100&columnid=1'
        headers['X-Playback-Session-Id'] = '81548AAF-40DF-46F9-8FC1-D991E7B3C376'
        headers['User-Agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D27 Safari/602.1'

        import requests
        for _ in range(10):
            res = requests.get(real_url, stream=True, headers=headers)
            if res.status_code == 200:
                break
            else:
                if _ == 9:
                    break
                res.close()
                continue

        r_headers = {n: v for n, v in res.headers.items() if not n.startswith('Access')}
        if r_headers.get('Transfer-Encoding') is not None:
            del r_headers['Transfer-Encoding']
        for n, v in r_headers.items():
            request_handler.set_header(n, v)
        try:
            for chunk in  res.iter_content(4096):
                if not chunk:
                    break
                request_handler.write(chunk)
                request_handler.flush()
        finally:
            res.close()
            request_handler.finish()
            return True
    return False


def add_proxy_to_m3u8(m3u8_content):
    import io
    buf = io.StringIO(m3u8_content)
    result = io.StringIO()
    while True:
        line = buf.readline()
        if not line:
            break
        if line.startswith('http://'):
            line = 'https://localhost:9527/proxy/sohum3u8/' + line
        result.write(line)
    result.seek(0)
    return result.read()
