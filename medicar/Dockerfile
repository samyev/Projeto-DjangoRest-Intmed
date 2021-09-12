FROM python:3.8.10-alpine

WORKDIR /app

ADD requirements.txt /app
RUN pip3 install -r requirements.txt 
ADD . /app

ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000