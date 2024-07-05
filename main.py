from utils.cargarInfo import mostrarDatos,guardarDatos,actualizarDatos,eliminarDatos,cargarDatos,analisisDatos,graphics
from utils.users import loadUsers,createUser,mainMenuUsers,saveUser,checkPass
import pwinput
 
def menu():
    users=loadUsers()
    loginUser = False
    print("\nIniciar Sesion")
    usuario=input("\nIngrese el usuario: ")
    password=pwinput.pwinput("\nIngrese la constraseña: ")
    for user in users.values():
        if user.get('nombre')==usuario and checkPass(user.get('password').encode(),password):
            loginUser=True
            datosAvistamientos=cargarDatos()
            if user.get('perfil')=='admin':
                while True:
                    print(f"\nSesion iniciada para {user.get('nombre')}")
                    print("\nMenu de Opciones")
                    print("1. Ver registro de observaciones")
                    print("2. Ingresar nueva observación")
                    print("3. Modificar registro de observación")
                    print("4. Eliminar registro de observación")
                    print("5. Menú Usuarios")
                    print("6. Estadisticas")
                    print("7. Salir")
                    option=input("\nElija una opción: ")
                    if option=="1":
                        print(f"\n{len(mostrarDatos())} registros cargados exitosamente: \n")
                        print(mostrarDatos())
                    elif option=="2":
                        guardarDatos(datosAvistamientos)
                        print("\nEl registro fue ingresado correctamente")
                    elif option=="3":
                        #print(datosAvistamientos)
                        actualizarDatos(datosAvistamientos)
                    elif option=="4":
                        idObs=input("\nIngrese el ID de la observación a eliminar: ")
                        eliminarDatos(datosAvistamientos,idObs)
                    elif option=="5":
                        mainMenuUsers()
                    elif option=="6":
                        analisisDatos()
                        graphics()
                    elif option=="7":
                        break
                    else: print("\nOpción no valida")
            else:
                while True:
                    print(f"\nSesion iniciada para {user.get('nombre')}")
                    print("\nMenu de Opciones")
                    print("1. Ver registro de observaciones")
                    print("2. Ingresar nueva observación")
                    print("3. Modificar registro de observación")
                    print("4. Eliminar registro de observación")
                    print("5. Estadisticas")
                    print("6. Salir")
                    option=input("\nElija una opción: ")
                    if option=="1":
                        print(f"\n{len(mostrarDatos())} registros cargados exitosamente: \n")
                        print(mostrarDatos())
                    elif option=="2":
                        guardarDatos(datosAvistamientos)
                        print("\nEl registro fue ingresado correctamente")
                    elif option=="3":
                        #print(datosAvistamientos)
                        actualizarDatos(datosAvistamientos)
                    elif option=="4":
                        idObs=input("\nIngrese el ID de la observación a eliminar: ")
                        eliminarDatos(datosAvistamientos,idObs)
                    elif option=="5":
                        analisisDatos()
                        graphics()
                    elif option=="6":
                        break
                    else: print("\nOpción no valida")
    if not loginUser:
        print("\nEl usuario o contraseña no existe")
        res=input("\n¿Desea realizar el registro?: \n1. Si \n2. No\n")
        if res.lower() =="1":
            createUser(users)
            saveUser(users)
            menu()
        else:
            menu()  
               
menu();