from flask import Blueprint, request
from utils.responses import response_with
from utils import responses as resp
from models.users import User, UserSchema
from utils.db import db
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from utils.token import generate_verification_token, confirm_verification_token
from utils.email import send_email
from flask import url_for, render_template_string

user_routes = Blueprint("user_routes", __name__)

@user_routes.route('/', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if(User.find_by_email(data['email']) is not None or User.find_by_username(data['username']) is not None):       # already exist user
            return response_with(resp.INVALID_INPUT_422)
        data['password'] = User.generate_hash(data['password'])     # password to hash
        user_schmea = UserSchema()
        user  = user_schmea.load(data).data
        token = generate_verification_token(data['email'])          # generate token by email
        verification_email = url_for('user_routes.verify_email', token=token, _external=True)
        html = render_template_string("<p>Welcome! Thanks for signing up. Please follow this link to activate your account:</p> <p><a href='{{ verification_email }}'>{{ verification_email }}</a></p> <br> <p>Thanks!</p>", verification_email=verification_email)
        subject = "Please Verify your email"
        send_email(user.email, subject, html)

        result = user_schmea.dump(user.create())
        return response_with(resp.SUCCESS_201)
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)

@user_routes.route('/confirm/<token>', methods=['GET'])     
def verify_email(token):        # register username , then check the email 
    try:
        email = confirm_verification_token(token)
    except Exception as e:
        return response_with(resp.SERVER_ERROR_401)
    user = User.query.filter_by(email=email).first_or_404()
    if user.isVerified:
        return response_with(resp.INVALID_INPUT_422)
    else:
        user.isVerified = True
        db.session.add(user)
        db.session.commit()
        return response_with(resp.SUCCESS_200, value={'message': 'E-mail verified, you can proceed to login now.'})

@user_routes.route('/login', methods=['POST'])
def authenticate_user():
    try:
        data = request.get_json()
        if data.get('email') :        # find user is exist by emial    
            current_user = User.find_by_email(data['email']) 
        elif data.get('username') :  # find user is exist by username
            current_user = User.find_by_username(data['username'])
        if not current_user:         # not find register user ,return 404
            return response_with(resp.SERVER_ERROR_404)
        if current_user and not current_user.isVerified:
            return response_with(resp.BAD_REQUEST_400)    # find user , but not verrify
        if User.verify_hash(data['password'], current_user.password):      # check password is right
            access_token = create_access_token(identity = current_user.username)    # generate access token
            return response_with(resp.SUCCESS_200, value={'message': 'Logged in as admin', "access_token": access_token})
        else:
            return response_with(resp.UNAUTHORIZED_401)
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)
