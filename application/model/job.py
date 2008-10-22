from google.appengine.ext import db
from gaeo.model import BaseModel

class Job(BaseModel):
    
    # --------------------------------------------------------------------------
    # Fields
    # --------------------------------------------------------------------------

    name    = db.StringProperty()

    mapper  = db.StringProperty(multiline=True)
    combiner= db.StringProperty(multiline=True)
    
    reducer = db.StringProperty(multiline=True)
    
    num_reducers = 15

    resource_url = db.StringProperty()
    num_mappers  = db.IntegerProperty()
    num_reducers = db.IntegerProperty()
    
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
        
        totally_incorrect_num_map_tasks = 1
        
        for i in range(totally_incorrect_num_map_tasks):
            MapTask(job=self, start_byte=0, end_byte=1000000).save()
        
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
        
        for i in range(self.num_reducers):
            ReduceTaks(job=self).save()
        
    def next_task(self):
        """
        Returns the next task that needs computation.  This could be either a
        MapTask, ReduceTask, or None depending on the current state of the Job.
        
        :rtype: Task
        :returns: Next task which needs to be executed to complete this job, or
                  `None` if no such job exists.
        """
        unimplemented
        
    # --------------------------------------------------------------------------
    # Private Methods
    # --------------------------------------------------------------------------
    
    def _delete_map_tasks(self):
        """
        Deletes all Map Tasks which reference this Job as their owner.
        """
        self.map_tasks.delete()
        
    def _delete_reduce_tasks(self):
        """
        Deletes all Reduce Tasks which reference this Job as their owner.
        """
        self.reduce_tasks.delete()
        