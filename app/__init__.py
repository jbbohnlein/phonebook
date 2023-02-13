# This is the brains of our operation, so we need to have the big things imported like SQLAlchemy, Migrate


from flask import Flask
from config import Config
from .site.routes import site
from .authentication.routes import auth     # What this does is goes into the routes.py and pulls the auth = Blueprint up at the top
from .api.routes import api


from flask_sqlalchemy import SQLAlchemy   # At first, these can't be found because they haven't been stored in any folders. They exist but haven't been installed into app
from flask_migrate import Migrate
from models import db as root_db, login_manager, ma   # This has already been imported into models
from flask_cors import CORS    # this will help prevent cross-site request forgery
from helpers import JSONEncoder


app = Flask(__name__)    # This is the line that actually runs our app
CORS(app)



app.register_blueprint(site)    # This is how we registered our sites folder. 
app.register_blueprint(auth)    # At first this gives an error until we import it up top
app.register_blueprint(api)

app.json_encoder = JSONEncoder
app.config.from_object(Config)
root_db.init_app(app)   # This initiaties the app and makes the database
login_manager.init_app(app)  # this applies the things we've made into the app
ma.init_app(app)
migrate = Migrate(app, root_db)

