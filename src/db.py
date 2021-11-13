import sqlite3
DB_URL = 'bd/DB.db'

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