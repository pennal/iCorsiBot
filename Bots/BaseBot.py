class BaseBot:
    def __init__(self):
        raise NotImplementedError

    def newEventAdded(self, event):
        raise NotImplementedError