from Models.Assignment import Assignment
import requests
from icalendar import Calendar

class EventParser:
    def __init__(self, calendarURL):
        self.calendarURL = calendarURL

    def __fetchCalendar(self):
        req = requests.get(self.calendarURL)
        cal = Calendar.from_ical(req.text)

        return cal

    def parseContents(self):
        content = self.__fetchCalendar()

        for event in content.walk("vevent"):
            a = Assignment.fromFetchedData(event)

            print(a)
