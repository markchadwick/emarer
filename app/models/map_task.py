from google.appengine.ext import db

from app.models.job import Job
from app.models.task import Task
from lib.http_utils import fetch_chunk

import logging

class MapTask(Task):
    job = db.ReferenceProperty(Job, collection_name='map_tasks')
    
    start_byte = db.IntegerProperty()
    end_byte   = db.IntegerProperty()

    def update(self, params):
        reducers     = [r for r in self.job.reduce_tasks]
        num_reducers = len(reducers)
        map_values   = [[] for r in range(num_reducers)]
        
        for reducer, map_value in zip(reducers, map_values):
            map_value = reducer.map_values

        for key, value in params.items():
            db_val = str(key) + '\t' + str(value)
            map_values[hash(key)%num_reducers].append(db_val)
            
        for reducer, map_value in zip(reducers, map_values):
            reducer.map_values = map_value
            reducer.save()

    def json_params(self):
        return {
            'task_type':    'map',
            'start_byte':   self.start_byte,
            'end_byte':     self.end_byte,
            'mapper':       self.job.mapper,
            'combiner':     self.job.combiner,
            'data':         fetch_chunk(self.job.resource_url, self.start_byte, self.end_byte),
        }