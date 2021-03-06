# -*- coding: utf-8 -*-
from ..models import AnonymousUser, User
from flask import g, jsonify, make_response
from flask.ext.httpauth import HTTPBasicAuth
from . import api
from .errors import forbidden
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token, password):
    # email means email or username
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
    # verify token
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    # verify email or username
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        user = User.query.filter_by(username=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)

@api.route('/token')
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(expiration=3600),\
                   'expiration': 3600})

# 写的莫名其妙
@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')

# all routes will auto auth through this
@api.before_request
@auth.login_required
def before_request():
    if g.current_user.is_anonymous:
        return forbidden('Not authorated')

