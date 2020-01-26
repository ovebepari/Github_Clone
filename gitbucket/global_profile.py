import os
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import auth, dashboard
from .db import get_db

global_profileBP = Blueprint('global_profile', __name__, url_prefix="/")


@global_profileBP.route('/@<username>/', methods=('GET', 'POST'))
def profile(username):
    
    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        error = 'Incorrect username.'
        flash(error)
        return redirect(url_for("dashboard.index"))

    else:
        g.global_user = get_db().execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()


        repository_folder = os.environ.get('HOME', "Not Found") + "/_gitrepositories_/"
        username = g.global_user['username']

        user_repo_dir = repository_folder + username + "/"

        repositories = []
        for file in os.listdir(user_repo_dir):
            if os.path.isdir(user_repo_dir + file):
                # Every every item in repository list
                # will be a dictionary
                repo_path = user_repo_dir + file + "/.git"
                
                repo = {}
                
                desc = "No Description"
                if os.path.exists(repo_path + '/description'):
                    desc = open(repo_path + '/description', "r").readlines()
                    if len(desc) >= 3:
                        repo['description'] = desc[2]

                
                repo['name'] = file
                

                repositories.append(repo)
             

        # User Gravatar Finding
        # import code for encoding urls and generating md5 hashes
        import urllib, hashlib
         
        # Set your variables here
        email = g.global_user['email'].encode('utf-8')
        size = 400
         
        # construct the url
        gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.parse.urlencode(({'s':str(size)}))

        return render_template('global_profile/index.html',
                               repositories=repositories,
                               avatar=gravatar_url)

    
@global_profileBP.route('/@<username>/<reponame>/', methods=('GET', 'POST'))
def repo(username, reponame):

    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        error = 'Incorrect username.'
        flash(error)
        return redirect(url_for("dashboard.index"))

    else:  
        g.global_user = get_db().execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

   
        repository_folder = os.environ.get('HOME', "Not Found") + "/_gitrepositories_/"

        path = repository_folder + username + "/" + reponame

        try:
            stream = os.popen('tree -L 3 ' + path)
            tree = stream.read()
        except:
            tree = "No directory structure found. </br>The tree command didn't run properly."
        tree.replace('\n', '</br>')

        return render_template("global_profile/repository.html", tree=tree, reponame=reponame)