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