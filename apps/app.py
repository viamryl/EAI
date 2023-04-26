from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import datetime
from getData import *

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'marketplace'
mysql = MySQL(app)


@app.route('/')
def main():
    return "Hello, World!"


@app.route('/customer', methods=['GET'])
def customer():
    cursor = mysql.connection.cursor()
    
    if 'id' in request.args:
        cursor.execute('SELECT * FROM customer where id_cust = %s', request.args['id'])

    elif 'name' in request.args:        
        cursor.execute('SELECT * FROM customer WHERE name LIKE \'%{}%\''.format(request.args['name']))

    else: 
        cursor.execute("SELECT * FROM customer")

    
    return getData(cursor)


@app.route('/item',methods=["GET"])
def item():
    cursor = mysql.connection.cursor()
    
    if 'id' in request.args:
        cursor.execute('SELECT * FROM item WHERE id_item = %s', request.args['id'])
    
    elif 'name' in request.args:
        cursor.execute('SELECT * FROM item WHERE item_name LIKE \'%{}%\'' .format(request.args['name']))

    else: 
        cursor.execute("SELECT * FROM item")

    return getData(cursor)


@app.route('/orders', methods=['GET'])
def orders():
    cursor = mysql.connection.cursor()
    if 'id' in request.args:
        cursor.execute("SELECT orders.id_order, customer.name, item.item_name, item.price, orders.qty, item.price*orders.qty as 'total_price' \
                        FROM customer \
                        JOIN orders ON orders.id_cust = customer.id_cust \
                        JOIN item ON orders.id_item = item.id_item\
                        WHERE id_order = {}" .format(request.args['id']))
    
    elif 'name' in request.args:
        cursor.execute("SELECT orders.id_order, customer.name, item.item_name, item.price, orders.qty, item.price*orders.qty as 'total_price' \
                        FROM customer \
                        JOIN orders ON orders.id_cust = customer.id_cust \
                        JOIN item ON orders.id_item = item.id_item\
                        WHERE customer.name LIKE \'%{}%\'" .format(request.args['name']))
    else:
        cursor.execute("SELECT orders.id_order, customer.name, item.item_name, item.price, orders.qty, item.price*orders.qty as 'total_price' \
                        FROM customer \
                        JOIN orders ON orders.id_cust = customer.id_cust \
                        JOIN item ON orders.id_item = item.id_item;")


    return getData(cursor)


@app.route('/editorder', methods=['POST'])
def editOrder():
    cursor = mysql.connection.cursor()

    try:
        cursor.execute('INSERT INTO orders(id_cust, id_item, qty) VALUES\
                        ({},{},{})'.format(request.json['id_cust'],request.json['id_item'],request.json['qty']))
        messege = "order added"
        statuscode = 200
    except:
        messege = "something wrong"
        statuscode = 500
    mysql.connection.commit()
    cursor.close()
    return returnMessege(messege, statuscode)

@app.route('/editcust',methods=['POST', 'PUT', 'DELETE'])
def editCust():
    cursor = mysql.connection.cursor()

    try:
        if request.method == 'POST':
            cursor.execute('INSERT INTO customer(name, phone, address) VALUES\
                        (\'{}\',\'{}\',\'{}\')'.format(request.json['name'], request.json['phone'], request.json['address']))
            messege = "custommer added"

        elif request.method == 'PUT':
            cursor.execute('UPDATE customer SET name = \'{}\', phone = \'{}\', address = \'{}\' WHERE id_cust = {}'\
                        .format(request.json['name'], request.json['phone'], request.json['address'], request.args['id']))
            messege = "customer updated"

        elif request.method == 'DELETE':
            cursor.execute('DELETE FROM customer WHERE id_cust = {}'.format(request.args['id']))

            messege = "customer deleted"
        statuscode = 200

    except:
        messege = "something wrong"
        statuscode = 500

    mysql.connection.commit()
    return returnMessege(messege, statuscode)

@app.route('/edititem', methods=['POST', 'PUT', 'DELETE'])
def editItem():
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        cursor.execute('INSERT INTO item(item_name, description, price) VALUES\
                       (\'{}\',\'{}\',{})'.format(request.json['item_name'], request.json['description'], request.json['price']))
        messege = "item added"

    elif request.method == 'PUT':
        cursor.execute('UPDATE item SET item_name = \'{}\', description = \'{}\', price = \'{}\' WHERE id_item = {}'\
                       .format(request.json['item_name'], request.json['description'], request.json['price'], request.args['id']))
        messege = "item updated"

    elif request.method == 'DELETE':
        cursor.execute('DELETE FROM item WHERE id_item = {}'.format(request.args['id']))
        messege = "item deleted"

    mysql.connection.commit()
    cursor.close()
    return returnMessege(messege)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 60, debug=True)


