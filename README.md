## 功能
- 使用对称密钥进行身份认证
- 认证信息在30秒内过期
- 使用Web API，调用方便
- 使用Docker部署，各平台适用

## 双向认证流程
1. 客户端发出request之前，使用`加密API`获得认证参数[a,b..]。
2. 在request header中放入认证参数[a,b..]，在request body中放入数据。
3. 服务端收到request后，使用`验证API`验证request header中的参数[a,b..]。
4. 服务端确认客户端的身份后，可向客户端发出response。
---
5. 服务端发出response之前，使用`加密API`获得认证参数[x,y..]。
6. 在response header中放入认证参数[x,y..]，在response body中放入数据。
7. 客户端收到response后，使用`验证API`验证response header中的参数[x,y..]。
8. 客户端对服务端身份进行确认，确认无误后再处理响应数据。

## API文档
- HOST = localhost:8008 
---
### 正常情况

| Ⅰ | 加密API |
| --- | ---|
| URL | HOST/encryptor |
| 请求方法 | POST |
| form-data | secret='qiop8qCBi8Ttvhjk' |
| response | 'timestamp': 1601107988.0</br>'random': 18513242</br>'encrpted': '83e1d52a0665...' |
---
| Ⅱ | 验证API |
| --- | ---|
| URL | HOST/verifier |
| 请求方法 | POST |
| form-data | secret='qiop8qCBi8Ttvhjk'</br>timestamp=1601107988.0</br>random=18513242</br>encrpted='83e1d52a0665...' |
| response | 'result': True</br>'message': 'verification passed' |
---
### 异常情况
| 加密API | 异常处理 |
| --- | ---|
| 未提供secret参数 | 状态码400，返回message：'no secret provided' |
---
| 验证API | 异常处理 |
| --- | ---|
| 参数未提供完整 | 状态码400，返回message：'no enough data provided' |
| 验证信息超时 | 状态码200，返回message：'encrpted content expired' |
| 密钥不正确 | 状态码200，返回message：'verification failed' |

## 部署指南
1. 进入项目根目录（main.py所在的目录）
2. 创建docker image  
`docker build -t verification_service .`
3. 创建并在后台运行docker container  
`docker run -d -p 8008:8008 verification_service`
4. 在宿主机访问  
`http://localhost:8008/verifier`

## 参考用例
API使用方法见[示例代码](func_test.py)