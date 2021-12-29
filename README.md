# pic_sender

How should we start?

1. We need a way to download an image, given a
link. This link can be either Reddit or Twitter
2. Create a Telegram bot that uses that code to
download the image, and then send it to a chat
3. Add the bot to the TG group

To clone this repo, run
```
git clone https://github.com/gabrielblancogarcia/pic_sender.git
``` 

To install the required libraries, run
```
pip install -r requirements.txt
```

Quick test:
```
cd pic_sender
source venv/bin/activate
python src/app.py
```

To run the tests:
```
cd pic_sender
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
pytest --cov
```