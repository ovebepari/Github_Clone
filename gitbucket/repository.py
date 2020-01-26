import os
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, flash
)

from . import auth

repo_bp = Blueprint('repository', __name__, url_prefix="/repository")

@repo_bp.route('/new', methods=('GET', 'POST'))
def index():
    if g.user is not None: # A User is Logged In
        if request.method == "POST":
            new_repo = request.form["reponame"]
            repo_desc = request.form["description"]

            repository_folder = os.environ.get('HOME', "Not Found") + "/_gitrepositories_/"
            username = g.user['username']

            msg = None
            try:
                new_path = repository_folder + username + '/' + new_repo

                if os.path.exists(new_path):
                    msg = "This repository already exists!"

                else:
                    os.system("mkdir " + new_path)
                    os.system("mkdir " + new_path + '/' + ".git")
                    os.system("touch " + new_path + '/' + ".git/description")

                    descpath = new_path + '/' + ".git/description"
                    os.system("echo a > " + descpath)
                    os.system("echo b >> " + descpath)
                    os.system("echo " + repo_desc + " >> " + descpath)


            except:
                pass

            if msg is None:
                msg = "Successfully Created!"

            flash(msg)

            return redirect(url_for("dashboard.index"))

    # If g.user is None, means no user is logged in
    else:
        return auth.login()


    return render_template("repositories/new.html")



@repo_bp.route('/delete', methods=('GET', 'POST'))
def delete():
    if g.user is not None:
        # Means a user is logged in
        reponame = request.args["reponame"]

        repository_folder = os.environ.get('HOME', "Not Found") + "/_gitrepositories_/"
        username = g.user['username']
        repopath = repository_folder + username + '/' + reponame

        msg = None
        try:
            os.system("rm -dr " + repopath)
            msg = "Successfully Deleted!"
        except:
            pass

        if msg is None:
            msg = "Could not Delete, Something is wrong!"

        flash(msg)
        return redirect(url_for("dashboard.index"))
       

    else:
        return auth.login()