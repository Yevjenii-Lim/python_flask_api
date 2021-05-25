import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, name, password):
        self.id = _id
        self.name = name
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="give your username")
    parser.add_argument("password", type=str, required=True, help="give your password")

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data["username"]):
            return {"message":f"user with name {data['username']} is alredy exists"} , 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES(NULL, ?, ?)"
        cursor.execute(query, (data["username"], data["password"]))

        connection.commit()
        connection.close()

        return {"message": "user created suceseful"}, 201

    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        select_query = "SELECT * from users"
        result = []

        for row in cursor.execute(select_query):
            result.append(row)

        return {"all users": result}, 201
