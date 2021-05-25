import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table)


# user = (1, "bob", 'qwer')

insert_query = "INSERT INTO users VALUES (?, ?, ?)"

users = [
    (1, "bob", 'qwer'),
    (2, "ann", 'qwer'),
    (3, "jonh", 'qwer')
]

# cursor.execute(insert_query, user)
cursor.executemany(insert_query, users)

select_query = "SELECT * from users"

for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()
