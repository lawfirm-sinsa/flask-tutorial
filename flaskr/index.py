import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from datetime import datetime

bp = Blueprint('index', __name__)

@bp.route('/')
def home():
    return render_template('index/index.html')

@bp.route('/lawyer')
def lawyer():
    return render_template('index/lawyer.html')
