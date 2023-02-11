# didn't need to make a folder in api

from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, ContactSchema, contacts_schema

api = Blueprint('api', __name__, url_prefix='/api')   # in the other routes files we included a template folder, but api doesn't have a template folder
                                    # ^ This keeps all api calls categorized in the url, like putting them in a folder
                                    # It also means that before we write an api route, we need to have /api before that slug