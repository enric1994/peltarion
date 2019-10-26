FROM python:3.7

ADD docker/requirements_os.txt .
RUN apt update -y && apt install -y $(cat requirements_os.txt|grep -v '#')

ADD docker/requirements.txt .
RUN pip3 install -r requirements.txt
