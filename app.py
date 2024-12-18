#######################################
#       ZEVI BERLIN - 12/17/2024      #
#                                     #
#   LEARNING RESTful API TECHNOLOGY   #
#######################################

###########################
#    IMPORTED LIBRARIES
from flask import Flask, request
from flask_restful import Api, Resource, marshal_with, reqparse, fields, abort
from flask_sqlalchemy import SQLAlchemy
import secrets
import hashlib
###########################

###########################
#      INITIALIZATION
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///creds.db'
db = SQLAlchemy(app)
###########################

###########################
#    HELPER FUNCTIONS
def getNextUserID():
    max_id = db.session.query(db.func.max(User.user_id)).scalar()
    return (max_id + 1) if max_id is not None else 0

def generateKey():
    return secrets.token_hex(32)

def hashKey(key):
    return hashlib.sha256(key.encode()).hexdigest()

def verifyKey(key):
    hashed_key = hashKey(key)
    return Keys.query.filter_by(hashed_key=hashed_key).first() is not None
###########################

###########################
#        DATABASES
class User(db.Model):
    user_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    passkey = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"User: {self.user_id}"

class Keys(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    hashed_key = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return f"API Key: {self.hashed_key}"
###########################
#     ARGS & PARSERS
user_post_args = reqparse.RequestParser() # initial args for creating a user
user_post_args.add_argument('email', type=str, required=True)
user_post_args.add_argument('passkey', type=str, required=True) # add passkey arg

user_put_args = reqparse.RequestParser() # new args for updating a user
user_put_args.add_argument('new_email', type=str)
user_put_args.add_argument('passkey', type=str)

user_delete_args = reqparse.RequestParser()
user_delete_args.add_argument('passkey', type=str)
###########################

###########################
#       DECORATORS
field_flavors = {
    "user_id": fields.Integer,
    "email": fields.String,
    "passkey": fields.String
}
###########################

###########################
#        RESOURCES
class UserResource(Resource):
    @marshal_with(field_flavors)
    def get(self, email):
        result = User.query.filter_by(email=email).first()
        if not result:
            abort(404, message="User not found")

        print(result)
        return result

    @marshal_with(field_flavors)
    def put(self, email):
        args = user_put_args.parse_args()
        result = User.query.filter_by(email=email).first()
        if not result:
            abort(404, message="User not found")

        if args["new_email"] and args["email"] != result.email:
            if User.query.filter_by(email=args["email"]).first():
                abort(409, message="Email is already in use")
            result.email = args["email"]

        if args["passkey"] and args["passkey"] != result.passkey:
            result.passkey = args["passkey"]

        db.session.commit()
        print(result)
        return result

    @marshal_with(field_flavors)
    def post(self):
        args = user_post_args.parse_args()
        result = User.query.filter_by(email=args["email"]).first()
        if result:
            abort(409, message="User with that user_id already exists")

        user = User(user_id=getNextUserID(), email=args["email"], passkey=args["passkey"])
        db.session.add(user)
        db.session.commit()

        print(result)
        return user, 201

    def delete(self, email):
        args = user_delete_args.parse_args()
        result = User.query.filter_by(email=email).first()
        if not result:
            abort(404, message="User not found")
        if result.passkey != args["passkey"]:
            abort(404, message="Passkey doesn't match")

        db.session.delete(result)
        db.session.commit()
        print(result)
        return {"message": f"User: {result.user_id} deleted"}, 204

class UserByEmail(Resource):
    @marshal_with(field_flavors)
    def get(self, email):
        result = User.query.filter_by(email=email).first()
        if not result:
            abort(404, message="User not found")

        return result
###########################
#      DEFINE ROUTES
api.add_resource(UserResource, "/user/<string:email>")
###########################

###########################
if __name__ == '__main__':
    #with app.app_context():
        #db.create_all()  # Uncomment only if re-initializing the database
    app.run(host="0.0.0.0", port=6969, debug=True) # ¡¡¡ DON'T RUN WITH DEBUG IN PRODUCTION ENVIRONMENT !!! #