FROM docker.io/python:3.6
WORKDIR /usr/src/xpc
COPY . /usr/src/xpc/
RUN pip install -r requirements.txt -i http://mirrors.tencentyun.com/pypi/simple --trusted-host=mirrors.te
ncentyun.com
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "web.wsgi"]