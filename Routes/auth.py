from flask import Blueprint, request, jsonify
from models import User
from db import db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

bcrypt = Bcrypt()
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    try:
        new_user = User(name=data['name'], username=data['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message="User created successfully"), 201

    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity=user.id, expires_delta=False)
        return jsonify(token=token), 200

    return jsonify(message="Invalid credentials"), 401
