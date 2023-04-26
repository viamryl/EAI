from flask import jsonify
from datetime import *

def getData(cursor):
    column_name = [i[0] for i in cursor.description]

    data = []
    for i in cursor.fetchall():
        data.append(dict(zip(column_name, i)))

    try:
        if data[0]:
            statuscode = 200
            messege = 'operation success'

    except IndexError:
        statuscode = 204
        messege = 'data empty'

    msg = {
        "Status Code" : statuscode,
        "Messege" : messege,
        "timestamp" : datetime.now()
    }

    cursor.close()

    return jsonify(data,msg)

def returnMessege(messege,statuscode):
    msg = {
        "Status Code" : statuscode,
        "Messege" : messege,
        "timestamp" : datetime.now()
    }
    return jsonify(msg)
