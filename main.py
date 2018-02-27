from EventParser import *
import sys
from Utils.DBConnection import *
from Bots.TelegramBot import TelegramBot
import schedule
import time


def fetchNewEvents(parser):
    oldEventsQuery = DBConnection.Instance().getSession().query(Assignment).all()

    # Transform into an id -> Assignment map
    oldEvents = {}
    for e in oldEventsQuery:
        oldEvents[e.id] = e

    newEvents = parser.parseContents()
    savedEvents = []

    for e in newEvents:
        try:
            _ = oldEvents[e.id]
        except:
            # Event does not exist. Therefore save it in the DB
            savedEvents.append(e)
            DBConnection.Instance().save(e)

            # Notify any listener of the fact that we have new events
            bot.newEventAdded(e)

# For now, this is like this. In the future, this will be taken from the bot or other settings
if len(sys.argv) < 2:
    print("Missing params")
    exit(0)

BOT_API_KEY = sys.argv[1]

# Init the DB
DBConnection.Instance().createAllTables()

# Get the URLs for the calendars
groups = DBConnection.Instance().executeQuery("SELECT * FROM Groups")

# Instantiate a parser for each of the URLs
parsers = []
if groups is not None:
    for g in groups:
        parsers.append(EventParser(g.calendarURL))

bot = TelegramBot(BOT_API_KEY)


for p in parsers:
    fetchNewEvents(p)

# # Scheduling happens here!
# schedule.every(10).seconds.do(fetchNewEvents)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)

# Last command is initializing the bot

bot.initializeBot()


