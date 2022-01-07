import xml.etree.ElementTree as ET

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

file = ET.parse('secrets.xml')

database = file.find('db').text
user = file.find('user').text
password = file.find('password').text

database_uri = 'mysql+pymysql://' + user + ':' + password + '@' + database

print(database_uri)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

