#!/usr/bin/env python3

# WSS (WS over TLS) client example, with a self-signed certificate

import pathlib
import ssl
import websockets
import time
import json
import hashlib
import base64


def md5(str):
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()


def base64_str(str):
    return base64.b64encode(str.encode(encoding='utf-8')).decode("utf-8")


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

user = 'bskbitop@gmail.com'
api_pwd = '4WXX7IC9UVFJMCB1'
ut = str(int(time.time()))
code = md5(base64_str((md5(api_pwd)[4:23] + user + ut)))
ws_url = 'wss://wsapi.17ce.com:8001/socket/?ut=' + ut + '&code=' + code + '&user=' + user


async def hello(domain):
    uri = ws_url
    async with websockets.connect(
            uri, ssl=ssl_context
    ) as websocket:
        j = {"txnid": 1,
             "nodetype": [1, 2],
             "num": 2,
             "Url": 'http://%s/' % domain,
             "TestType": 'HTTP',
             "TimeOut": 10,
             "Request": 'GET',
             "NoCache": True,
             "Speed": 0,
             "Cookie": '',
             "Trace": False,
             "UserAgent": 'curl/7.47.0',
             "FollowLocation": 2,
             "GetMD5": True,
             "GetResponseHeader": True,
             "MaxDown": 1048576,
             "AutoDecompress": True,
             "type": 1,
             "isps": [1, 2, 7],
             # "pro_ids": [12, 180, 183, 184, 188, 189, 190, 192, 193, 194, 195, 196, 221, 227, 235, 236, 238, 239, 241,
             #             243, 250, 346, 349, 350, 351, 352, 353, 354, 355, 356, 357, 49, 79, 80],
             "pro_ids": [49, 250, 350, 235],
             "areas": [1]}

        send_str = json.dumps(j)
        await websocket.send(send_str)
        result = list()
        try:
            while 1:
                rt = json.loads(await websocket.recv())
                result.append(rt)
                if rt.get('type') == 'TaskEnd':
                    break
        except Exception as e:
            print(e)

        return result



