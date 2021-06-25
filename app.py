
# Import Libraries
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import os


# Get base directory path or the path you need to save the database file
basedir = os.path.abspath(os.path.dirname(__file__))

# Initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['JWT_SECRET_KEY'] = 'super-secret'


# Initialize class objects
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


# Default Function just to test the connection
@app.route('/')
def test_connection():
    return 'Hello you are able to ping the server!', 201


# Log in Method
@app.route('/login', methods=['POST'])
def login():

    # Check if request is json or a form and get email and password
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    # Check if user already exists in database
    test = User.query.filter_by(email=email, password=password).first()
    # If user exist return the bear token else send 401 message
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login succeeded!", access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401


# Function to get list of users along with details from the database
@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():

    # Query the USer table and serialize using the schema and return json obj
    user_list = User.query.all()
    result = users_schema.dump(user_list)
    return jsonify(result)


# Function to add new user
@app.route('/register', methods=['POST'])
def register_user():

    # Get email and check if email already exists in database
    email = request.json['email']

    # Query user table and get the first record
    test = User.query.filter_by(email=email).first()

    # if User exist return conflict error code and a message
    if test:
        return jsonify(message='That email already exists.'), 409
    else:

        # Read all the inputs from json
        name = request.json['name']
        password = request.json['password']
        telephone_number = request.json['telephone_number']

        # Create an object with all the users
        user = User(name=name, telephone_number=telephone_number, email=email, password=password)

        # Add user to the table and commit
        db.session.add(user)
        db.session.commit()

        # return success message
        return jsonify(message="User created successfully."), 201


# Function to update the user
@app.route('/update_user', methods=['PUT'])
@jwt_required()
def modify_user():

    # Get email ID and check if the mail exits in the table
    email = request.json['email']
    user = User.query.filter_by(email=email).first()

    # if the email exists update that record with inputs from JSON file
    if user:
        user.email = request.json['email']
        user.name = request.json['name']
        user.telephone_number = request.json['telephone_number']
        user.password = request.json['password']

        # Commit the changes
        db.session.commit()
        return jsonify(message="User Details updated"), 202
    else:
        return jsonify(message="User Does not Exists"), 404


# Database models
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    telephone_number = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


# User schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'telephone_number', 'email', 'password')


# Create claa for one user and Multi users
user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Run the application
if __name__ == '__main__':
    app.run()


