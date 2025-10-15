from flask_restx import Namespace, Resource
from flask import request
from App.config.config import db
from App.resources.auth import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest, Conflict
from flask_jwt_extended import create_access_token
from http import HTTPStatus


from flask_restx import Namespace,fields

auth_ns = Namespace('auth', description='Authentication')

register_input_model = auth_ns.model('RegisterInput', {
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})

register_output_model = auth_ns.model('RegisterOutput', {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
})


login_model = auth_ns.model('Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_input_model)
    @auth_ns.marshal_with(register_output_model, code=HTTPStatus.CREATED)
    @auth_ns.response(HTTPStatus.CONFLICT, 'User already exists')
    @auth_ns.response(HTTPStatus.BAD_REQUEST, 'Invalid data')
    def post(self):
        """Register a new user"""
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            raise BadRequest("All fields are required.")

        try:
            old_user = User.query.filter_by(email=email).first()
            if old_user:
                raise Conflict(f"User with email '{email}' already exists.")

            new_user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
            )
            db.session.add(new_user)
            db.session.commit()

            return new_user, HTTPStatus.CREATED

        except Conflict as e:
            return {"message": str(e)}, HTTPStatus.CONFLICT
        except BadRequest as e:
            return {"message": str(e)}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            db.session.rollback()
            return {"message": "Internal server error", "detail": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(HTTPStatus.OK, 'Login successful')
    @auth_ns.response(HTTPStatus.UNAUTHORIZED, 'Invalid credentials')
    def post(self):
        """User login with JWT generation"""
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"message": "Username and password required."}, HTTPStatus.BAD_REQUEST

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.username)
            return {
                "message": "Login successful",
                "access_token": access_token
            }, HTTPStatus.OK

        return {"message": "Invalid credentials"}, HTTPStatus.UNAUTHORIZED
