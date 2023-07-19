FROM python:3.9


WORKDIR /code
RUN pip install --upgrade pip
RUN apt-get update &&\
    apt-get install -y netcat-openbsd
ADD ./requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt
ADD . /code/
RUN mkdir /code/staticfiles
RUN chmod +x /code/wait-for-it.sh
EXPOSE 8000
