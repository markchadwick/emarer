from gaeo.controller import BaseController

from model.job import Job
from forms.job_form import JobForm

from urlparse import urlparse
from urllib import unquote_plus

import logging

class JobController(BaseController):
    def index(self):
        """
        List all jobs

        GET /jobs
        url_for('jobs')
        """
        self.jobs = Job.all()

    def create(self):
        """
        POST /jobs
        url_for('jobs')
        """
        job_form = JobForm(data=self.request.POST)

        if job_form.is_valid():
            job = job_form.save()
#            job.create_map_tasks()
#            job.create_reduce_tasks()

            self.redirect_to(url_for('jobs'))

        else:
            self.view['job_form'] = job_form
            self.render_view('jobs/new.html')

    def compute(self):
        job = Job.job(self.request.get('id'))
        
        self.view['job'] = job
        self.render_view('jobs/compute.html')
        

    def new(self):
        """
        GET /jobs/new
        url_for('new_job')
        """
        job_form = JobForm()
        
        self.view['job_form'] = JobForm()
        self.render_view('jobs/new.html')

    def update(self):
        """
        PUT /jobs/1
        url_for('job', id=1)
        
        TODO: Figure out why the framework doesn't take care of parsing this
              kinda shit for me.  It's a PUT statement.  What's the big deal?
        """
        job  = Job.job(self.request.get('id'))
        url  = urlparse(self.request.body)
        

        data = [part.split('=') for part in url[2].split('&')]
        data = dict([(k, unquote_plus(v)) for (k,v) in data if v != 'None'])
        logging.info("DATA: %s" % str(data))
        job_form = JobForm(instance=job, data=data)

        if job_form.is_valid():
            job = job_form.save()
#            job.create_map_tasks()
#            job.create_reduce_tasks()
            
            self.redirect_to(url_for('jobs', job.key))

        else:
            self.view['job_form'] = job_form
            self.render_view('jobs/edit.html')

    def delete(self):
        """
        DELETE /jobs/1
        url_for('job', id=1)
        """
        job = Job.job(self.request.get('id'))
        job.delete()
        
        self.redirect_to(url_for('jobs'))

    def show(self):
        """
        GET /jobs/1
        url_for('jobs', id=1)
        """
        job = Job.job(job_id=self.request.get('id'))
                
        self.view['job'] = job
        self.render_view('jobs/show.html')

    def edit(self):
        """
        GET /jobs/1;edit
        url_for('edit_job', id=1)
        """
        job = Job.job(job_id=self.request.get('id'))
        job_form = JobForm(instance=job)

        self.view['job_form'] = job_form
        self.view['job'] = job
        self.render_view('jobs/edit.html')


    def resource(self):
        job = Job.job(job_id=self.request.get('id'))
        self.redirect_to(job.resource_url)