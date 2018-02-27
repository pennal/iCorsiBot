from Patterns.Singleton import Singleton
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL = 'sqlite:///icorsi.db'

@Singleton
class DBConnection:
    def __init__(self):
        self.engine = create_engine(URL, echo=True)
        self.Base = declarative_base()

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        print("Engine created")

    def getSession(self):
        return self.session

    def getBase(self):
        return self.Base

    def createAllTables(self):
        self.Base.metadata.create_all(self.engine)

    def save(self, element):
        self.session.add(element)
        self.session.commit()

    def executeRAWQuery(self, query):
        currentSession = self.getSession()
        try:
            currentSession.execute(query)
        except:
            pass

    def executeQuery(self, query, flattenLists=False):
        currentSession = self.getSession()
        try:
            fetched = currentSession.execute(query)
        except:
            return None

        if fetched == None:
            return None

        dbData = []
        for f in fetched:
            dbData.append(f)

        if dbData == None or dbData == []:
            return None

        # In the case there is only one element, flatten the list and return the element itself
        if len(dbData) == 1 and flattenLists:
            return dbData[0]

        return dbData
