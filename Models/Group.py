from sqlalchemy import Column, Integer, String, Text
from Utils.DBConnection import DBConnection

base = DBConnection.Instance().getBase()

class Group(base):
    __tablename__ = "Groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    groupId = Column(String(255))
    calendarURL = Column(Text)

    def __init__(self, groupId, calendarURL):
        self.groupId = groupId
        self.calendarURL = calendarURL