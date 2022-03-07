# pic_sender

The purpose of this project is to build a bot capable of process soical media
post links, harvest its multimedia content (photos, videos) and send that content
through Telegram. Currently, the system only supports Twitter and Reddit links, but
we might extend it to other sites, such as Instagram.

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

To test the bot:

```
python src/bot.py
```
