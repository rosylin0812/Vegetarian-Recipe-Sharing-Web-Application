from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from veggyblog.config import Config
from flask_migrate import Migrate

db = SQLAlchemy()

migrate = Migrate()

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail() 

# by moving app out from () and put them into create_app under __init__()
# the extension object doesn't initially get bound to the application  
# so one extension object can b used for multiple apps
def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    migrate.init_app(app,db)
    
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from veggyblog.users.routes import users # avoid circular import
    from veggyblog.posts.routes import posts
    from veggyblog.main.routes import main
    from veggyblog.errors.handlers import errors
    #from veggyblog.relation.routes import relation
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    #app.register_blueprint(relation)
    return app


