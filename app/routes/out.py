from flask import Flask, url_for, render_template,request,redirect, session
from flask_mysqldb import MySQL

app= Flask(__name__)
mysql= MySQL(app)

def out():
     if request.method == 'POST':
        if session:
            session.clear()
            return redirect(url_for('principal'))