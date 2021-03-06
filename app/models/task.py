from google.appengine.ext import db
from django.utils import simplejson

class Task(db.Model):
    claimed  = db.BooleanProperty(default=False)
    complete = db.BooleanProperty(default=False)

    # --------------------------------------------------------------------------
    # Class Methods
    # --------------------------------------------------------------------------
    
    @classmethod
    def task(self, task_id):
        """
        Given a task id, return the task with that primary key.
        
        :Parameters:
            task_id : int
                Primary key of a task to look up
                
        :rtype: Task
        :returns: The task of the given id
        """
        return db.get(task_id)

    def as_json(self):
        params = {
            'resource': self.job.resource_url,
            'job_id':   str(self.job.key()),
            'task_id':  str(self.key())
        }
        params.update(self.json_params())
        return simplejson.write(params)