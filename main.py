#######################################
#       ZEVI BERLIN - 12/16/2024      #
#   LEARNING RESTful API TECHNOLOGY   #
#        IGNORE WHIMSICAL NAMES       #
#######################################

from flask import Flask
from flask_restful import Api, Resource, marshal_with, reqparse, fields, abort
from flask_sqlalchemy import SQLAlchemy

###########################
#      INITIALIZATION
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///creds.db'
db = SQLAlchemy(app)
###########################
#         DATABASE
class User(db.Model):
    email = db.Column(db.String, unique=True, nullable=False)
    passkey = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"User: {self.email}, Passkey: {self.passkey}"

user_post_args = reqparse.RequestParser() # initial args for creating a user
user_post_args.add_argument('email', type=str, required=True) # add email arg
user_post_args.add_argument('passkey', type=str, required=True) # add passkey arg

user_put_args = reqparse.RequestParser() # new args for updating a user
user_put_args.add_argument('email', type=str, required=True)
user_put_args.add_argument('passkey', type=str, required=True)

field_flavors = {
    "email": fields.String, # verify that an email is a string
    "passkey": fields.String # verify that a passkey is a string
}

###########################
#   RESOURCES & REQUESTS
class Food(Resource):
    @marshal_with(field_flavors)
    def get(self, email, passkey): # overrides the default get request because the class extends Resource
        result = User.query.filter_by(email=email).first()
        if not result:
            abort(404, message="Could not find user with that email")
        return result

    def put(self, email, passkey):
        pass

api.add_resource(Food, "/add-user/<email>/<passkey>") # this adds the route to the API to create a food object

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True) # ¡¡¡ DON'T RUN WITH DEBUG IN PRODUCTION ENVIRONMENT !!! #