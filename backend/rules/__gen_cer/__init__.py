# coding: utf-8
from OpenSSL import crypto

__all__ = ['create']

with open('dfRootCA.pem', 'r') as f:
    content = f.read()
    ca_crt = crypto.load_certificate(crypto.FILETYPE_PEM, content.encode())

with open('dfRootCA.key', 'r') as f:
    content = f.read()
    ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, content)


def create(hostname):
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)
    req = crypto.X509Req()
    req.get_subject().CN = hostname
    req.set_pubkey(key)
    req.sign(key, 'sha256')

    crt = crypto.X509()
    crt.set_subject(req.get_subject())
    crt.set_serial_number(666)
    crt.gmtime_adj_notBefore(0)
    crt.gmtime_adj_notAfter(512*24*60*60)
    crt.set_issuer(ca_crt.get_subject())
    crt.set_pubkey(req.get_pubkey())
    crt.sign(ca_key, 'sha256')

    with open(hostname+ '.pem', 'wt') as f:
        w = crypto.dump_certificate(crypto.FILETYPE_PEM, crt)  # type: bytes
        f.write(w.decode())
    with open(hostname+ '.key', 'wt') as f:
        w = crypto.dump_privatekey(crypto.FILETYPE_PEM, key)  # type: bytes
        f.write(w.decode())
