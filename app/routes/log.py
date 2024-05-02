from flask import Flask, url_for, render_template,request,redirect, session
from flask_mysqldb import MySQL

app= Flask(__name__)
mysql= MySQL(app)

def log():
    if request.method == 'POST':
        tipo_documento= request.form['tipo_documento']
        numero_documento= request.form['numero_documento']
        contraseña= request.form['contraseña']
        cursor= mysql.connection.cursor()
        cursor.execute('SELECT * FROM railway.estudiantes WHERE tipo_documento = %s AND numero_documento = %s AND contrasena_estudiante = %s', (tipo_documento, numero_documento, contraseña))
        result=cursor.fetchall()
        if result:
                    session['id_estudiante'] = result[0][0]
                    session['nombre_estudiante'] = result[0][1]
                    session['email_estudiante'] = result[0][2]
                    session['tipo_documento'] = result[0][3]
                    session['numero_documento'] = result[0][4]
                    session['grado_estudiante'] = result[0][5]
                    session['grupo_estudiante'] = result[0][6]
                    session['contraseña_estudiante'] = result[0][7]
                    
                    return redirect(url_for('interfaz'))
        else:
             return 'Usuario no encontrado'
        
