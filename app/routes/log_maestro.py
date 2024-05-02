from flask import Flask, url_for, render_template,request,redirect, session
from flask_mysqldb import MySQL

app= Flask(__name__)
mysql= MySQL(app)

def log():
    if request.method == 'POST':
        email= request.form['email']
        contraseña= request.form['password']
        cursor= mysql.connection.cursor()
        cursor.execute('SELECT * FROM railway.maestros WHERE  email_maestro = %s AND contrasena_maestro = %s', ( email, contraseña))
        result=cursor.fetchall()
        if result:
                    
                    session['id_maestro'] = result[0][0]
                    session['nombre_maestro'] = result[0][1]
                    return redirect(url_for('interfaz_maestro'))
        else:
             return 'Usuario no encontrado'
        
