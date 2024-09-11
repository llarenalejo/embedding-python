import sys
from time import strftime
from gpt4all import Embed4All
import psycopg2 
from dotenv import load_dotenv
import os
from data_embed import *

try:
    if len(sys.argv)>2:
        first_argument=sys.argv[1]
        second_argument=sys.argv[2]
        
    else:
        print("args vacio")
except Exception  as e:
    print("Error:{e}")


load_dotenv()

connection =psycopg2.connect(
    host=os.getenv('host'),
    port=os.getenv('port'),
    database=os.getenv('database'),
    user=os.getenv('user'),
    password=os.getenv('password')
)
cursor=connection.cursor()
#modificar los argumentos
if(first_argument=="1"):

    print(second_argument)
    search_term_vector=embed_text(str(second_argument))    
    cursor.execute("SELECT st.title_name,st.series_name,st.author,st.fecha_publicacion,embedding <-> '"+str(search_term_vector)+"' as distance FROM itemsv iv JOIN series_titles st ON iv.id_titulos=st.id_titulos ORDER BY iv.embedding <-> '"+str(search_term_vector)+"' LIMIT 5;")    
    data_rows=cursor.fetchall()
    for row in data_rows:        
        print(str(row))
    cursor.close()    

if(first_argument=="2"):
    
    cursor.execute("SELECT series_name,id_titulos,title_name,author,fecha_publicacion,description FROM series_titles ORDER BY id_titulos ;")    
    data_rows=cursor.fetchall()
    for row in data_rows:
        serie,id_titulo,titulo,author,fecha_publicacion,description=row
        prompt=r"el siguiente texto representa un titulo de manga o comic con los siguientes datos: titulo(nombre del titulo individual)='"+titulo+"', serie(nombre de la serie a la que pertenece el titulo)="+serie+", autor(el autor o autores de la serie)='"+author+", fecha de publicacion(fecha en que salio a la venta en formato año-mes-dia)='"+str(fecha_publicacion)+", descripcion(datos sobre la trama y de que trata la serie a la que el titulo forma parte)='"+description+"', todos estos datos son de un titulo o numero en especifico estos titulos o numeros se pueden agrupar en base al nombre de la serie a la que pertenecen"        
        row_vector=embed_text(prompt)        
        query=r"INSERT INTO itemsV (embedding,id_titulos) VALUES ('"+str(row_vector)+"',"+str(id_titulo)+")"
        cursor.execute(query)
        connection.commit()
        print(id_titulo)

connection.close()