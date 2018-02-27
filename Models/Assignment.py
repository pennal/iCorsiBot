from sqlalchemy import Column, Integer, String, Text, DateTime
from Utils.DBConnection import DBConnection

base = DBConnection.Instance().getBase()
from dateutil import tz


to_zone = tz.gettz("Europe/Zurich")

class Assignment(base):
    __tablename__ = "Assignments"
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    date = Column(DateTime)
    subject = Column(String(255))
    description = Column(Text)
    calendarURL = Column(String(255))

    def __init__(self, id, title, date, subject, description, calendarURL):
        self.id = id
        self.title = title
        self.date = date.astimezone(to_zone)
        self.subject = subject
        self.description = description
        self.calendarURL = calendarURL

    @staticmethod
    def fromFetchedData(event, calendarURL):
        assignmentId = int(event.get("UID").split("@")[0])
        title = str(event.get("summary"))
        date = event.get('dtstart').dt
        subject = str(event.get("categories"))
        description = str(event.get("description"))

        return Assignment(assignmentId, title, date, subject, description, calendarURL)

    def __repr__(self):
        return "====================\n{}\n{}\n{}\n{}\n{}\n====================".format(self.id, self.title, self.subject, self.description, self.date)

    def __eq__(self, other):
        return self.id == other.id