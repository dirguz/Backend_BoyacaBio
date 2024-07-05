import pandas as pd
import json
import random
import os
import pwinput
import bcrypt
import re

fileUsers = 'users.json'

def hashPass(pas):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pas.encode('utf-8'), salt)
    return hashed

def checkPass(storePass, inputPass):
    return bcrypt.checkpw(inputPass.encode('utf-8'),storePass)

def isValidEmail(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def loadUsers():
    if not os.path.exists(fileUsers):
        return {}
    with open(fileUsers, 'r') as file:
        return json.load(file)
    
def saveUser(users):
    with open(fileUsers, 'w') as file:
        json.dump(users, file, indent=4)
 
def createUser(users):
    name = input("Ingrese el nombre de usuario: ")
    email = input("Ingrese el Email: ")
    while not isValidEmail(email):
        print("Formato de Email incorrecto")
        email = input("Ingrese el Email: ")
    password = pwinput.pwinput("Ingrese la contraseña del usuario: ")
    userId = str(random.randint(1000,9999))
    profile = "user"
    users[userId] = {'nombre':name, 'email':email, 'password': hashPass(password).decode(), 'perfil':profile}
    print(f"Usuario registrado con ID: {userId}")
    
def updateUser(users):
    userId = input("Ingrese el ID del usuario a actualizar: ")
    if userId in users:
        name = input("Ingrese el nuevo nombre de usuario: ")
        email = input("Ingrese el nuevo Email: ")
        while not isValidEmail(email):
            print("Formato de Email incorrecto")
            email = input("Ingrese el nuevo Email del usuario: ")
        password = pwinput.pwinput("Ingrese la nueva contraseña del usuario: ")
        print("Defina el perfil del usuario")
        print("1. Administrador")
        print("2. Usuario")
        categoria=input("\nIngrese la opción deseada: ")
        if categoria == "1":
            profile="admin"
        elif categoria == "2":
            profile="user"    
        users[userId] = {'nombre':name, 'email':email, 'password': hashPass(password).decode(), 'perfil':profile}
        print("Usuario actualizado correctamente.")
    else:
        print("Usuario no encontrado.")
        
def deleteUser(users):
    userId = input("Ingrese el ID del usuario a eliminar: ")
    if userId in users:
        del users[userId]
        print("Usuario eliminado correctamente.")
    else:
        print("Usuario no encontrado.")

def showUsers(users):
    if users:
        usersDF=[]
        print("\n Lista de Usuarios:")
        for userId, info in users.items():
            usersDF.append({
                "ID":userId,
                "Nombre": info['nombre'],
                "Email": info['email'],
                "Contraseña": info['password'],
                "Perfil": info['perfil']
            })
        df=pd.DataFrame(usersDF)
        print(df)    
    else:
        print("No hay usuarios registrados")

def mainMenuUsers():
    users = loadUsers()
    while True:
        print("\nMenú Usuarios:")
        print("1. Agregar Usuario")
        print("2. Actualizar Usuario")
        print("3. Eliminar Usuario")
        print("4. Listado de Usuarios")
        print("5. Salir")
        
        opcion = input("Seleccione una opcion: ")
        
        if opcion == '1':
            createUser(users)
        elif opcion == '2':
            updateUser(users)
        elif opcion == '3':
            deleteUser(users)
        elif opcion == '4':
            showUsers(users)
        elif opcion == '5':
            saveUser(users)
            print("Datos guardados")
            break
        else:
            print("Opción no valida, favor intente de nuevo")

if __name__ == '__main__':
    mainMenuUsers()       