from google.appengine.ext import db

from app.models.job import Job
from app.models.task import Task

class ReduceTask(Task):
    job        = db.ReferenceProperty(Job, collection_name='reduce_tasks')
    map_values = db.StringListProperty()

    def json_params(self):
        return {
            'task_type':    'reduce',
            'reducer':      self.job.reducer
        }    