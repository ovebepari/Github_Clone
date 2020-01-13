For Flask: 

    $ export FLASK_APP=gitbucket
    $ export FLASK_ENV=development

    Then for flask db and server: 

        $ flask init-db
        $ flask run

    Make Required Folders:
        
        $ mkdir ~/_gitrepositories_ 

Making a dumb git server: (on .git folder)    

    $ mv hooks/post-update.sample hooks/post-update
    $ chmod a+x hooks/post-update
    
    $ git update-server-info 
