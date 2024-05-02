from flask import Flask, url_for, render_template,request,redirect, session
from flask_mysqldb import MySQL

app= Flask(__name__)
mysql= MySQL(app)

def register():
    if request.method == 'POST':
        nombre=request.form['name']
        email= request.form['email']
        tipo_documento= request.form['tipo_documento']
        numero_documento= request.form['numero_documento']
        grado= request.form['grado']
        contraseña= request.form['contraseña']
        repetir_contraseña= request.form['repetir_contraseña']

        if contraseña == repetir_contraseña:
            cursor= mysql.connection.cursor()
            cursor.execute('INSERT INTO railway.estudiantes (nombre_estudiante,email_estudiante,tipo_documento,numero_documento,grado_estudiante,contrasena_estudiante) VALUES (%s,%s,%s,%s,%s,%s)', (nombre,email,tipo_documento,numero_documento,grado,contraseña))
            mysql.connection.commit()
            cursor.execute('SELECT id_estudiante,nombre_estudiante,grado_estudiante,grupo_estudiante FROM railway.estudiantes WHERE numero_documento = %s', (numero_documento,))
            result= cursor.fetchall()
            if result:
                session['id_estudiante'] = result[0][0]
                session['nombre_completo'] = result[0][1]
                session['grado'] = result[0][2]
                session['grupo_estudiante'] = result[0][3]

            return redirect(url_for('grupo'))
        