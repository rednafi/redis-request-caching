FROM python:3.8.2-slim-buster


RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "flask_run:application"]
