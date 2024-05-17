import os
from flask import Flask, render_template
from flask_migrate import Migrate
from models.User import db
from routes.user_bp import user_bp

def create_app():
    app = Flask(__name__)

    app.config.from_object('config')

    db.init_app(app)

    migrate = Migrate(app, db)

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')
    
    app.register_blueprint(user_bp, url_prefix='/users')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
