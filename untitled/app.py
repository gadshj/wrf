from flask import Flask
from config import Config
from rescourse.user import user_bp
from util.middlewares import jwt_authentication

app = Flask(__name__)

app.register_blueprint(user_bp)

app.config.from_object(Config)

app.before_request(jwt_authentication)


@app.route('/')
def index():
    return 'ok'


if __name__ == '__main__':
    app.run()
