from zerodb.models import Model, Field, Text
import time

class Measurement(Model):
    mid = Text()
    value = Field()
    date = Field()

    def __repr__(self):
        return "<%s measured %s watts at %s>" % (self.mid, self.value, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(self.date)))
