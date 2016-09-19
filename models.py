from zerodb.models import Model, Field, Text
import time

class Measurement(Model):
    roomID = Field()
    nodeID = Field()
    value = Field()
    date = Field()

    def __repr__(self):
        return "<%s in %s measured %s watts at %s>" % (self.nodeID, self.roomID, self.value, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(self.date)))

class State(Model):
    roomID = Field()
    nodeID = Field()
    desc = Text()
    state = Field()

    states=["locked","closed","open","unknown"]

    def __repr__(self):
        return "<%s #%s in %s is %s>" % (self.desc, self.nodeID, self.roomID, self.states[int(repr(self.state))])
