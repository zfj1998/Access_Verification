FROM python:3.6

RUN mkdir /access_verification
WORKDIR /access_verification

COPY requirements.txt ./
COPY guni_conf.py ./
COPY main.py ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN mkdir logs

CMD gunicorn -c guni_conf.py main:app
