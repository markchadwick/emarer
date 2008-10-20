from application_controller import ApplicationController
from framework.routes.util import url_for
from app.models.job import Job
from app.forms.job_form import JobForm

import logging

class JobsController(ApplicationController):
    def index(self):
        """
        List all jobs

        GET /jobs
        url_for('jobs')
        """
        jobs = Job.all()

        self.view['jobs'] = jobs
        self.render_view('jobs/index.html')

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
        """
        job = Job.job(self.request.get('id'))
        
        job_form = JobForm(instance=job, data=self.request.POST)

        logging.info("Found Job %s" % str(id))
        logging.info("Post :%s - %s" % (str(self.request.__class__), str(self.request.arguments())))

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