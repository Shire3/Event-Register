from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from App.services.auth_service import auth_ns
from App.services.event_service import event_ns
from App.config.config import db, config_dict


def create_app (config= config_dict['Dev']):
    app = Flask(__name__)
    app.config.from_object(config)
    JWTManager(app)
    db.init_app(app)
    authorizations = {
        'Bearer Auth':{
            'type':'apiKey',
            'in':'header',
            'name':'Authorization',
            'description':'add jwt **Bearer <JWT>**'
        }
    }

    api = Api(app,
            title="Event Management API",
            version="1.0",
            description="To leep track of book available borrowed",
            authorizations=authorizations,
            security="Bearer Auth"
            )

    migrate = Migrate(app,db)

    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(event_ns, path='/events')

    return app
