FROM python:3.9


WORKDIR /code
RUN pip install --upgrade pip
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin
ADD ./requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt
ADD . /code/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]