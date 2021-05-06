FROM python:3.9-slim-buster

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app
EXPOSE 5000
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "5000"]
