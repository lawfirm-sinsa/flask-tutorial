import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from datetime import datetime
from bs4 import BeautifulSoup
from .auth import jwt_token_required
from pymongo import MongoClient
import jwt

client = MongoClient('localhost',27017)
db = client.dbLFD

SECRET_KEY = 'apple'

bp = Blueprint('index', __name__)

@bp.route('/')
def home():        
    return render_template('index/index.html')

@bp.route('/lawyer')
def lawyer():
    return render_template('index/lawyer.html')

@bp.route('/userinfo')
def userinfo():
    return render_template('index/userinfo.html')

@bp.route('/protected_service')
@jwt_token_required
def protected_service(**kwargs):
    return render_template('index/index_protected.html')

