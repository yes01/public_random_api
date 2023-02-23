FROM python:3.7.2-slim-stretch

WORKDIR /data/webapp

ADD ./. /data/webapp

RUN pip install -r requirements.txt

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

CMD python manage.py runserver -h 0.0.0.0 -D --threaded