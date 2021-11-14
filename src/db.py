import sqlite3

DB_URL = 'db/DB.db'
URL_DB = 'db/DB.db'

def accion(sql, data) -> int:
	""" (INSERT, DELETE, UPDATE) """
	try:
		with sqlite3.connect(DB_URL) as con:
			cur = con.cursor()
			sal = cur.execute(sql, data).rowcount
			if sal != 0:
				con.commit()
	except Exception as ex:
		print(f'ExceptionAccion: {ex}')
		sal = 0
	return sal

def seleccion(query) -> list:
	""" SELECT """
	try:
		with sqlite3.connect(DB_URL) as con:
			cur = con.cursor()
			sal = cur.execute(query).fetchall()
	except Exception as ex:
		print(f'ExceptionSeleccion: {ex}')
		sal = []
	return sal

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

