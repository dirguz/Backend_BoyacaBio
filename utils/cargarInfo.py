import pandas as pd
import matplotlib.pyplot as plt
import json
import random

""" datosAvistamientos=[
    {
    "id":0,
    "species":"Prueba1",
    "description":"texto alterno",
    "dateObserved":"2024-04-21",
    "category":"Fauna",
    "location":{
        "latitud":"5.7334876058",
        "longitud":"-73.1738433836"
        },
    "observer":{
        "name":"observerName",
        "observationsCount":2,
    },
    "placeObservation":{
        "city":"Sotaquira", 
        "department":"Boyacá", 
        "country":"Colombia"
        },
    "photos":["https://inaturalist-open-data.s3.amazonaws.com/photos/377888853/square.jpeg","https://inaturalist-open-data.s3.amazonaws.com/photos/377842891/square.jpg"]
    }
] """

def cargarDatos():
    try:
        with open("data.txt", "r") as file:
            datosAvistamientos=json.load(file)
    except FileNotFoundError:
        datosAvistamientos=[]
    return datosAvistamientos

def mostrarDatos():
    try:
        datosDf = []
        with open("data.txt", "r") as file:
            datosAvistamientos=json.load(file)
            for obs in datosAvistamientos:
                datosDf.append({
                    "ID":obs["id"],
                    "Nombre":obs["species"],
                    "Descripción":obs["description"],
                    "Fecha":obs["dateObserved"],
                    "Categoria":obs["category"],
                    "Latitud":obs["location"]["latitud"],
                    "Longitud":obs["location"]["longitud"],
                    "Observador":obs["observer"]["name"],
                    "Numero_Observaciones":obs["observer"]["observationsCount"],
                    "Ciudad":obs["placeObservation"]["city"],
                    "Departamento":obs["placeObservation"]["department"],
                    "Pais":obs["placeObservation"]["country"],
                    "Imagenes":", ".join(obs["photos"])
                })
            df = pd.DataFrame(datosDf)
            pd.set_option("display.max_columns",None)
    except FileNotFoundError:
        df=[]
    return df

def guardarDatos(datos): 
    nuevaObservacion={}
    nuevaObservacion["id"]=str(random.randint(1000,9999))
    nuevaObservacion["species"]=input("\nIngrese nombre de la especie observada: ")
    nuevaObservacion["description"]=input("\nIngrese descripción de la especie observada: ")
    nuevaObservacion["dateObserved"]=input("\nIngrese fecha de la observación (YYYY-MM-DD)): ")
    print("\nIndique la categoria a la que pertenece la especie: \n")
    print("1. Flora")
    print("2. Fauna")
    print("3. Ecosistemas")
    print("4. Otros")
    categoria=input("\nIngrese la opción deseada: ")
    if categoria == "1":
        nuevaObservacion["category"]="Flora"
    elif categoria == "2":
        nuevaObservacion["category"]="Fauna"
    elif categoria == "3":
        nuevaObservacion["category"]="Ecosistemas"
    elif categoria == "4":
        nuevaObservacion["category"]="Otros"   

    nuevaCoordenada={}
    nuevaCoordenada["latitud"]=round(float(input("\nIngrese latitud del lugar (en decimales): ")),6)
    nuevaCoordenada["longitud"]=round(float(input("\nIngrese longitud del lugar (en decimales): ")),6)
    nuevaObservacion["location"]=nuevaCoordenada
    
    nuevoUsuario={}
    nuevoUsuario["name"]=input("\nIngrese el nombre del observador: ")
    nuevoUsuario["observationsCount"]=1        
    for i in datos:
        if i["observer"]["name"].lower()==nuevoUsuario["name"].lower():
            nuevoUsuario["observationsCount"]+=1            
    nuevaObservacion["observer"]=nuevoUsuario
    
    nuevoLugar={}
    nuevoLugar["city"]=input("\nIngrese la ciudad o municipio de la observación: ")
    nuevoLugar["department"]=input("\nIngrese el departamento de la observación: ")
    nuevoLugar["country"]="Colombia"
    nuevaObservacion["placeObservation"]=nuevoLugar

    nuevaFoto=[]
    while True:
        foto=input("\nIngrese la url de la fotografía de la observación: ")
        nuevaFoto.append(foto)
        res=input("\n¿Desea ingresar más fotografías?: \n1. Si \n2. No\n")
        if res.lower() =="2":
            break
    nuevaObservacion["photos"]=nuevaFoto
    
    datos.append(nuevaObservacion)
    with open("data.txt", "w") as f:
        json.dump(datos, f, indent=4)

def actualizarDatos(datos):
    idObs=input("\nIngrese el ID de la observación a modificar: ")
    datoEncontrado=False
    for dato in datos:
        if dato["id"] == idObs:
            datoEncontrado=True
            print("\nEl registro a modificar es: ")
            print(dato)            
            while True:
                print("\nSeleccione el campo que desea actualizar\n")
                print("1. Decripción y Fecha Observación")
                print("2. Latitud y Longitud")
                print("3. Lugar de observación")
                print("4. Enlaces de fotografías")
                opcion=input("\nIngrese la opción deseada: ")
                
                if opcion == "1":
                    dato["description"]=input("\nIngrese la nueva descripción de la especie observada: ")
                    dato["dateObserved"]=input("\nIngrese la nueva fecha de la observación (YYYY-MM-DD)): ")
                    print("\nIndique la nueva categoria a la que pertenece la especie: \n")
                    print("1. Flora")
                    print("2. Fauna")
                    print("3. Ecosistemas")
                    print("4. Otros")
                    categoria=input("\nIngrese la opción deseada: ")
                    if categoria == "1":
                        dato["category"]="Flora"
                    elif categoria == "2":
                        dato["category"]="Fauna"
                    elif categoria == "3":
                        dato["category"]="Ecosistemas"
                    elif categoria == "4":
                        dato["category"]="Otros"
                elif opcion == "2":
                    dato["location"]["latitud"]=round(float(input("\nIngrese nueva latitud del lugar (en decimales): ")),6)
                    dato["location"]["longitud"]=round(float(input("\nIngrese nueva longitud del lugar (en decimales): ")),6)
                elif opcion == "3":
                    dato["placeObservation"]["city"]=input("\nIngrese la nueva ciudad o municipio de la observación: ")
                    dato["placeObservation"]["department"]=input("\nIngrese el nuevo departamento de la observación: ")   
                elif opcion == "4":
                    nuevaFoto=[]
                    while True:
                        foto=input("\nIngrese la nueva url de la fotografía de la observación: ")
                        nuevaFoto.append(foto)
                        res=input("\n¿Desea ingresar más fotografías?: \n1. Si \n2. No\n")
                        if res.lower() =="2":
                            break
                    dato["photos"]=nuevaFoto                
                with open("data.txt", "w") as f:
                    json.dump(datos, f, indent=4)
                print("\nEl registro fue modificado exitosamente")
                res=input("\n¿Desea realizar alguna otra actualización?: \n1. Si \n2. No\n")
                if res.lower() =="2":
                    break
    if not datoEncontrado:
        print("\nRegistro no encontrado")
    
def eliminarDatos(datos,id):
    prevLen=len(datos)  
    datos[:]=[item for item in datos if not (item.get('id') == id)]
    with open("data.txt", "w") as f:
        json.dump(datos, f, indent=4)
    if len(datos)<prevLen:
        print("\nRegistro eliminado exitosamente")
    else:
        print("\nRegistro no encontrado")
        
def analisisDatos():  
    datosDf = []
    with open("data.txt", "r") as file:
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

    if df.empty:
        print("No hay datos disponibles")
        return
    
    df["Fecha"]=pd.to_datetime(df["Fecha"])
    df=df.drop_duplicates()
    df=df.dropna()
    
    print("\nAnálisis de datos")
    print("\nEstadísticas:")
    print(df.describe(include="all"))
    print("\nTendencias por Especie:")
    print(df.groupby('Nombre').size())
    print("\nDistribución por lugar:")
    print(df.groupby('Ciudad').size())
    print("\nObservaciones por categoria")
    print(df.groupby('Categoria').size())
    
def graphics():
    datosDf = []
    with open("data.txt", "r") as file:
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
    
    # Primer gráfico: Número de observaciones por especie
    df.groupby('Nombre').size().plot(kind='bar', ax=axs[0, 0])
    axs[0, 0].set_title('Número de Observaciones por Especie')
    axs[0, 0].set_xlabel('Especie')
    axs[0, 0].set_ylabel('No. de Observaciones')

    # Segundo gráfico: Número de observaciones por ciudad
    df.groupby('Ciudad').size().plot(kind='bar', ax=axs[0, 1])
    axs[0, 1].set_title('Número de Observaciones por Ciudad')
    axs[0, 1].set_xlabel('Ciudad')
    axs[0, 1].set_ylabel('No. de Observaciones')

    # Tercer gráfico: Número de observaciones por categoría
    df.groupby('Categoria').size().plot(kind='bar', ax=axs[1, 0])
    axs[1, 0].set_title('Número de Observaciones por Categoría')
    axs[1, 0].set_xlabel('Categoría')
    axs[1, 0].set_ylabel('No. de Observaciones')

    # Cuarto gráfico: Número de observaciones por departamento
    df.groupby('Departamento').size().plot(kind='bar', ax=axs[1, 1])
    axs[1, 1].set_title('Número de Observaciones por Departamento')
    axs[1, 1].set_xlabel('Departamento')
    axs[1, 1].set_ylabel('Número de Observaciones')
    
    plt.tight_layout()   
    plt.show()
       
 