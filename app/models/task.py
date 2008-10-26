from google.appengine.ext import db
from django.utils import simplejson

class Task(db.Model):
    claimed  = db.BooleanProperty(default=False)
    complete = db.BooleanProperty(default=False)
    
    def as_json(self):
        params = {
            'resource': self.job.resource_url,
            'job_id':   str(self.job.key()),
            'task_id':  str(self.key())
        }
        params.update(self.json_params())
        return simplejson.write(params)