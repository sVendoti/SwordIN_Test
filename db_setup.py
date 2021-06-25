from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
import os

# Base directory path for DB creation
basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize the objects
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')

db = SQLAlchemy(app)
ma = Marshmallow(app)



@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('db_seed')
def db_seed():
    test_user = User(name='admin',
                     telephone_number='+1 999-999-9999',
                     email='admin@swordin.com',
                     password='P@ssw0rd')

    test_user2 = User(name='coadmin',
                     telephone_number='+1 888-999-9999',
                     email='coadmin@swordin.com',
                     password='P@ssw0rd123')


    db.session.add(test_user)
    db.session.add(test_user2)
    db.session.commit()
    print('Database seeded!')


# database models
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    telephone_number = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'telephone_number', 'email', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

if __name__ == '__main__':
    app.run()