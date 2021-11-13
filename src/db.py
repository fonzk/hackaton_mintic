import sqlite3

URL_DB = 'DB.db'

def consult_select(query)->list:
    try:
        with sqlite3.connect(URL_DB) as conection:
            cursor = conection.cursor()
            respuesta = cursor.execute(query).fetchall()
    except Exception as ex:
        respuesta = []
    return respuesta

def consult_action(query,datos)->int:
    try:
        with sqlite3.connect(URL_DB) as conection:
            cursor = conection.cursor()
            respuesta = cursor.execute(query,datos).rowcount
            if respuesta!=0:
                conection.commit()
    except Exception as ex:
        respuesta = 1000
    return respuesta