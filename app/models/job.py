from google.appengine.ext import db
from lib.http_utils import asset_size

import math
import logging

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------

DEFAULT_MAP_BYTES    = 1000
DEFAULT_NUM_REDUCERS = 15

# ------------------------------------------------------------------------------
# Implementation
# ------------------------------------------------------------------------------

class Job(db.Model):
    
    # --------------------------------------------------------------------------
    # Fields
    # --------------------------------------------------------------------------

    name    = db.StringProperty()

    mapper  = db.StringProperty(multiline=True)
    combiner= db.StringProperty(multiline=True)
    reducer = db.StringProperty(multiline=True)
    
    resource_url  = db.StringProperty()
    resource_size = db.IntegerProperty()
    num_mappers   = db.IntegerProperty()
    num_reducers  = db.IntegerProperty()
    
    map_complete = db.BooleanProperty(default=False)
    complete     = db.BooleanProperty(default=False)
    
    # --------------------------------------------------------------------------
    # Class Methods
    # --------------------------------------------------------------------------
    
    @classmethod
    def job(self, job_id):
        """
        Given a job id, return the job with that primary key.
        
        :Parameters:
            job_id : int
                Primary key of a job to look up
                
        :rtype: Job
        :returns: The Job of the given id
        """
        return db.get(job_id)

    # --------------------------------------------------------------------------
    # Public Methods
    # --------------------------------------------------------------------------

    def create_map_tasks(self):
        """
        Determine the number of map tasks which should be created for this
        resource.  If a job has already created map tasks, they will be
        destroyed, even if some of the map tasks are in progress or finished.
        
        TODO: This should reflect the size of the input file, and a configurable
              chunk size per file
        """
        from app.models.map_task import MapTask
        self._delete_map_tasks()
        
        self.resource_size = asset_size(self.resource_url)
        
        num_map_tasks = self.resource_size / float(DEFAULT_MAP_BYTES)
        num_map_tasks = int(math.ceil(num_map_tasks))
        self.num_mappers = num_map_tasks

        for i in range(num_map_tasks):
            start_byte = i * DEFAULT_MAP_BYTES
            end_byte   = ((i+1) * DEFAULT_MAP_BYTES) - 1
            end_byte   = self.resource_size if end_byte > self.resource_size else end_byte
            MapTask(job=self, start_byte=start_byte, end_byte=end_byte).save()
        
        self.save()

    def create_reduce_tasks(self):
        """
        Create a pre-determined number of reducers for a job.  This number,
        currently, is pre-set by the `num_reducers` field variable.  There is
        little advantage (and a number of potential problems) to making this
        dynamic.  Rather than figure them out for a silly hack, we will leave
        this staticlly set for the time being.
        
        TODO: This could possibly be based off some broad ratio of the input
              file.  Theoreticlly speaking, this doesn't make a lot of sense,
              but may work out practiclly.
        """
        from app.models.reduce_task import ReduceTask
        self._delete_reduce_tasks()
        
        for i in range(DEFAULT_NUM_REDUCERS):
            ReduceTask(job=self).save()
            
        self.num_reduce_tasks = DEFAULT_NUM_REDUCERS
        self.put()
        
    def next_task(self):
        """
        Returns the next task that needs computation.  This could be either a
        MapTask, ReduceTask, or None depending on the current state of the Job.
        
        :rtype: Task
        :returns: Next task which needs to be executed to complete this job, or
                  `None` if no such job exists.
        """
        if self.complete:
            return None
        
        #
        # Find available Map tasks
        #
        if not self.map_complete:
            task = self._next_map_task()
            if task is None:
                self.map_complete = True
                self.save()
                return self.next_task()
            else:
                return task
                
        #
        # Find available Reduce tasks
        #
        
        else:
            task = self._next_reduce_task()
            
            if task is None:
                self.complete = True
                save.save()
                return None
            else:
                return task
        
    # --------------------------------------------------------------------------
    # Private Methods
    # --------------------------------------------------------------------------
    
    def _delete_map_tasks(self):
        """
        Deletes all Map Tasks which reference this Job as their owner.
        """
        db.delete(self.map_tasks)
        
    def _delete_reduce_tasks(self):
        """
        Deletes all Reduce Tasks which reference this Job as their owner.
        """
        db.delete(self.reduce_tasks)
        
    def _next_map_task(self):
        return self._next_task(self.map_tasks)

    def _next_reduce_task(self):
        #
        # TODO: WTF do I need this here?
        #
        from app.models.reduce_task import ReduceTask
        return self._next_task(self.reduce_tasks)
        
    def _next_task(self, tasks):
        """
        Iterate twice through the given tasks for this Job.  During the first
        iteration, it will return any job which is unclaimed.  During the second
        iteration, it will return any job which is not complete.
        """
        for task in tasks:
            if not task.claimed:
                return task
        
        for task in taks:
            if not task.complete:
                return task
        
        return None
        