from google.appengine.ext.db import djangoforms

from model.job import Job

class JobForm(djangoforms.ModelForm):
    class Meta:
        model = Job
