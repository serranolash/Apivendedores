import requests
from flask import Flask, render_template, request
import json
import time
import pandas as pd

app = Flask(__name__)
@app.route('/')

def home():
    return render_template('base.html')
@app.route('/contacto.html')

def contacto():
    return render_template('contacto.html')

@app.route('/base.html')

def base():
    return render_template('base.html')


@app.route('/index.html', methods=['GET', 'POST'])
def index():
    r = None
    if request.method == 'POST':
        codigo = request.form['codigo']
        base_de_datos = request.form['base_de_datos']
        payload = {'query':codigo , 'preciocero':'true', 'stockcero':'true', 'exacto':True }
        r = requests.get('http://190.220.155.74:8008/api.Dragonfish/ConsultaStockYPrecios/', 
                 params=payload, 
                 headers={'IdCliente' : "APIALEX", 
                          'Authorization' : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c3VhcmlvIjoiQURNSU4iLCJwYXNzd29yZCI6IjFhZjIwZWY4Njk5MjI0MzU1ZTdjNWQ3MTYwY2JlMjAzOTIwZWU4MGU1Zjg5ZDFmNjM5OTQ1YTQ2OWM0OWFkMmEiLCJleHAiOiIxNjg3NjM4OTEyIn0.NCAE0WEuhppe2fLOO21gtWy658F-Uh95iWWUfZ0NpVU', 
                          'BaseDeDatos' : base_de_datos,
                          'limit':'3' },
                 
                 ) # define un tiempo de espera de 30 segundos      
                        
        if r is not None and r.status_code == 200:
            resultados = r.json()
            #print(resultados) # imprime los resultados en la consola para verificar su contenido
           

            return render_template('resultados.html', resultados=resultados)
        else:
            print(f"Error en la solicitud: {r.status_code}")
    return render_template('index.html')
 
@app.route('/stock.html', methods=['GET', 'POST'])

def stock():
    if request.method == 'POST':
        codigo = request.form['codigo']
        base_de_datos = 'DEPOSEVN'
        payload = {'query': codigo, 'preciocero': 'true', 'stockcero': 'true', 'exacto': True }
        timeout = 300 # define un tiempo de espera de 5 minutos
        start_time = time.time() # captura el tiempo inicial de la consulta
        while True:
            r = requests.get('http://190.220.155.74:8008/api.Dragonfish/ConsultaStockYPreciosEntreLocales/', 
                     params=payload, 
                     headers={'IdCliente' : "APIALEX", 
                              'Authorization' : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c3VhcmlvIjoiQURNSU4iLCJwYXNzd29yZCI6IjFhZjIwZWY4Njk5MjI0MzU1ZTdjNWQ3MTYwY2JlMjAzOTIwZWU4MGU1Zjg5ZDFmNjM5OTQ1YTQ2OWM0OWFkMmEiLCJleHAiOiIxNjg3NjM4OTEyIn0.NCAE0WEuhppe2fLOO21gtWy658F-Uh95iWWUfZ0NpVU', 
                              'BaseDeDatos' : base_de_datos,
                              'limit':'10' },
                     timeout=timeout) 
            elapsed_time = time.time() - start_time # calcula el tiempo transcurrido
            if r.status_code == 200:               
               resultados = r.json()               
               articulo_descripcion = resultados['Resultados'][0]['ArticuloDescripcion']
               articulo_color = resultados['Resultados'][0]['Color']
               articulo_colordescripcion = resultados['Resultados'][0]['ColorDescripcion']
               stock = []
        
                             
               for resultado in resultados['Resultados']:
                   articulo_talle = resultado.get('Talle', 'Talle desconocido')
                   stock.append({'BaseDeDatos': resultado.get('BaseDeDatos', 'Base de datos desconocida'), 'Stock': resultado.get('Stock', 'Sin stock disponible'), 'Talle': articulo_talle})
               
                   
               return render_template('resultados2.html', articulo_descripcion=articulo_descripcion, stock=stock, articulo_color=articulo_color, articulo_colordescripcion=articulo_colordescripcion, resultados=resultados)               
            elif elapsed_time >= timeout:
                print("Tiempo de espera agotado.")
                break # si el tiempo de espera se agota, sale del bucle
            else:
                print(f"Error en la solicitud: {r.status_code}. Reintentando en 10 segundos.")
                time.sleep(10) # espera 10 segundos y vuelve a intentarlo
    return render_template('stock.html')

if __name__ == '__main__':
    app.run()
