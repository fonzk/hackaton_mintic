from flask import Flask, render_template, request, jsonify, redirect, session, url_for
from flask.helpers import flash, url_for
from werkzeug.utils import secure_filename
from werkzeug.wrappers import response
from wtforms.i18n import messages_path
from formularios import FormPart, Login
from markupsafe import escape
from db import consult_action, consult_select
from werkzeug.security import check_password_hash, generate_password_hash
import os



# from flask import Flask, render_template
# import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def hello_world():
    return render_template("construccion.html")


@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/login")
def loginForm():
    frm = Login()
    return render_template("login.html",form=frm)

@app.route('/validarLogin',methods=["GET","POST"])
def validarLogin():
    #recuperacion de datos
    if request.method == "POST" :
        user = escape(request.form['username'].strip()).lower()
        pwd = escape(request.form['password'].strip())
        print(user,pwd)
        #preparamos para consultar si el usuario existe
        sql = f"SELECT * FROM Person WHERE username = '{user}'"
        #realizamos la consulta
        res = consult_select(sql)
        print(res)
        #si el usuario existe traemos los datos para crear la sesion
        if len(res)!=0:
            sql2 = f"SELECT contra, id, Nombres, Apellidos, username, rol, sexo ,activo FROM Person WHERE username = '{user}'"
            res2 = consult_select(sql2)
            passw = res2[0][0]
            activo = res2[0][4]
            confirmPassword = check_password_hash(passw,pwd)
            if confirmPassword == True and activo == 'si':
                #si el usuario y la password son correctos creamos la session y lo enviamos al dashboard
                session['name'] = res2[0][1]
                session['userName'] = res2[0][4]
                session['rol'] = res2[0][5]
                sql = "SELECT * FROM Producto"
                res = consult_select(sql)
                if len(res)!= 0:
                    return render_template('contents/home.html',datos=res)
                else :
                    messageRes = "No existen productos registrados"
                    return render_template('admin.html',messageRes=messageRes)
            else :
                #si el usuario no existe lo redirigimos al login
                flash('Usuario o Contraseña incorrectos')
                return redirect('/login')
        else :
            #si el usuario no existe lo redirigimos al login
            flash('Usuario o Contraseña incorrectos')
            return redirect('/login')
    else :
        if 'userName' and 'rol' in session :
            sql = "SELECT * FROM Producto"
            res = consult_select(sql)
            if len(res)!= 0:
                return render_template('contents/home.html',datos=res)
            else :
                messageRes = " No existen productos registrados"
                return render_template('admin.html',messageRes=messageRes)
        else :
            return redirect(url_for('/login'))

@app.route("/user")
def user():
    if 'userName' and 'rol' in session :
        sql =  "SELECT * FROM Person"
        res = consult_select(sql)
        if len(res)!=0 :
            frm = FormPart()
            return render_template('usuarios.html',form=frm, data=res)
    else :
        res = [()]
        frm = FormPart()
        return render_template('usuarios.html',form=frm, data=res)
        # return redirect(url_for('loginForm'))

@app.route('/form/crear',methods=["GET"])
def formUser():
    frm = FormPart()
    return render_template('formUser.html',form=frm)
    # if 'userName' and 'name' in session :
    #     frm = FormPart()
    #     return render_template('formUser.html',form=frm)
    # else :
    #     return redirect(url_for('index'))

@app.route('/usuarios/edit/<string:id>',methods=["GET"])
def userEdit(id):
    if 'userName' and 'name' in session :
        sql = f"SELECT * FROM Person id = '{id}'"
        res = consult_select(sql)
        frm = FormPart()
        return render_template('editUser.html',form=frm,datos=res)
    else :
        return redirect(url_for('index'))

def deleteUsuarios(id):
    if 'userName' and 'name' in session :
        sql =  f"SELECT Nombres, activo FROM Person WHERE id = {id}"
        res = consult_select(sql)
        name = res[0][0]
        if res[0][1] == 'si' :
            activo = 'no'
        else :
            activo = 'si'

        sql = f"UPDATE Person SET nombres =?, activo =? WHERE id = {id} "
        res = consult_action(sql,(name,activo))
        return redirect(url_for('user'))
    else :
        return redirect(url_for('loginForm'))


@app.route('/username/',methods=["POST"])
def username():
    username = request.form['username'].lower()
    sql = f"SELECT * FROM Persona WHERE username = '{username}'"
    res = consult_select(sql)
    if len(res)==0 :
        response = 'username free'
        return response;
    else :
        response = 'username busy'
        return response;

#ruta para salir del dashboard
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route("/admin")
def admin():
    return render_template("admin.html")
# Reinaldo test
@app.route("/api")
def api():
	return render_template("reinaldo.html")
# Reinaldo test

# if __name__ == '__main__':
# 	app.run()


if __name__ == '__main__':
    app.run(port=8080, debug=True)