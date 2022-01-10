import os
from os import listdir
from os.path import isfile, join

from config import config

from app.twitter_client import TwitterClient
from app.reddit_client import RedditClient
from app.image_maker import ImageMaker
from app.logger_client import LoggerClient

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


TOKEN = config.TELEGRAM_CONFIG["bot_token"]
logger = LoggerClient(config).get_logger()

reddit_client = RedditClient(config=config, logger=logger)
twitter_client = TwitterClient(config=config, logger=logger) 
image_maker = ImageMaker(config=config, logger=logger)


# Define a few command handlers. These usually take the two arguments update and context.
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

def expendable_level(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /explevel is issued."""
    if not len(context.args) == 2:
        logger.info('Incorrect number of arguments in /explevel command')

    image_path = image_maker.create_image(context.args[0], context.args[1])
    if not image_path:
        return 

    photo = open(image_path, 'rb')
        
    update.message.bot.send_photo(
        chat_id=update.message.chat_id,
        reply_to_message_id=update.message.message_id,
        photo=photo
    )
        
    os.remove(image_path)
    logger.info('Image removed')

def send_pictures(update: Update, context: CallbackContext) -> None:

    if not update.message:
        return
    input_message = update.message.text

    # Download images using clients
    # TODO: If message is not just an url but an url + some text this might fail
    if 'reddit' in input_message:
        reddit_client.url = input_message 
        reddit_client.download_image('testing')  # TODO: split download and save?

    if 'twitter' in input_message:
        twitter_client.url = input_message
        twitter_client.download_image()

    image_folder = config.GLOBAL_CONFIG['image_folder']

    # Load and send images
    for image in [name for name in listdir(image_folder) if isfile(join(image_folder, name))]:        
        image_path = join(image_folder, image)
        photo = open(image_path, 'rb')
        
        update.message.bot.send_photo(
            chat_id=update.message.chat_id,
            reply_to_message_id=update.message.message_id,
            photo=photo
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
    dispatcher.add_handler(CommandHandler("explevel", expendable_level))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_pictures))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
