class Assignment:
    def __init__(self, id, title, date, subject, description):
        self.id = id
        self.title = title
        self.date = date
        self.subject = subject
        self.description = description

    @staticmethod
    def fromFetchedData(event):
        assignmentId = event.get("UID").split("@")[0]
        title = event.get("summary")
        date = event.get('dtstart').dt
        subject = event.get("categories")
        description = event.get("description")

        return Assignment(assignmentId, title, date, subject, description)

    def __repr__(self):
        return "====================\n{}\n{}\n{}\n{}\n{}\n====================".format(self.id, self.title, self.subject, self.description, self.date)
