from application_controller import ApplicationController

from app.models.task import Task
from app.models.map_task import MapTask
from app.models.reduce_task import ReduceTask

class TasksController(ApplicationController):
    
    def flush(self):
        task = Task.task(self.request.get('id'))
        task.update(self.request.POST)
        task.complete = True
        task.save()
        
        self.render_text('OK')