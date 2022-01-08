import logging
import os
from config import config

from app.twitter_client import TwitterClient
from app.reddit_client import RedditClient

from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

TOKEN = config.TELEGRAM_CONFIG["bot_token"]


import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:

    input_message = update.message.text
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    
    image_name = 'downloaded_image'
    image_folder = 'images'


    if 'reddit' in input_message:
    
        reddit_client = RedditClient(
            config=config,
            logger=logger,
            url=input_message
        )
        
        reddit_client.download_image(image_name)  # TODO: split download and save?
        
        # DANGER: format must come from the class, not hardcoded
        image_path = os.path.join(image_folder, image_name + reddit_client._image_format)
        
        update.message.bot.send_photo(
        chat_id=chat_id,
        reply_to_message_id = message_id,
        photo=open(image_path, 'rb')
        )
        
        os.remove(image_path)
        logger.info('Image removed')


    if 'twitter' in input_message:
        twitter_client = TwitterClient(
            config=config,
            logger=logger,
            url=input_message
        )

        twitter_client.download_image(image_name)
        image_path = os.path.join(image_folder, image_name + '.jpg')
        
        
        update.message.bot.send_photo(
        chat_id=chat_id,
        reply_to_message_id = message_id,
        photo=open(image_path, 'rb')
        )

        os.remove(image_path)
        logger.info('Image removed')


    


def main() -> None:
    """Start the bot."""
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()