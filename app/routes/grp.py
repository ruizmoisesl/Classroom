from flask import Flask, url_for, render_template,request,redirect, session
from flask_mysqldb import MySQL

app= Flask(__name__)
mysql= MySQL(app)

def grp():
        if request.method == 'POST':
            id= session.get('id_estudiante')
            grupo= request.form['grupo']
            cursor= mysql.connection.cursor()
            cursor.execute('UPDATE estudiantes SET grupo = %s WHERE id = %s',  (grupo, id, ))
            mysql.connection.commit()
            return redirect(url_for('interfaz'))