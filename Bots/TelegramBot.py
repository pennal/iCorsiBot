from Bots.BaseBot import BaseBot
from Models.Group import *

from Utils.DBConnection import *

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

CALENDAR_URL, ALIAS_NAME, ALIAS_SUBJECT = range(3)


class TelegramBot(BaseBot):
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

        self.updater = Updater(API_KEY)

        # Get the dispatcher to register handlers
        self.dp = self.updater.dispatcher

        # on different commands - answer in Telegram
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],

            states={
                CALENDAR_URL: [MessageHandler(Filters.text, self.calendarURL)]
            },

            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

        self.dp.add_handler(conv_handler)
        self.dp.add_handler(CommandHandler("unlink", self.unlink))


        # Start polling
        self.updater.start_polling()


    def start(self, bot, update):
        from_user = update.message.from_user

        # Query the DB and check if the group has already been added
        currentUser = DBConnection.Instance().executeQuery("SELECT * FROM `Group` WHERE groupId = {}".format(from_user.id), True)

        if currentUser == None:
            update.message.reply_text("Hi! Let us get started\n\n" +
                                      "Please provide the URL for the iCorsi calendar you want to be updated on")

            return CALENDAR_URL
        else:
            update.message.reply_text("Looks like everything has been already set up")


    def getUpdater(self):
        return self.updater


    def initializeBot(self):
        print("Bot has been initialized")
        self.updater.idle()


    def __icorsiCalendarURLIsValid(self, url):
        # TODO
        return True

    def calendarURL(self, bot, update):
        user_id = update.message.from_user.id
        message = update.message.text

        # Verify the URL
        if self.__icorsiCalendarURLIsValid(message):
            a = DBConnection.Instance().executeQuery("SELECT * FROM Groups WHERE groupId = {}".format(user_id), True)
            if a == None:
                group = Group(user_id, message)
                DBConnection.Instance().save(group)

            # ELSE: This is a weird case. The group may already be present in the DB

            update.message.reply_text("The bot has been set up!")
        else:
            update.message.reply_text("Looks like the provided URL is not valid. Please start again with the procedure")

    def unlink(self, bot, update):
        user_id = update.message.from_user.id

        # Remove the user from the Groups table
        DBConnection.Instance().executeRAWQuery("DELETE FROM Groups WHERE groupId = {}".format(user_id))

        update.message.reply_text("You have successfully been removed!")

    def cancel(self, update):
        user = update.message.from_user
        logger.info("User %s canceled the conversation.", user.first_name)
        update.message.reply_text('Bye! I hope we can talk again some day.')

        return ConversationHandler.END


    def newEventAdded(self, event):
        # Check and find which group the event belongs to
        groupId = DBConnection.Instance().executeQuery("SELECT * FROM Groups WHERE calendarURL = \"{}\"".format(event.calendarURL), True).groupId

        message = "New event added:\n\n{} - {}\n\n{}".format(event.title, event.subject, event.description)

        self.updater.bot.sendMessage(groupId, message)
