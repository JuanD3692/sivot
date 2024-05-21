
import mysql.connector

def conexion():
    #return  mysql.connector.connect(host='localhost', user='root', password='', db='votaciones')
    return  mysql.connector.connect(host='db4free.net', user='marcos6533', password='753b112c', db='votaciones1')
  
def verificar(cedula):
    connect=conexion()  
    cursor = connect.cursor()           
    cursor.execute("select cedula from usuarios")
    verificar=False     
    for fila in cursor:
        if fila[0] == cedula:
            verificar = True
    if verificar == True:
        comprobar = True
    else:
     comprobar = False
    connect.close()
    return comprobar

  
    
def verificar_voto(cedula):
    connect=conexion()  
    cursor = connect.cursor()           
    sql=("SELECT voto FROM usuarios WHERE cedula=%s")
    verificar=False     
    adr = (cedula,)
    cursor.execute(sql, adr)     
    for fila in cursor:
        if fila[0]=='Si':
            verificar=True
    return verificar         
   
    
    
def Numero_personas_votaron():
    connect=conexion()
    cursor = connect.cursor()         
    cursor.execute("select voto from usuarios") 
    si_voto=0     
    for fila in cursor:
        if fila[0]=='Si':
            si_voto+=1
    connect.close()   
    return si_voto            



def Numero_personas_no_votaron():
    connect=conexion()
    cursor = connect.cursor() 
    cursor.execute("select voto from usuarios") 
    no_voto=0      
    for fila in cursor:
        if fila[0]=='No':
            no_voto+=1
    connect.close()     
    return no_voto   


def votos():
    connect=conexion()
    cursor = connect.cursor() 
    cursor.execute("SELECT nombre,apellido,votos FROM candidatos") 
    candidatos=[]  
    for fila in cursor:
        candidatos.append(fila)
    connect.close()     
    return candidatos


def porcentajes():
    connect=conexion()
    cursor = connect.cursor() 
    cursor.execute("SELECT  votos from candidatos") 
    total_votos=0
    #(total_candidato/total_votos)*100 
    for fila in cursor:
        if fila[0]>0:
            total_votos=total_votos+fila[0]              
    return total_votos                    


def Insertar_candidato(nombre,apellido,votos,foto):
    connect=conexion()
    cursor = connect.cursor()         
    sql="insert into candidatos(nombre, apellido,votos,foto_name) values (%s,%s,%s,%s)"
    datos=(nombre, apellido,votos,foto)
    cursor.execute(sql,datos)
    connect.commit()
    connect.close()   
    
def insert_user(username,apellido,cedula,expedicion,voto):
    connect=conexion()
    cursor = connect.cursor()
    sql=('INSERT  INTO usuarios (nombre,apellido,cedula,expedicion,voto)values (%s,%s,%s,%s,%s)')
    datos=(username,apellido,cedula,expedicion,voto)
    cursor.execute(sql,datos)
    connect.commit()  
   


 
def Numero_personas_habilitas():
    connect=conexion()
    cursor = connect.cursor() 
    cursor.execute("select voto from usuarios") 
    num_personas=0      
    for fila in cursor:
        num_personas+=1
    connect.close()    
    return num_personas 
   
def update(cedula):  
    connect=conexion()
    cursor = connect.cursor()           
    sql = "SELECT * FROM usuarios WHERE cedula = %s"
    adr = (cedula, )
    list=[]
    cursor.execute(sql, adr)
    verificar=False
    for x in cursor:
     if x[3]==cedula:
        list.append(x[1])
        list.append(x[2])
        list.append(x[3])  
        verificar=True
     else:
        verificar=False
    list1=[]    
    if verificar==True:     
      list1=list
    else:
      list1.append('False')
    return list1

def actualizar(nombre,apellido,cedula):   
    connect=conexion()
    cursor = connect.cursor()           
    sql = "UPDATE usuarios SET nombre= %s, apellido=%s WHERE cedula = %s"
    adr = (nombre,apellido,cedula, )
    cursor.execute(sql, adr)
    connect.commit()

def actualizarreloj(fecha,horas,minutos,segundos,tipo):
    connect=conexion()
    cursor = connect.cursor()           
    sql = "UPDATE comenzar_votacion SET fecha= %s, horas=%s, minutos=%s, segundos=%s where id =%s"
    adr = (fecha,horas,minutos,segundos,tipo)
    cursor.execute(sql, adr)
    connect.commit()


def contacto(nombre,correo,mensaje):
    connect=conexion()
    cursor = connect.cursor()          
    sql="insert into contacto(nombre, correo,mensaje) values (%s,%s,%s)"
    datos=(nombre,correo,mensaje)
    cursor.execute(sql,datos)
    connect.commit()
    connect.close()
    
def verificar_contacto(correo):
    connect=conexion()
    cursor = connect.cursor()
    sql=("SELECT correo from contacto Where correo=%s")
    verificar=False
    adr = (correo,)
    cursor.execute(sql, adr)     
    for fila in cursor:
        if fila[0]==correo:
            verificar=True
    return verificar 
       
def traer_contacto():
   lista_contacto=[] 
   connect=conexion()
   cursor = connect.cursor() 
   cursor.execute('SELECT nombre,correo, mensaje From contacto')
   for i in cursor:
       lista_contacto.append(i)
   return lista_contacto     

def insertar_voto(cedula):
    voto='Si'
    connect=conexion()
    cursor = connect.cursor()  
    sql=('UPDATE usuarios SET voto =%s  WHERE cedula=%s')
    adr = (voto,cedula, )
    cursor.execute(sql, adr)
    connect.commit()

def insertar_voto_candidato(id,voto_votante):
    voto_candidato=0
    connect=conexion()
    cursor = connect.cursor()  

    sql=('SELECT id,votos FROM candidatos')
    cursor.execute(sql)   
    for i in cursor:
        print(i)
        if i[0]==int(id):
            voto_candidato=int(i[1])
    print("Voto candidato",voto_candidato)
    print("Voto votante",voto_votante)
    votos=voto_candidato+voto_votante        
    print("Votos totales",votos)
    
    sql=('UPDATE candidatos SET votos =%s  WHERE id=%s') 
    adr = (votos,id)
    cursor.execute(sql, adr)
    connect.commit()

    

def comenzarv():
    comienzo=""
    try:
        connect=conexion()
        cursor = connect.cursor()           
        sql=("SELECT * FROM comenzar_votacion where id=1")
        cursor.execute(sql)  
        registro = cursor.fetchall()
        for row in registro:
            comienzo = str(row[1]) +" " + str(row[2])+":"+ str(row[3])+":"+ str(row[4])  
    except Exception as ex:
        print("")
    return comienzo


def terminarv():
    fin=""
    try:
        connect=conexion()
        cursor = connect.cursor()           
        sql=("SELECT * FROM comenzar_votacion where id=2")
        cursor.execute(sql)  
        registro = cursor.fetchall()
        for row in registro:
            fin = str(row[1]) +" " + str(row[2])+":"+ str(row[3])+":"+ str(row[4])  
    except Exception as ex:
        print("")
    return fin

def prueba_candidatos_foto():
   lista_contacto=[] 
   connect=conexion()
   cursor = connect.cursor() 
   cursor.execute('SELECT id,nombre,apellido,foto_name From candidatos')
   for i in cursor:
       lista_contacto.append(i)
   return lista_contacto

def delete_candidato(id): 
    connect=conexion()
    cursor = connect.cursor()  
    
    sql=('SELECT nombre,apellido,foto_name FROM candidatos WHERE id=%s')
    adr=(id,)
    cursor.execute(sql,adr)
    for i in cursor:
        filename=i

    sql=('DELETE FROM candidatos WHERE id=%s') 
    adr = (id, )
    cursor.execute(sql, adr)
    connect.commit() 
    return filename


def delete_mensaje(correo): 
    connect=conexion()
    cursor = connect.cursor()  
    
    sql=('DELETE FROM contacto WHERE correo=%s') 
    adr = (correo, )
    cursor.execute(sql, adr)
    connect.commit() 
