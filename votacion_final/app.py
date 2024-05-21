from flask import Flask, jsonify, redirect, request, send_from_directory, session, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import flash
import forms
from flask_wtf.csrf import CSRFProtect
import consulta
import pymysql
import io
import xlwt
from flask import Response
pymysql.install_as_MySQLdb()
import os

UPLOAD_FOLDER = os.path.abspath("static/uploads/")
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])



app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://marcos6533:753b112c@db4free.net/votaciones1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


db = SQLAlchemy(app)
ma = Marshmallow(app)
app.secret_key = 'my_secret_key'
csrf = CSRFProtect(app)


# Creacion de la tabla
class usuarios(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20))
    apellido = db.Column(db.String(20))
    cedula = db.Column(db.String(10), unique=True)
    expedicion = db.Column(db.String(10))
    voto = db.Column(db.String(2))

    def __init__(self, nombre, apellido, cedula, expedicion, voto):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.expedicion = expedicion
        self.voto = voto


# Esquema Categoria
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id', 'nombre', 'apellido',
                  'cedula', 'expedicion', 'voto')


# Una respuesta
categoria_schema = CategoriaSchema()
# Muchas respuestas
categorias_schema = CategoriaSchema(many=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = forms.LoginForm(request.form)
    cedula = login_form.cedula.data
    comenzar =  consulta.comenzarv()
    terminar = consulta.terminarv()      
    if request.method == 'POST':
        if consulta.verificar(cedula) == True:
            if consulta.verificar_voto(cedula)==False:
                
                consulta.insertar_voto(cedula) 
                session['cedula'] = login_form.cedula.data               
                return redirect(url_for('votacion'))
            else:
                success_message = 'Ya usted voto!!!'
                flash(success_message)
       
        else:
            success_message = 'No esta registrado!!!'
            flash(success_message)
    return render_template('html/login.html', form=login_form, comenzar=comenzar, terminar=terminar)

@app.route('/adminlogin',methods=['POST','GET'])
def adminlogin():
    cedula = request.form.get("cedula")
    clave = request.form.get("clave")
    if request.method == 'POST':
        if cedula == '10203010' and clave == '12345':
                session['cedula'] = cedula
                return redirect(url_for('admin'))
        else:
            success_message = 'El usuario o contraseña está incorrecto'
            flash(success_message)
    
   
    return render_template('html/adminlogin.html')

@app.route('/captar_voto',methods=['POST'])
def captar_voto():
    voto_votante=1
    id=request.form.get('candidato')
    consulta.insertar_voto_candidato(id,voto_votante)
    return jsonify({'respuesta':"oK"})

@app.route('/eliminar_candidato',methods=['POST'])
def eliminar_candidato():
    id=request.form.get('id')
    filename=consulta.delete_candidato(id)
    for i in filename:
        filename=i 
    os.unlink(os.path.join(app.config['UPLOAD_FOLDER'], filename))    
    return jsonify({'respuesta':"oK"})


@app.route('/eliminar_mensaje',methods=['POST'])
def eliminar_mensaje():
    correo=request.form.get('correo')
    consulta.delete_mensaje(correo)   
    return jsonify({'respuesta':"oK"})

@app.route('/eliminar_candidatos')
def  eliminar_candidatos():
    if 'cedula' in session:
        list=consulta.prueba_candidatos_foto()
        return  render_template('html/candidatos_delete.html',list=list)
    return render_template('html/403.html')
@app.route('/Inicio',methods=['POST','GET'])
def Inicio():
    if 'cedula' in session and 'cedula'!='10203010':
        session.pop('cedula')      
        return redirect(url_for('votacion'))
    comenzar =  consulta.comenzarv()
    terminar = consulta.terminarv()                                                        
    return render_template('index.html',comenzar=comenzar,terminar=terminar)

def return_name_photos():
    fotos=[]
    SEND_IMG = os.listdir('static/uploads/') 
    for i in SEND_IMG:
        fotos.append(i)
    return fotos


@app.route('/',methods=['GET','POST'])
def votacion():  
    list=[]
    fotos=[]
    fotos=return_name_photos()
    list=consulta.prueba_candidatos_foto()
    if 'cedula' in session:
        if session.get('cedula')!='10203010':  
            return render_template('html/votacion.html',list=list,fotos=fotos)
    comenzar =  consulta.comenzarv()
    terminar = consulta.terminarv()     
    return render_template('index.html',comenzar=comenzar,terminar=terminar)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('html/404.html')


#POST #########
@app.route('/registrar_user', methods=['POST','GET'])
def registrar_user():
    register_form = forms.RegisterForm(request.form)
    username = register_form.username.data
    apellido = register_form.apellido.data
    cedula = register_form.cedula.data
    expedicion = register_form.expedicion.data
    voto = 'No'
    if request.method=='POST':
            if consulta.verificar(cedula) == True:
                    success_message = 'Ya esta registrado!!!'
                    flash(success_message)
            else:
                try:
                    consulta.insert_user(username, apellido, cedula, expedicion, voto)
                    return redirect(url_for('Inicio'))
                except Exception as ex:
                    print(ex)
    return render_template('html/registrar_user.html', form=register_form)
   


@app.route('/registraradministrador', methods=['POST','GET'])
def registraradministrador():
    register_form = forms.RegisterForm(request.form)
    username = register_form.username.data
    apellido = register_form.apellido.data
    cedula = register_form.cedula.data
    expedicion = register_form.expedicion.data
    voto = 'No'
    if 'cedula' in session:
        if request.method=='POST':
            if consulta.verificar(cedula) == True:
                    success_message = 'Ya esta registrado!!!'
                    flash(success_message)
            else:
                try:
                    consulta.insert_user(username, apellido, cedula, expedicion, voto)
                    success_message = 'Registrado correctamente'
                    flash(success_message)                 
                except Exception as ex:
                    print(ex)
                return render_template('html/registraradministrador.html', form=register_form)
        return render_template('html/registraradministrador.html', form=register_form)                     
    return render_template('html/403.html')

def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1]in ALLOWED_EXTENSIONS

@app.route('/candidatos', methods=['POST', 'GET'])
def candadidatos():
    user = request.form.get('nombre', False)
    apellido = request.form.get("last", False)
    f= request.files.get('ourfile')
    if 'cedula' in session:
        if request.method=='POST':
            if f and allowed_file(f.filename):
                filename = f.filename
                fotos= return_name_photos()
                verificar=False
                for i in fotos:
                    if i==filename:
                        verificar=True                    
                if verificar==True:
                    success_message = 'Ya subio esta imagen'
                    flash(success_message)
                else:
                    verificar=False
                    votos =consulta.votos()
                    for i in votos:
                        print(i[0])
                        if i[0]==user:
                            if i[1]==apellido:
                                print(i[1])
                                verificar=True
                    if verificar==True:
                        success_message = 'Ya registro este candidato'
                        flash(success_message)                      
                    else:
                        f.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
                        votos=0
                        consulta.Insertar_candidato(user, apellido,votos, filename)
                        success_message = 'Subido correctamente'
                        flash(success_message)
                return render_template('html/candidatos.html')
            else:
                success_message = 'No puede subir este tipo  de archivos'
                flash(success_message)
                return render_template('html/candidatos.html')
        else:
            return render_template('html/candidatos.html')
    return render_template('html/403.html')

@app.route("/uploads/<filename>")
def get_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
 
@app.route('/admin')
def admin():
    if 'cedula' in session:
        num_personas_habilitadas = consulta.Numero_personas_habilitas()
        num_personas_votaron = consulta.Numero_personas_votaron()
        num_personas_no_votaron = consulta.Numero_personas_no_votaron()
        return render_template('html/admin.html',  num_personas_no_votaron=num_personas_no_votaron, num_personas_votaron=num_personas_votaron, num_personas_habilitadas=num_personas_habilitadas)
    return render_template('html/403.html')


@app.route('/update_user', methods=['POST', 'GET'])
def update_user():
    usuario = []
    usuario1 = []
    mensaje=''
    if request.method=='POST':
        if 'cedula' in session:
            nombre=request.form.get('nombre',False)
            apellido=request.form.get('apellido',False)
            cedula1 = request.form.get('cedula', False)
            usuario=consulta.update(cedula1)
            if usuario[0]=='False':    
                mensaje='No encontrado'
            else:    
                usuario1=usuario    
            if cedula1=='':
                mensaje=''            
            return render_template('html/update_user.html',usuario1=usuario1,mensaje=mensaje)  
    if request.method=='GET':
        return render_template('html/update_user.html',usuario1=usuario1,mensaje=mensaje)      
    return render_template('html/403.html')

@app.route('/actualizar',methods=['POST'])
def actualizar():
    nombre=request.form.get('nombre',False)
    apellido=request.form.get('apellido',False)
    cedula1=request.form.get('cedula1') 
    print(nombre)
    print(apellido)
    print(cedula1)
    consulta.actualizar(nombre,apellido,cedula1)
    return jsonify({'respuesta':"oK"})

@app.route('/actualizarreloj',methods=['POST'])
def actualizarreloj():
    fecha=request.form.get('fecha',False)
    horas=request.form.get('horas',False)
    minutos=request.form.get('minutos',False) 
    segundos=request.form.get('segundos',False)
    tipo = request.form.get('tipo',False) 
    consulta.actualizarreloj(fecha,horas,minutos,segundos,tipo)
    return jsonify({'respuesta':"oK"})

@app.route('/actualizarrelojfin',methods=['POST'])
def actualizarrelojfin():
    fecha=request.form.get('fecha2',False)
    horas=request.form.get('horas2',False)
    minutos=request.form.get('minutos2',False) 
    segundos=request.form.get('segundos2',False)
    tipo = request.form.get('tipo2',False) 
    consulta.actualizarreloj(fecha,horas,minutos,segundos,tipo)
    return jsonify({'respuesta':"oK"})


@app.route('/opciones',methods=['GET','POST'])
def opciones():
    if 'cedula' in session:
        return render_template('html/opciones.html')
    return render_template('html/403.html')

@app.route('/configurarreloj',methods=['GET','POST'])
def configurarreloj():
    if 'cedula' in session:
        return render_template('html/configurarreloj.html')
    return render_template('html/403.html')


@app.route('/Reiniciar_candidatos')
def Reiniciar_candidatos():
    connect= consulta.conexion()
    cursor = connect.cursor()
    votos=0  
    sql=('UPDATE candidatos SET votos =%s')
    adr = (votos, )
    cursor.execute(sql, adr)
    connect.commit()
    return redirect(url_for('opciones'))


@app.route('/Reiniciar_usuarios')
def Reiniciar_usuarios():
    connect=consulta.conexion()
    cursor = connect.cursor()
    voto='No'  
    sql=('UPDATE usuarios SET voto =%s')
    adr = (voto, )
    cursor.execute(sql, adr)
    connect.commit()
    connect.close()
    return redirect(url_for('opciones'))


@app.route('/descargar')
def descargar():
    if 'cedula' in session:
        connect=consulta.conexion()
        cursor = connect.cursor()           
        cursor.execute("SELECT id,nombre,apellido,votos FROM candidatos")
        result = cursor.fetchall()
        
        #Salida en Bytes
        output = io.BytesIO()
        #creacion de libro de trabajo tipo objeto
        Workbook = xlwt.Workbook()
        #Añadir a sheet
        sh = Workbook.add_sheet('Reporte candidatos')
        
        #Añadir cabeceraz
        sh.write(0, 0, 'Id')
        sh.write(0, 1, 'Nombre')
        sh.write(0, 2, 'Apellido')
        sh.write(0, 3, 'Votos') 
        celda = 1
        for row in result:
            sh.write(celda+1, 0, str(row[0]))
            sh.write(celda+1, 1, str(row[1]))
            sh.write(celda+1, 2, str(row[2]))
            sh.write(celda+1, 3, str(row[3]))
            celda += 1
    
        Workbook.save(output)
        output.seek(0)    
        return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=candidatos_report.xls"})
    return render_template('html/403.html')

@app.route('/descargar1',methods=['GET','POST'])
def descargar1():
    if 'cedula' in session:
        connect=consulta.conexion()
        cursor = connect.cursor()           
        cursor.execute("SELECT nombre,apellido,cedula,expedicion,voto FROM usuarios")
        result = cursor.fetchall()
        
        #Salida en Bytes
        output = io.BytesIO()
        #creacion de libro de trabajo tipo objeto
        Workbook = xlwt.Workbook()
        #Añadir a sheet
        sh = Workbook.add_sheet('Reporte usuarios')
        
        #Añadir cabeceraz
        sh.write(0, 0, 'Nombre')
        sh.write(0, 1, 'Apellido')
        sh.write(0, 2, 'Cedula')
        sh.write(0, 3, 'Expedicion')
        sh.write(0, 4, 'Voto') 
        celda = 1
        for row in result:
            sh.write(celda+1, 0, str(row[0]))
            sh.write(celda+1, 1, str(row[1]))
            sh.write(celda+1, 2, str(row[2]))
            sh.write(celda+1, 3, str(row[3]))
            sh.write(celda+1, 4, str(row[4]))
            celda += 1
    
        Workbook.save(output)
        output.seek(0)    
        return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=usuarios_report.xls"})
    return render_template('html/403.html')

@app.route('/contacto')
def contacto():
    lista_contac=[]
    lista_contac=consulta.traer_contacto()
    if 'cedula' in session:
        return render_template('html/contacto.html',lista_contac=lista_contac)
    return render_template('html/403.html')

@app.route('/resultados')
def resultados():
    fotos=[]
    fotos=return_name_photos()
    list=consulta.prueba_candidatos_foto()
    total_votos = consulta.porcentajes()
    votos =consulta.votos()
    return render_template('html/resultados.html',fotos=fotos, votos=votos,list=list,total_votos=total_votos)
 
@app.route('/Mensaje_contacto',methods=['POST'])
def Mensaje_contacto():
    nombre =request.form.get('nombre',False)
    email =request.form.get('email',False)
    mensaje = request.form.get('mensaje',False)
   
    if consulta.verificar_contacto(email)==False:       
            if nombre!=0 and email!=0:
                consulta.contacto(nombre,email,mensaje)  
    return jsonify({'respuesta':"oK"})


@app.route('/logout')
def logout():
    if 'cedula' in session:
        session.pop('cedula')
    return redirect(url_for('Inicio'))


if __name__ == '__main__':
    app.run(debug=True)
    with app.app_context():
        db.create_all()
