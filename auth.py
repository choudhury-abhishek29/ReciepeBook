from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST'])
def post_signup():
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return 'Content-Type not supported!'
    else:
        json = request.json
        if 'username' in json and 'password' in json and 'email' in json and 'name' in json and json['username'] != "" and json[
            'password'] != "" and json['email'] != "":
            username = json['username']
            password = json['password']
            email = json['email']
            name = json['name']

            user = User.query.filter_by(email=email).first()
            if user:
                return "User exists already", 409
            else:
                new_user = User(email=email, username=username, userhash=generate_password_hash(username, method='scrypt'), name=name,
                                password=generate_password_hash(password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
        else:
            return "Bad Request", 400

    return "signup success : " + username, 200

def isValidateRequest(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.userhash, username) and check_password_hash(user.password, password):
        return True
    else:
        return False
