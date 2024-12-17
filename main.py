#######################################
#       ZEVI BERLIN - 12/17/2024      #
#                                     #
#   LEARNING RESTful API TECHNOLOGY   #
#######################################

from flask import Flask, jsonify
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
    email = db.Column(db.String, unique=True, nullable=False, primary_key=True)
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
}

###########################
#   RESOURCES & REQUESTS
class UserResource(Resource):
    @marshal_with(field_flavors)
    def get(self, email): # overrides the default get request because the class extends Resource
        result = User.query.filter_by(email=email).first()
        if not result:
            abort(404, message="Could not find user with that email")
        return jsonify(result)

    @marshal_with(field_flavors)
    def put(self, email):
        args = user_put_args.parse_args()
        result = User.query.filter_by(email=email).first()
        if not result:
            abort(404, message="User doesn't exist, cannot update")

        if args["email"] != User.query.filter_by(email=email).first():
            db.session.delete(result)
            new_user = User(email=args["email"], passkey=args["passkey"])
            db.session.add(new_user)

        if args["passkey"] != User.query.filter_by(email=email).first().passkey:
            result.passkey = args["passkey"]

        db.session.commit()

        return jsonify(result)

    @marshal_with(field_flavors)
    def post(self, email):
        args = user_post_args.parse_args()
        result = User.query.filter_by(email=email).first()
        if result:
            abort(409, message="Email taken...")

        user = User(email=email, passkey=args["passkey"])
        db.session.add(user)
        db.session.commit()
        return user, 201

    def delete(self, email):
        result = User.query.filter_by(email=email).first()
        if not result:
            abort(404, message="Could not find user with that email")

        db.session.delete(result)
        db.session.commit()

        return {"User Deleted": email}, 204

api.add_resource(UserResource, "/user/<email>") # this adds the route to the API to create a food object

if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True) # ¡¡¡ DON'T RUN WITH DEBUG IN PRODUCTION ENVIRONMENT !!! #