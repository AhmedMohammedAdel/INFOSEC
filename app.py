from flask import Flask
from db import db_init
from Routes.auth import auth_blueprint
from Routes.prd import product_blueprint
from config import Config
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)

db_init(app)
jwt = JWTManager(app)

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(product_blueprint, url_prefix='/products')

if __name__ == "__main__":
    app.run(debug=True)
