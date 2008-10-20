def routing(m):
    # Routes from http://routes.groovie.org/
    # see the full documentaiton at http://routes.groovie.org/docs/
    # The priority is based upon order of creation: first created -> highest priority.

    # Connect the root of your app "http://yourapp.appspot.com/" to a controller/action
    # m.connect('home', '', controller='blog', action='index')
    # use in your application with url_for('home')

    # Named Routes
    # Routes can be named for easier use in your controllers/views
    # m.connect( 'history' , 'archives/by_eon/:century', controller='archives', action='show')
    # 
    # use with url_for('history', '1800') 
    # will route to ArchivesController.show() with self.params['century'] equal to '1800'

    # Typical route example.
    # m.connect('archives/:year/:month/:day', controller='archives', action='show')
    # 
    # routes urls like archives/2008/12/10 to
    # ArchivesController.show() with self.params['year'], self.params['month'], self.params['day'] available
    # 
    # use in your aplication views/controllers with url_for(controller='archives', year='2008', month='12', day='10')

    # Connect entire RESTful Resource routing with mapping
    # m.resource('message','messages') 
    # will be a shortcut for the following pattern of routes:
    # GET    /messages         -> MessagesController.index()          -> url_for('messages')
    # POST   /messages         -> MessagesController.create()         -> url_for('messages')
    # GET    /messages/new     -> MessagesController.new()            -> url_for('new_message')
    # PUT    /messages/1       -> MessagesController.update(id)       -> url_for('message', id=1)
    # DELETE /messages/1       -> MessagesController.delete(id)       -> url_for('message', id=1)
    # GET    /messages/1       -> MessagesController.show(id)         -> url_for('message', id=1)
    # GET    /messages/1;edit  -> MessagesController.edit(id)         -> url_for('edit_message', id=1)
    #
    # see http://routes.groovie.org/class-routes.base.Mapper.html#resource for all options
    m.resource('job', 'jobs')

    # Install the default routes as the lowest priority.  
    m.connect(':controller/:action/:id')

    # returns the mapper object. Do not remove.
    return m