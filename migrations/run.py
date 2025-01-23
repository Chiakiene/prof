from flask import Flask
from flask_migrate import Migrate, upgrade
from models import db, User

def run_migrations():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    migrate = Migrate(app, db)
    
    with app.app_context():
        upgrade()

if __name__ == '__main__':
    run_migrations() 