import os
import sys
from flask import Flask 
from .extensions import db
from .routes import main
from .auth import flow, GOOGLE_CLIENT_ID
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    # postgres://chat4pp_user:qC8By8lXhwBVtKltbL7JRBuWIWxGnohF@dpg-ck3ntm6ru70s73c2d180-a.oregon-postgres.render.com/chat4pp

    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)



    app.register_blueprint(main)

    return app