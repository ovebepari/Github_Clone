import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import auth

dashbp = Blueprint('dashboard', __name__, url_prefix="/dashboard")

@dashbp.route('/', methods=('GET', 'POST'))
def index():
    if g.user is not None: # A User is Logged In
    	import os

    	repository_folder = os.environ.get('HOME', "Not Found") + "/_gitrepositories_/"
    	username = g.user['username']

    	user_repo_dir = repository_folder + username + "/"

    	repositories = []
    	for file in os.listdir(user_repo_dir):
    		if os.path.isdir(user_repo_dir + file):
    			# Every every item in repository list
    			# will be a dictionary

    			repositories.append(file)

    	print(*repositories)	
    	return render_template('dashboard/index.html', repositories=repositories)

    return auth.login()


