import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import auth

dashbp = Blueprint('dashboard', __name__, url_prefix=None)

@dashbp.route('/', methods=('GET', 'POST'))
def index():
    if g.user is not None: # A User is Logged In
    	return render_template('dashboard/index.html')
    return auth.login()

