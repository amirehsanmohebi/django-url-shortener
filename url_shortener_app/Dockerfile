FROM python:3.9


RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin
COPY requirements.txt /code/

RUN pip install -r requirements.txt
COPY . /code/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]