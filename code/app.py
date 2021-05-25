from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from user import UserRegister
from item import Items, Item


app = Flask(__name__)

app.secret_key = "yevhenii"

api = Api(app)

jwt = JWT(app, authenticate, identity) # new endpoint  /auth






# api.add_resource(Student, "/student/<string:name>")
api.add_resource(Items, "/items")
api.add_resource(Item, "/items/<string:name>")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    app.run(port="5000", debug=True)
