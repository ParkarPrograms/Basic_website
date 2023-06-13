import sqlite3

db = sqlite3.connect("orders_data.db", check_same_thread=False)
cursor = db.cursor()

# cursor.execute("CREATE TABLE Cake_Orders (name varchar(70), number int, email varchar(250), address varchar(250), order_details varchar(250), specs varchar(500), type varchar(10), date varchar(15))")