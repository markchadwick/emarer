from google.appengine.ext import db

from app.models.job import Job
from app.models.task import Task

class MapTask(Task):
    job = db.ReferenceProperty(Job, collection_name='map_tasks')
    
    start_byte = db.IntegerProperty()
    end_byte   = db.IntegerProperty()
    

    def json_params(self):
        return {
            'task_type':    'map',
            'start_byte':   self.start_byte,
            'end_byte':     self.end_byte,
        }