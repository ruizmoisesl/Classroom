# region import
from flask import Flask, url_for, render_template,request,redirect, session
from flask_mysqldb  import MySQL
import secrets
from routes import reg, log, grp, out, log_maestro
from werkzeug.utils import secure_filename 
import os
from datetime import datetime

# region config 
app= Flask(__name__)

UPLOAD_FOLDER = os.path.join('app/static/', 'upload')
ALLOWED_EXTENSIONS= set(['pdf','pptx','docx','jpg','png','peg', 'mp4', 'mp3', 'wav' ])

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


fecha_actual= datetime.now()
formato= datetime.strftime(fecha_actual, '%d %h, %I:%M %p')


app.config['MYSQL_HOST']= 'roundhouse.proxy.rlwy.net'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PORT']= 53399
app.config['MYSQL_DATABASE']= 'railway'
app.config['MYSQL_PASSWORD']= 'aMvpscNhTMNBVNtQLWFdouEJIOEhsqLU'
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER

mysql= MySQL(app)

#region grupos

def septimo():
    cursor= mysql.connection.cursor()
    cursor.execute('SELECT nombre_grupo FROM railway.grupo WHERE id_grado = %s', ('1'))
    septimo= cursor.fetchone()
    return septimo

def octavo():
    cursor= mysql.connection.cursor()
    cursor.execute('SELECT nombre_grupo FROM railway.grupo WHERE id_grado = %s', ('2'))
    octavo= cursor.fetchone()
    return octavo
def noveno():
    cursor= mysql.connection.cursor()
    cursor.execute('SELECT nombre_grupo FROM railway.grupo WHERE id_grado = %s', ('3'))
    noveno= cursor.fetchone()
    return noveno

#region grados
def grados():
    cursor= mysql.connection.cursor()
    cursor.execute('SELECT nombre_grado FROM railway.grado')
    grados = cursor.fetchall()
    if grados:
        return grados

#region route principal

@app.route('/')
def principal():
    return render_template('principal.html', fecha_actual = formato)

#region register

@app.route('/register')
def register():
    return render_template('interfaz_register.html')

@app.route('/register_estudiante')
def register_estudiante():
    return render_template('register_estudiante.html', grupos= grados())

@app.route('/register_maestro')
def register_maestro():
    return render_template('register_maestro.html', grupos= grados())

@app.route('/registro', methods= ['POST'])
def registro():
     return reg.register()

#region login

@app.route('/login')
def login():
    return render_template('interfaz_login.html')

@app.route('/logIn', methods= ['POST'])
def logIn():
    return log.log()

@app.route('/login_estudiante')
def login_estudiante():
    return render_template('login.html')

#region seleccion de grupo

@app.route('/grupo')
def grupo():
    grado= session.get('grado')
    return render_template('grupo.html', grado= grado,septimo= septimo(),octavo=octavo(),noveno=noveno())

@app.route('/group', methods= ['POST'])
def group():
   return grp.grp()  

#region interfaz estudiante
@app.route('/interfaz')
def interfaz():
    id_estudiante= session.get('id_estudiante')
    nombre= session.get('nombre_estudiante')
    grado= session.get('grado_estudiante')
    grupo= session.get('grupo_estudiante')
    cursor= mysql.connection.cursor()
    cursor.execute('SELECT * FROM railway.trabajos WHERE grado_trabajo = %s',(grado,))
    trabajos = cursor.fetchall()

    return render_template('interfaz.html', nombre=nombre,grado=grado,grupo=grupo, trabajos=list(reversed(trabajos)), id_estudiante= id_estudiante)

#region Logout
@app.route('/logout', methods= ['POST'])
def logout():
    return out.out()

#region interfaz maestro
@app.route('/maestro')
def interfaz_maestro():
    cursor= mysql.connection.cursor()
    id_maestro= session.get('id_maestro')
    nombre_maestro= session.get('nombre_maestro')
    cursor.execute('SELECT * FROM railway.trabajos WHERE id_maestro = %s', (id_maestro,))
    trabajos= cursor.fetchall()
    if trabajos:
        felimite= trabajos[0][3]
        fecha_formateada= datetime.strftime(felimite, '%d %h, %I:%M %p' ) 
    return render_template('interfaz_maestro.html',trabajos=reversed(trabajos),nombre= nombre_maestro, id_maestro= id_maestro ,fecha= fecha_formateada )

@app.route('/login_maestro', methods= ['GET','POST'])
def interfaz_loginMaestro():
    if request.method == 'POST':
        return log_maestro.log()

    return render_template('login_maestro.html')

@app.route('/registro_maestro')
def registro_maestro():
    return render_template('register_maestro.html')

#region CRUD

def allowed_file(file):

    file= file.split('.')

    if file[1] in ALLOWED_EXTENSIONS:
        return True
    return False

@app.route('/add')
def add():
    return render_template('add.html', grados= grados())

@app.route('/upload', methods=['POST'])
def upload():
    nombre_actividad= request.form['nombre_actividad']
    descripcion= request.form['descripcion']
    fecha_limte= request.form['limitdate']
    grado= request.form['grado']
    id_maestro= session.get('id_maestro')
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(nombre_actividad))

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        return 'Folder already exists'

    files = request.files.getlist('file[]')
    for file in files:
        if file.filename == '':
            return 'No selected file'
        if file:
            cursor= mysql.connection.cursor()
            filename = secure_filename(file.filename)
            file.save(os.path.join(folder_path, filename))
            cursor.execute('INSERT INTO railway.trabajos (nombre_actividad,descripcion_trabajo, fecha_limite_trabajo ,grado_trabajo, nombre_carpeta_trabajo ,id_maestro ) VALUES (%s,%s,%s,%s,%s,%s)',(nombre_actividad, descripcion,fecha_limte,grado,filename,id_maestro))
            mysql.connection.commit()
            return redirect(url_for('interfaz_maestro'))


@app.route('/delete/<string:id_trabajo>')
def delete(id_trabajo):
    cursor= mysql.connection.cursor()
    cursor.execute('DELETE FROM railway.trabajos WHERE id_trabajo =%s',(id_trabajo))
    mysql.connection.commit()
    return redirect(url_for('interfaz_maestro'))



@app.route('/update/<string:id_trabajo>', methods= ['GET','POST'])
def update(id_trabajo):
    cursor= mysql.connection.cursor()
    cursor.execute('SELECT * FROM railway.trabajos WHERE id_trabajo= %s', (id_trabajo))
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
            cursor.execute('UPDATE railway.trabajos  SET nombre_actividad = %s, descripcion = %s, filename = %s WHERE id_trabajo = %s ', (nombre_actividad, descripcion, filename, id_trabajo,))
            mysql.connection.commit()

            return redirect(url_for('interfaz_maestro'))
    
    
    return render_template('update.html',datos=datos)




@app.route('/ver_actividad/<string:id>', methods= ['GET', 'POST'])
def  ver_actividad(id):
    cursor= mysql.connection.cursor()
    cursor.execute('SELECT * FROM railway.trabajos WHERE id_trabajo = %s',(id))
    trabajos = cursor.fetchall()
    if trabajos:
        session['filename']= trabajos[0][4]
        fecha = trabajos[0][3]
        fecha_forma= datetime.strftime(fecha, '%d %h, %I:%M %p')
    
    nombre= session.get('nombre_estudiante')
    grado= session.get('grado_estudiante')
    grupo= session.get('grupo_estudiante')

    cursor.execute('SELECT * FROM railway.trabajos WHERE grado_trabajo = %s', (grado,))
    listra= cursor.fetchall()
    cursor.close()
         
    return render_template('ver_trabajo.html', trabajos= trabajos,nombre=nombre,grado=grado,grupo=grupo,listra= reversed(listra), fecha = fecha_forma)

@app.route('/edit_profile/<string:id_estudiante>')
def edit_profile(id_estudiante):
    cursor= mysql.connection.cursor()
    cursor.execute('SELECT * FROM railway.estudiantes WHERE id_estudiante =%s' , (id_estudiante))
    datos= cursor.fetchall()
    nombre= session.get('nombre_completo')
    grado= session.get('grado')
    grupo= session.get('grupo')
    return render_template('edit_profile.html', nombre=nombre, grado=grado, grupo=grupo, datos= datos)


@app.route('/edit_profile_maestro/<string:id_maestro>')
def edit_profile_maestro(id_maestro):
    cursor= mysql.connection.cursor()
    cursor.execute('SELECT * FROM maestros.maestros WHERE id_maestro =%s' , (id_maestro))
    datos= cursor.fetchall()
    nombre_maestro= session.get('nombre_maestro')
    return render_template('edit_profile_maestro.html', nombre=nombre_maestro, datos= datos)
