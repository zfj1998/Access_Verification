import requests
import ipdb
import time
import json

SECRET = 'qiop8qCBi8Ttvhjk'
FAKE_SECRET = 'qiop8qCBi8Ttvhjl' 

host = 'http://localhost:8008'
encryptor_url = host + '/encryptor'
verifier_url = host + '/verifier'

def encryption():
    data = {
        'secret': SECRET
    }
    start = time.time()
    resp = requests.post(encryptor_url, data)
    end = time.time()
    print('{}ms'.format((end-start)*1000))
    print(json.loads(resp.content))
    return json.loads(resp.content)

def check(data):
    data['secret']=SECRET
    # data['secret']=FAKE_SECRET # 可靠性测试
    # time.sleep(3) # 超时测试
    start = time.time()
    resp = requests.post(verifier_url, data)
    end = time.time()
    print('{}ms'.format((end-start)*1000))
    print(json.loads(resp.content))

if __name__ == "__main__":
    check(encryption())