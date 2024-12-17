#######################################
#       ZEVI BERLIN - 12/17/2024      #
#                                     #
#   LEARNING RESTful API TECHNOLOGY   #
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
#    HELPER FUNCTIONS
def getNextUserID():
    max_id = db.session.query(db.func.max(User.user_id)).scalar()
    return (max_id + 1) if max_id is not None else 0

###########################
#         DATABASE
class User(db.Model):
    user_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    passkey = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"User: {self.user_id}"

user_post_args = reqparse.RequestParser() # initial args for creating a user
user_post_args.add_argument('email', type=str, required=True)
user_post_args.add_argument('passkey', type=str, required=True) # add passkey arg

user_put_args = reqparse.RequestParser() # new args for updating a user
user_put_args.add_argument('email', type=str)
user_put_args.add_argument('passkey', type=str)

field_flavors = {
    "user_id": fields.Integer, # verify that an user_id is a string
    "email": fields.String,
}

###########################
#   RESOURCES & REQUESTS
class UserResource(Resource):
    @marshal_with(field_flavors)
    def get(self, user_id): # overrides the default get request because the class extends Resource
        result = User.query.filter_by(user_id=user_id).first()
        if not result:
            abort(404, message="User not found")

        return result

    @marshal_with(field_flavors)
    def put(self, user_id):
        args = user_put_args.parse_args()
        result = User.query.filter_by(user_id=user_id).first()
        if not result:
            abort(404, message="User not found")

        if args["email"] and args["email"] != result.email:
            if User.query.filter_by(email=args["email"]).first():
                abort(409, message="Email is already in use")
            result.email = args["email"]

        if args["passkey"] and args["passkey"] != result.passkey:
            result.passkey = args["passkey"]

        db.session.commit()
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
        return user, 201

    def delete(self, user_id):
        args = user_post_args.parse_args()
        result = User.query.filter_by(user_id=user_id).first()
        if not result:
            abort(404, message="User not found")

        else:
            if result.passkey != args["passkey"]:
                abort(404, message="Passkey doesn't match")

        db.session.delete(result)
        db.session.commit()

        return {"message": f"User: {user_id} deleted"}, 204

class UserByEmail(Resource):
    @marshal_with(field_flavors)
    def get(self, email):
        result = User.query.filter_by(email=email).first()
        if not result:
            abort(404, message="User not found")

        return result

api.add_resource(UserResource, "/user/create") # this adds a route to the API to create a user
api.add_resource(UserByEmail, "/user/email/<string:email>") # this adds a route to the API to fetch user data with email !& user_id

if __name__ == '__main__':
    #with app.app_context():
        #db.create_all()  # Uncomment only if re-initializing the database
    app.run(host="0.0.0.0", debug=True) # ¡¡¡ DON'T RUN WITH DEBUG IN PRODUCTION ENVIRONMENT !!! #