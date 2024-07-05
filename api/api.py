import pandas as pd
import os
import json
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for Matplotlib
import matplotlib.pyplot as plt
import io
from flask import Flask, jsonify,send_file
from flask_cors import CORS 

app = Flask(__name__)

CORS(app,resources={r"/*":{"origins":"*"}})

CARPETA_IMG = "img"
ARCHIVO_TXT = "data.txt"
ARCHIVO_JSON = "users.json"

""" for carpeta in [CARPETA_IMG]:
    os.makedirs(carpeta, exist_ok=True)
    
app.config["CARPETA_IMG"] = CARPETA_IMG """

def readTxt():
    if os.path.exists(ARCHIVO_TXT):
        datosDf = []
        with open(ARCHIVO_TXT, mode="r",encoding="utf-8") as file:
            datosAvistamientos=json.load(file)
            for obs in datosAvistamientos:
                datosDf.append({
                    "ID":int(obs["id"]),
                    "Nombre":obs["species"],
                    "Descripcion":obs["description"] if obs["description"] else "Descripción no disponible" ,
                    "Fecha":obs["dateObserved"],
                    "Categoria":obs["category"],
                    "Latitud":obs["location"]["latitud"],
                    "Longitud":obs["location"]["longitud"],
                    "Observador":obs["observer"]["name"],
                    "Numero_Observaciones":obs["observer"]["observationsCount"],
                    "Ciudad":obs["placeObservation"]["city"],
                    "Departamento":obs["placeObservation"]["department"],
                    "Pais":obs["placeObservation"]["country"],
                    "Imagenes":obs["photos"]
                })
                
    return datosDf

def readUsers():
    if os.path.exists("users.json"):
        dataUsers = []
        with open(ARCHIVO_JSON, 'r') as file:
          users = json.load(file)
          for userId, info in users.items():
            dataUsers.append({
                "ID":int(userId),
                "Nombre": info['nombre'],
                "Email": info['email'],
                "Contraseña": info['password'],
                "Perfil": info['perfil']
            })
    return dataUsers

def graphicsAPI():
    datosDf = []
    with open(ARCHIVO_TXT, mode="r",encoding="utf-8") as file:
        datosAvistamientos=json.load(file)
        for obs in datosAvistamientos:
            datosDf.append({
                "Nombre":obs["species"],                    
                "Fecha":obs["dateObserved"],
                "Categoria":obs["category"],            
                "Observador":obs["observer"]["name"],
                "Ciudad":obs["placeObservation"]["city"],
                "Departamento":obs["placeObservation"]["department"],   
            })
    df = pd.DataFrame(datosDf)
    fig, axs = plt.subplots(2,2,figsize=(12,10))
    
    df.groupby('Nombre').size().plot(kind='bar', ax=axs[0, 0])
    axs[0, 0].set_title('Número de Observaciones por Especie')
    axs[0, 0].set_xlabel('Especie')
    axs[0, 0].set_ylabel('No. de Observaciones')

    df.groupby('Ciudad').size().plot(kind='bar', ax=axs[0, 1])
    axs[0, 1].set_title('Número de Observaciones por Ciudad')
    axs[0, 1].set_xlabel('Ciudad')
    axs[0, 1].set_ylabel('No. de Observaciones')

    df.groupby('Categoria').size().plot(kind='bar', ax=axs[1, 0])
    axs[1, 0].set_title('Número de Observaciones por Categoría')
    axs[1, 0].set_xlabel('Categoría')
    axs[1, 0].set_ylabel('No. de Observaciones')

    df.groupby('Departamento').size().plot(kind='bar', ax=axs[1, 1])
    axs[1, 1].set_title('Número de Observaciones por Departamento')
    axs[1, 1].set_xlabel('Departamento')
    axs[1, 1].set_ylabel('Número de Observaciones')
    
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)

    return send_file(img, mimetype='image/png')


@app.route("/obs/", methods=["GET"])
def loadObs():
    obs = readTxt()
    return jsonify(obs)

@app.route("/users/", methods=["GET"])
def loadUsers():
    users = readUsers()
    return jsonify(users)

@app.route('/plots.png')
def plot():
    grafico = graphicsAPI()
    return grafico

@app.errorhandler(500)
def errorInterno(error):
    return jsonify({"error":"ocurrio error interno en el servidor"}),500

@app.errorhandler(404)
def noEncontrado(error):
    return jsonify({"error":"Recurso no encontrado."}),404

if __name__ == "__main__":
    app.run(debug=True)
