from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid    # for unique ids in primary keys
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow # helps with moving data back and forth
import secrets 

# set variables for class insantiation

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader   # like writing a route where the user
# getting looked for will get loaded

def load_user(user_id):
   return User.query.get(user_id) 

class User(db.Model, UserMixin):       # This whole class is for users to create accounts and login and what data is associated with that account
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False)     # email can't be empty to sign up
    password = db.Column(db.String, nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True) # Want to be able to see/gatekeep who is accessing our stuff
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # when the user creates an account, we'll know what date it was

    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)   # going to send back a token hex for token which is 24 characters long

    def set_id(self):
        return str(uuid.uuid4())   # when we run this function it will generate a uuid for user and have a primary key that it's own entity

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash    # when they make their password, it'll take their password and hash it, and this pw_hash is the only way to unhash it

    def __repr__(self):
        return f'User {self.email} has been added to the database'

    

    # Need another class of our contacts of the info that we actually want to store. So, when a user wants to update their contacts, they can
class Contact(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(200))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    # all these db.s come from up above where i set variables for class instantiation and set db = SQLAlchemy. This is how data gets put into SQLAlchemy

    def __init__(self,name,email,phone_number,address,user_token,id=''):
        self.id = self.set_id()
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.user_token = user_token      # don't have to write a function for this because we're getting it from somewhere else

    def __repr__(self):
        return f'The following contact has been added to the phonebook: {self.name}'

    def set_id(self):
        return (secrets.token_urlsafe())

class ContactSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'email', 'phone_number', 'address']     # This deals with creating network and how the data interacts with one another??
        # deals with connecting the dots and how things relate to one another

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)

    
