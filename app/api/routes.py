# Application Programming Interface - it's a way for 2 or more computers to communicate

# The api portion of our Flask app is the location and rules of the server. 
# So far we've created a couple pages and the authentication information, but our database has no content for users to view.
# This portion of our Flask explicitly handles back-end data.

# didn't need to make a folder in api, because it's not returning any HTML, which is what the template folders do

from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Contact, contact_schema, contacts_schema

api = Blueprint('api', __name__, url_prefix='/api')   # in the other routes files we included a template folder, but api doesn't have a template folder
                                    # ^ This keeps all api calls categorized in the url, like putting them in a folder
                                    # It also means that before we write an api route, we need to have /api before that slug

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}  # looks like a dictionary but we didn't call it a dictionary. Returns JSON

@api.route('/contacts', methods = ['POST'])    # POST means we can actually send data to the api
@token_required                             # requires the user to have a token
def create_contact(current_user_token):
    name = request.json['name']     # json works in key-value pairs, so we're setting the value of 'name' = name
    email = request.json['email']
    phone_number = request.json['phone_number']
    address = request.json['address']
    user_token = current_user_token.token  

    print(f'BIG TESTER: {current_user_token.token}')

    contact = Contact(name, email, phone_number, address, user_token = user_token )  # Contact() comes from models.py. Looks similar but the ID will get written for us
                                                            # ^ This overwrites the default from the Contact() class 
    db.session.add(contact)    # adding / staging it to the database
    db.session.commit()         # committing it to the database

    response = contact_schema.dump(contact)    # contact_schema is also from models.py which instantiates a class (we didn't write this but brought it in from marshmallow)
    return jsonify(response)

@api.route('/contacts', methods = ['GET'])   # This time the method will be 'GET'
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    contacts = Contact.query.filter_by(user_token = a_user).all()  # This brings back all the contacts in our database
    response = contacts_schema.dump(contacts)
    return jsonify(response)


@api.route('/contacts/<id>', methods = ['GET'])   # This <id> is a variable that we'll be able to call and pull down into the rest of the function
@token_required
def get_single_contact(current_user_token, id):
    contact = Contact.query.get(id)
    response = contact_schema.dump(contact)
    return jsonify(response)


# Update endpoint
@api.route('/contacts/<id>', methods = ['POST', 'PUT'])
@token_required
def update_contact(current_user_token, id):
    contact = Contact.query.get(id)
    contact.name = request.json['name']
    contact.email = request.json['email']
    contact.address = request.json['address']
    contact.phone_number = request.json['phone_number']
    contact.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

# Remove endpoint (endpoint = contact?)
@api.route('/contacts/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)