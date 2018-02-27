from EventParser import *
import sys

# For now, this is like this. In the future, this will be taken from the bot or other settings
if len(sys.argv) == 1:
    print("Missing params. Calendar URL needed!")
    exit(0)

CALENDAR_URL = sys.argv[1]

parser = EventParser(CALENDAR_URL)
parser.parseContents()