from google.appengine.ext.db import djangoforms

from app.models.job import Job

class JobForm(djangoforms.ModelForm):
    class Meta:
        model = Job
