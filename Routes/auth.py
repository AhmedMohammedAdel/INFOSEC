from flask import Blueprint, request, jsonify, send_file
from models import User
from db import db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
import pyotp
import qrcode
from io import BytesIO

bcrypt = Bcrypt()
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    secret = pyotp.random_base32()

    new_user = User(
        name=data['name'], 
        username=data['username'], 
        password=data['password'],
    )
    new_user.twofa_secret = secret

    db.session.add(new_user)
    db.session.commit()

    return jsonify(
        message="User created successfully",
        twofa_secret=secret
    ), 201


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    otp_code = data['otp']

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        totp = pyotp.TOTP(user.twofa_secret)
        
        if totp.verify(otp_code, valid_window=1):
            access_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=10))
            return jsonify(access_token=access_token), 200
        else:
            return jsonify(message="Invalid 2FA code"), 401

@auth_blueprint.route('/qrcode/<username>', methods=['GET'])
def get_qrcode(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify(message="User not found"), 404

    totp = pyotp.TOTP(user.twofa_secret)
    uri = totp.provisioning_uri(name=user.username, issuer_name="MyApp")

    img = qrcode.make(uri)
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    return send_file(buffer, mimetype="image/png")