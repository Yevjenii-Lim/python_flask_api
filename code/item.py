
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


def check_items_db(name):
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    query = "SELECT * FROM items WHERE name=?"
    result = cursor.execute(query, (name,))
    row = result.fetchone()
    if row:
        return row

    return None

class Items(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # row = result.fetchone()
        result = []
        for item in cursor.execute(query):
            el = {"name": item[0], "price": item[1]}
            result.append(el)
        if len(result):
            return {"items": result}

        connection.close()
        return {"message": "no items in storage"}

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",type=float, required=True, help="Fill the field")
    parser.add_argument("name",type=str, required=True, help="Fill the field")

    # @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item

        return {"message": f"no such item as {name}"}
        # items = next(filter(lambda x: x["name"] == name, store["items"]), None)
        # for item in store["items"]:
        #     print(store["items"])
        #     if item["name"] == name:
        #         items.append(item)

        # if len(items) == 0:
        #     return {"items": None}, 404

        # return {"items": items }, 200 if items else 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}

        return None
    def post(self, name):
        request_data = Item.parser.parse_args()
        item = self.find_by_name(request_data["name"])
        if item:
            return {"message": f"Item with name {request_data['name']} is alredy exsists"}, 400
        # if next(filter(lambda x: x["name"] == request_data["name"], store["items"]), None):
            # return {"message": f"Item with name {name} is alredy exsists"}, 400
        # print(request_data)
        # new_item = {
        #     "name": request_data["name"],
        #     "price": request_data["price"]
        # }
        item = {"name": request_data["name"], "price": request_data["price"]}
        try:
            self.insert(item)
        except:
            return {"message": "error"}, 500 #internal server error


        return item, 201

    def delete(self,name):
        # items = list(filter(lambda x: x["name"] != name, store["items"]))
        item = self.find_by_name(name)
        if item:
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()
            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))
            connection.commit()
            connection.close()
            return item
            # return {"message": f"no {name} for deleting"}
        #
        # store["items"] = items
        return {"message": f"no {name} for deleting"}


    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(data["name"])
        updated_item = {"name": data["name"], "price": data["price"]}
        if item is None:
            try:
                self.insert(updated_item)
            except Exception as e:
                return {"messag": e.message}, 500
        else:
            try:
                self.update(updated_item)
            except Exception as e:
                return {"message": e.message}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES(?, ?)"

        cursor.execute(query, (item["name"], item["price"]))
        connection.commit()
        connection.close()
