import os
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import auth

dashbp = Blueprint('dashboard', __name__, url_prefix="/dashboard")

@dashbp.route('/', methods=('GET', 'POST'))
def index():
    if g.user is not None: # A User is Logged In

        repository_folder = os.environ.get('HOME', "Not Found") + "/_gitrepositories_/"
        username = g.user['username']

        user_repo_dir = repository_folder + username + "/"

        repositories = []
        for file in os.listdir(user_repo_dir):
            if os.path.isdir(user_repo_dir + file):
                # Every every item in repository list
                # will be a dictionary
                repo_path = user_repo_dir + file + "/.git"
                
                desc = open(repo_path + '/description', "r").readlines()

                repo = {}
                repo['name'] = file
                repo['description'] = desc[2]

                repositories.append(repo)
             

        # User Gravatar Finding
        # import code for encoding urls and generating md5 hashes
        import urllib, hashlib
         
        # Set your variables here
        email = g.user['email'].encode('utf-8')
        size = 400
         
        # construct the url
        gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.parse.urlencode(({'s':str(size)}))

        return render_template('dashboard/index.html',
                               repositories=repositories,
                               avatar=gravatar_url)

    # If g.user is None, means no user is logged in
    return auth.login()


@dashbp.route("/<path:repository>", methods=('GET',))
def show_repo(repository=None):
    repository_folder = os.environ.get('HOME', "Not Found") + "/_gitrepositories_/"
    username = g.user['username']

    path = repository_folder + username + "/" + repository.split('/')[0]

    try:
        stream = os.popen('tree -L 3 ' + path)
        tree = stream.read()
    except:
        tree = "No directory structure found. </br>The tree command didn't run properly."
    tree.replace('\n', '</br>')

    return render_template("dashboard/repository.html", path=path, tree=tree)