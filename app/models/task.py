from google.appengine.ext import db

class Task(db.Model):
    complete = db.BooleanProperty(default=False)
    