FROM python:3-alpine

EXPOSE 8080

COPY requirements.txt /
RUN pip3 install -r requirements.txt

WORKDIR /app

ADD src /app

ENTRYPOINT ["python3", "bot.py"]