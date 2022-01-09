FROM python:3-alpine

EXPOSE 8080

COPY requirements.txt /

RUN apk add zlib-dev jpeg-dev gcc musl-dev bash freetype-dev
RUN pip3 install -r requirements.txt

WORKDIR /app

ADD src /app
ADD images /app/images

ENTRYPOINT ["python3", "bot.py"]