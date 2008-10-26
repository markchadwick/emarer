from google.appengine.ext import db

from app.models.job import Job
from app.models.task import Task

class ReduceTask(Task):
    job = db.ReferenceProperty(Job, collection_name='reduce_tasks')

    def json_params(self):
        return {
            'task_type':    'reduce',
        }    