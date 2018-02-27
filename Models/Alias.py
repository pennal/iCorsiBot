from sqlalchemy import Column, Integer, String
from Utils.DBConnection import DBConnection

base = DBConnection.Instance().getBase()


class Alias:
    __tablename__ = "Alias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(255))
    name = Column(String(255))

    def __init__(self, code, name):
        self.code = code
        self.name = name
