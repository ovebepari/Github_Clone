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

                os.system("mkdir " + new_path)

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
        pass

    else:
        return auth.login()