FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080
CMD [ "gunicorn", "app:app", "-b", "0.0.0.0:8080" ]
