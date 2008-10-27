from google.appengine.ext import db

from app.models.job import Job
from app.models.task import Task

import logging

class ReduceTask(Task):
    job        = db.ReferenceProperty(Job, collection_name='reduce_tasks')
    map_values = db.StringListProperty()

    def update(self, params):
        output = []
        for key, value in params.items():
            output.append('%s\t%s' % (str(key), str(value)))
    
        job_output = '\n'.join(output) + '\n'
        if self.job.output is None:
            self.job.output = job_output
        else:
            self.job.output += job_output
            
        self.job.save()
        
        self.complete = True
        

    def json_params(self):
        map_values = []
        for v in self.map_values:
            map_values.append(v.split('\t'))
            
        return {
            'task_type':    'reduce',
            'reducer':      self.job.reducer,
            'data':         map_values,
        }