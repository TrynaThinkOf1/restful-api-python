#######################################
#       ZEVI BERLIN - 12/16/2024      #
#   LEARNING RESTful API TECHNOLOGY   #
#######################################

from flask import Flask
from flask_restful import Api, Resource

###########################
#      INITIALIZATION     #
app = Flask(__name__)     #
api = Api(app)            #
###########################



if __name__ == '__main__':
    app.run(debug=True) # ¡¡¡ DON'T RUN WITH DEBUG IN PRODUCTION ENVIRONMENT !!! #