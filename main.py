from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import hashlib
from datetime import datetime
import time
import random

RAND_MIN = 12345678 #随机数下界
RAND_MAX = 9876543210000000 #随机数上界
MAX_TIME_DELTA = 30 #时间差最多3秒

app = Flask(__name__) 
CORS(app, supports_credentials=True)

def hash_encription(secret, timestamp, rand):
    '''
    拼接参数并用SM3哈希加密
    '''
    concat = '{}{}{}'.format(secret, timestamp, rand)
    h = hashlib.new('sm3')
    h.update(bytes(concat, 'utf8'))
    return h.hexdigest()

def get_time():
    '''
    获得当前UTC时间戳
    '''
    now = datetime.utcnow()
    now_ts = time.mktime(now.timetuple())
    return now_ts

def check_time(ts):
    '''
    检验参数时间与当前时间的差值
    '''
    dt = datetime.fromtimestamp(ts)
    now = datetime.utcnow()
    t_delta = (now - dt).seconds
    if t_delta >= MAX_TIME_DELTA:
        return False
    return True 

def get_rand():
    '''
    获取随机数
    '''
    return random.randint(RAND_MIN, RAND_MAX)

def response(data, code):
    return make_response(
        jsonify(data), code
    )

@app.route('/encryptor', methods = ["POST"])
def encryptor():
    '''
    require: secret
    return: timestamp, random integer, encrypted content
    '''
    secret = request.form.get('secret', None)
    if not secret:
        return response({'message': 'no secret provided'}, 400)
    ts = get_time()
    rand = get_rand()
    X = hash_encription(secret, ts, rand)
    return response({
        'timestamp': str(ts),
        'random': rand,
        'encrpted': X}, 200)

@app.route('/verifier', methods = ["POST"])
def verifier():
    '''
    require: secret, timestamp, random integer, encrypted content
    return: True/False
    '''
    data = request.form
    secret = data.get('secret', None)
    ts = eval(data.get('timestamp', None))
    rand = data.get('random', None)
    X = data.get('encrpted', None)
    if None in [secret, ts, rand, X]:
        return response({'message': 'no enough data provided'}, 400)

    if not check_time(ts):
        return response({'result': False, 'message': 'encrpted content expired'}, 200)
    X_ = hash_encription(secret, ts, rand)
    if X_ != X:
        return response({'result': False, 'message': 'verification failed'}, 200)
    return response({'result': True, 'message': 'verification passed'}, 200)

if __name__ == '__main__':
    app.run(debug=True)
