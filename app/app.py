from flask import Flask, url_for, render_template,request,redirect, session, send_from_directory
from flask_mysqldb import MySQL
import secrets
from routes import reg, log, grp, out
from werkzeug.utils import secure_filename 
import os
import datetime

app= Flask(__name__)

UPLOAD_FOLDER = os.path.join('app/static/', 'upload')
ALLOWED_EXTENSIONS= set(['pdf','pptx','docx','jpg','png','peg', 'mp4', 'mp3', 'wav' ])

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= '1234567'
app.config['MYSQL_DB']= 'classroom'
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER

mysql= MySQL(app)

def septimo():
    cursor= mysql.connection.cursor()
    cursor.execute('SELECT numero_grupo FROM grupos WHERE id_grado = %s', ('1'))
    septimo= cursor.fetchone()
    return septimo

def octavo():
    cursor= mysql.connection.cursor()
    cursor.execute('SELECT numero_grupo FROM grupos WHERE id_grado = %s', ('2'))
    octavo= cursor.fetchone()
    return octavo
def noveno():
    cursor= mysql.connection.cursor()
    cursor.execute('SELECT numero_grupo FROM grupos WHERE id_grado = %s', ('3'))
    noveno= cursor.fetchone()
    return noveno

@app.route('/')
def principal():
    return render_template('principal.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registro', methods= ['POST'])
def registro():
     return reg.register()
        
@app.route('/login')
def login():
    return render_template('interfaz_login.html')

@app.route('/logIn', methods= ['POST'])
def logIn():
    return log.log()

@app.route('/login_estudiante')
def login_estudiante():
    return render_template('login.html')

@app.route('/grupo')
def grupo():
    grado= session.get('grado')
    return render_template('grupo.html', grado= grado,septimo= septimo(),octavo=octavo(),noveno=noveno())

@app.route('/group', methods= ['POST'])
def group():
   return grp.grp()  

@app.route('/interfaz')
def interfaz():
    nombre= session.get('nombre_completo')
    grado= session.get('grado')
    grupo= session.get('grupo')
    cursor= mysql.connection.cursor()
    cursor.execute('SELECT * FROM trabajos WHERE grado_trabajo = %s',(grado,))
    trabajos = cursor.fetchall()
    return render_template('interfaz.html', nombre=nombre,grado=grado,grupo=grupo, trabajos=trabajos)

@app.route('/logout', methods= ['POST'])
def logout():
    return out.out()

@app.route('/maestro')
def interfaz_maestro():
    cursor= mysql.connection.cursor()
    cursor.execute('SELECT * FROM trabajos')
    trabajos= cursor.fetchall()
    return render_template('interfaz_maestro.html',trabajos=reversed(trabajos))

@app.route('/login_maestro')
def interfaz_loginMaestro():
    if request.method == 'POST':
        email= request.form['email']
        password= request.form['password']
        cursor= mysql.connection.cursor()


    return render_template('login_maestro.html')

@app.route('/registro_maestro')
def registro_maestro():
    return render_template('register_maestro.html')

#CRUD

def allowed_file(file):

    file= file.split('.')

    if file[1] in ALLOWED_EXTENSIONS:
        return True
    return False

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/upload', methods=['POST'])
def upload():
    nombre_actividad= request.form['nombre_actividad']
    descripcion= request.form['descripcion']
    grado= request.form['grado']
    file= request.files.getlist('archivos[]')

    for archivo in file:
        filename= secure_filename(archivo.filename)

    if archivo and allowed_file(filename):
        archivo.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        ruta = UPLOAD_FOLDER + filename
        cursor= mysql.connection.cursor()
        cursor.execute('INSERT INTO trabajos (nombre_actividad,descripcion,grado_trabajo, filename) VALUES (%s,%s,%s,%s)', (nombre_actividad, descripcion,grado,ruta,))
        mysql.connection.commit()
        print(ruta)
        return redirect(url_for('interfaz_maestro'))
    else:
        return 'archivo no Permitido'


@app.route('/delete/<string:id_trabajo>')
def delete(id_trabajo):
    cursor= mysql.connection.cursor()
    cursor.execute('DELETE FROM trabajos WHERE id_trabajo =%s',(id_trabajo))
    mysql.connection.commit()
    return redirect(url_for('interfaz_maestro'))



@app.route('/update/<string:id_trabajo>', methods= ['GET','POST'])
def update(id_trabajo):
    cursor= mysql.connection.cursor()
    cursor.execute('SELECT * FROM trabajos WHERE id_trabajo= %s', (id_trabajo))
    datos= cursor.fetchone()

    if request.method == 'POST':

        nombre_actividad= request.form['nombre_actividad']
        descripcion= request.form['descripcion']
        file= request.files.getlist('archivos[]')

        for archivo in file:
            filename= secure_filename(archivo.filename)

        if archivo and allowed_file(filename):
            archivo.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            cursor= mysql.connection.cursor()
            cursor.execute('UPDATE trabajos  SET nombre_actividad = %s, descripcion = %s, filename = %s WHERE id_trabajo = %s ', (nombre_actividad, descripcion, filename, id_trabajo,))
            mysql.connection.commit()

            return redirect(url_for('interfaz_maestro'))
    
    
    return render_template('update.html',datos=datos)




@app.route('/ver_actividad/<string:id>', methods= ['GET', 'POST'])
def  ver_actividad(id):
    cursor= mysql.connection.cursor()
    cursor.execute('SELECT * FROM trabajos WHERE id_trabajo = %s',(id))
    trabajos = cursor.fetchall()
    cursor.close()
    if trabajos:
        session['filename']= trabajos[0][4]

    
    nombre= session.get('nombre_completo')
    grado= session.get('grado')
    grupo= session.get('grupo')

         
    return render_template('ver_trabajo.html', trabajos= trabajos,nombre=nombre,grado=grado,grupo=grupo)



if __name__ == "__main__":
    app.run(debug=True)