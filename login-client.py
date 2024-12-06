import client

def verificar_usuario(c: client.Client, username):
    # Solicita al servicio verificar si el usuario ya existe
    request_content = {'action': 'check_user', 'username': username}
    request = client.Request('login', request_content)
    c.send(request)  # Enviar solicitud al bus

    response = c.receive()  # Recibir respuesta del bus
    return response.content

def registrar_usuario(c: client.Client):
    print("\n--- Registro de Usuario ---")

    nombre = input("Nombre: ")
    apellido = input("Apellido: ")

    # Verificar nombre de usuario disponible en un bucle
    while True:
        username = input("Nombre de usuario: ")
        response = verificar_usuario(c, username)
        if response.get('status') == 'exists':
            print("Error: El nombre de usuario ya existe. Intenta con otro.")
        else:
            break

    password = input("Contraseña: ")

    request_content = {
        'action': 'register',
        'nombre': nombre,
        'apellido': apellido,
        'username': username,
        'password': password
    }
    request = client.Request('login', request_content)
    c.send(request)  # Enviar solicitud al bus

    response = c.receive()  # Recibir respuesta del bus
    print("Respuesta:", response.content.get('message'))

def crear_fonda(c: client.Client):
    print("\n--- Crear Fonda ---")
    nombre = input("Nombre de la fonda: ")
    mesas = int(input("Cantidad de mesas: "))

    request_content = {
        'action': 'create',
        'nombre': nombre,
        'mesas': mesas
    }
    request = client.Request('fonda', request_content)
    c.send(request)  # Enviar solicitud al bus

    response = c.receive()  # Recibir respuesta del bus
    print("Respuesta:", response.content.get('message'))

def listar_fondas(c: client.Client):
    print("\n--- Listado de Fondas ---")

    request_content = {'action': 'list'}
    request = client.Request('fonda', request_content)
    c.send(request)  # Enviar solicitud al bus

    response = c.receive()  # Recibir respuesta del bus
    if response.content.get('status') == 'success':
        fondas = response.content.get('fondas', [])
        if fondas:
            for f in fondas:
                print(f"ID: {f['id']}, Nombre: {f['nombre']}, Mesas: {f['mesas']}")
        else:
            print("No hay fondas registradas.")
    else:
        print("Error:", response.content.get('message'))

def eliminar_fonda(c: client.Client):
    print("\n--- Eliminar Fonda ---")

    # Solicitar listado de fondas
    request_content = {'action': 'list'}
    request = client.Request('fonda', request_content)
    c.send(request)  # Enviar solicitud al bus

    response = c.receive()  # Recibir respuesta del bus
    if response.content.get('status') == 'success':
        fondas = response.content.get('fondas', [])
        if not fondas:
            print("No hay fondas registradas.")
            return

        # Mostrar lista de fondas con su ID
        print("\nLista de Fondas:")
        for f in fondas:
            print(f"ID: {f['id']}, Nombre: {f['nombre']}, Mesas: {f['mesas']}")

        # Solicitar ID de la fonda a eliminar
        while True:
            try:
                fonda_id = int(input("\nIngrese el ID de la fonda a eliminar: "))
                if any(f['id'] == fonda_id for f in fondas):
                    break
                else:
                    print("El ID ingresado no pertenece a ninguna fonda.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número válido.")

        # Enviar solicitud para eliminar la fonda
        request_content = {'action': 'delete_fonda', 'fonda_id': fonda_id}
        request = client.Request('fonda', request_content)
        c.send(request)  # Enviar solicitud al bus

        response = c.receive()  # Recibir respuesta del bus
        print("Respuesta:", response.content.get('message'))
    else:
        print("Error:", response.content.get('message'))


def crear_operador(c: client.Client):
    print("\n--- Crear Operador ---")
    nombre = input("Nombre del operador: ")
    username = input("Username: ")
    contraseña = input("Contraseña: ")
    fonda_id = int(input("ID de la fonda: "))

    request_content = {
        'action': 'create_operator',
        'nombre': nombre,
        'username': username,
        'contraseña': contraseña,
        'fonda_id': fonda_id
    }
    request = client.Request('opera', request_content)
    c.send(request)  # Enviar solicitud al bus

    response = c.receive()  # Recibir respuesta del bus
    print("Respuesta:", response.content.get('message'))

def ver_ventas(c: client.Client):
    print("\n--- Ver Ventas ---")

    # Solicitar listado de fondas
    request_content = {'action': 'list'}
    request = client.Request('fonda', request_content)
    c.send(request)  # Enviar solicitud al bus

    response = c.receive()  # Recibir respuesta del bus
    if response.content.get('status') == 'success':
        fondas = response.content.get('fondas', [])
        if not fondas:
            print("No hay fondas registradas.")
            return

        # Mostrar lista de fondas disponibles
        print("\nLista de Fondas Disponibles:")
        for f in fondas:
            print(f"ID: {f['id']}, Nombre: {f['nombre']}, Mesas: {f['mesas']}")

        # Solicitar ID de la fonda
        while True:
            try:
                fonda_id = int(input("\nIngrese el ID de la fonda para ver las ventas: "))
                if any(f['id'] == fonda_id for f in fondas):
                    break
                else:
                    print("El ID ingresado no pertenece a ninguna fonda registrada.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número válido.")

        # Solicitar ventas de la fonda
        rango = input("Rango ('diario' o 'semanal'): ").strip().lower()
        request_content = {'action': 'view_sales', 'fonda_id': fonda_id, 'rango': rango}
        request = client.Request('fonda', request_content)
        c.send(request)  # Enviar solicitud al bus

        response = c.receive()  # Recibir respuesta del bus
        if response.content.get('status') == 'success':
            print("Ventas Totales:", response.content.get('total'))
        else:
            print("Error:", response.content.get('message'))
    else:
        print("Error:", response.content.get('message'))


def listar_operadores(c: client.Client):
    print("\n--- Listado de Operadores ---")

    request_content = {'action': 'list_operators'}
    request = client.Request('opera', request_content)
    c.send(request)  # Enviar solicitud al bus

    response = c.receive()  # Recibir respuesta del bus
    if response.content.get('status') == 'success':
        operadores = response.content.get('operadores', [])
        if operadores:
            for o in operadores:
                print(f"ID: {o['id']}, Nombre: {o['nombre']}, Username: {o['username']}, Fonda: {o['fonda']}")
        else:
            print("No hay operadores registrados.")
    else:
        print("Error:", response.content.get('message'))


def eliminar_operador(c: client.Client):
    print("\n--- Eliminar Operador ---")

    # Solicitar listado de operadores
    request_content = {'action': 'list_operators'}
    request = client.Request('opera', request_content)  # Cambiado a 'opera'
    c.send(request)  # Enviar solicitud al bus

    response = c.receive()  # Recibir respuesta del bus
    if response.content.get('status') == 'success':
        operadores = response.content.get('operadores', [])
        if not operadores:
            print("No hay operadores registrados.")
            return

        # Mostrar lista de operadores con su ID
        print("\nLista de Operadores:")
        for o in operadores:
            print(f"ID: {o['id']}, Nombre: {o['nombre']}, Username: {o['username']}, Fonda: {o['fonda']}")

        # Solicitar ID del operador a eliminar
        while True:
            try:
                operador_id = int(input("\nIngrese el ID del operador a eliminar: "))
                if any(o['id'] == operador_id for o in operadores):
                    break
                else:
                    print("El ID ingresado no pertenece a ningún operador.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número válido.")

        # Enviar solicitud para eliminar el operador
        request_content = {'action': 'delete_operator', 'operador_id': operador_id}
        request = client.Request('opera', request_content)  # Cambiado a 'opera'
        c.send(request)  # Enviar solicitud al bus

        response = c.receive()  # Recibir respuesta del bus
        print("Respuesta:", response.content.get('message'))
    else:
        print("Error:", response.content.get('message'))


def menu_admin(c: client.Client):
    while True:
        print("\n--- Menú de Administrador ---")
        print("1. Crear fonda")
        print("2. Ver listado de fondas")
        print("3. Eliminar fonda")
        print("4. Crear operador")
        print("5. Ver listado de operadores")
        print("6. Eliminar operador")
        print("7. Ver ventas")
        print("8. Cerrar sesión")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_fonda(c)
        elif opcion == "2":
            listar_fondas(c)
        elif opcion == "3":
            eliminar_fonda(c)
        elif opcion == "4":
            crear_operador(c)
        elif opcion == "5":
            listar_operadores(c)
        elif opcion == "6":
            eliminar_operador(c)
        elif opcion == "7":
            ver_ventas(c)
        elif opcion == "8":
            print("Cerrando sesión...")
            break
        else:
            print("Opción no válida.")

def iniciar_sesion(c: client.Client):
    print("\n--- Inicio de Sesión ---")
    username = input("Nombre de usuario: ")
    password = input("Contraseña: ")

    request_content = {
        'action': 'login',
        'username': username,
        'password': password
    }
    request = client.Request('login', request_content)
    c.send(request)  # Enviar solicitud al bus

    response = c.receive()  # Recibir respuesta del bus
    if response.content.get('status') == 'success':
        print(response.content.get('message'))
        role = response.content.get('role')
        if role == 'admin':
            menu_admin(c)  # Menú del administrador
        elif role == 'operador':
            user_fonda_id = response.content.get('fonda_id')
            if user_fonda_id is not None:
                menu_operador(c, user_fonda_id)  # Pasar fonda_id al menú del operador
            else:
                print("Error: No se encontró el ID de la fonda para este operador.")
        elif role == 'normal':
            menu_normal()
        else:
            print("Rol no reconocido.")
    else:
        print("Error:", response.content.get('message'))



# Función para gestionar inventario
def gestionar_inventario(c: client.Client, user_fonda_id):
    while True:
        print("\n--- Gestión de Inventario ---")
        print("1. Agregar producto")
        print("2. Actualizar producto")
        print("3. Eliminar producto")
        print("4. Ver inventario")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":  # Agregar producto
            producto = input("Nombre del producto: ")
            cantidad = int(input("Cantidad: "))
            precio = int(input("Precio: "))
            request_content = {'action': 'add', 'producto': producto, 'cantidad': cantidad, 'precio': precio, 'user_fonda_id': user_fonda_id}
            request = client.Request('invnt', request_content)
            c.send(request)
            response = c.receive()
            print("Respuesta:", response.content.get('message', 'Error al procesar la solicitud.'))

        elif opcion == "2":  # Actualizar producto
            print("\n--- Productos Disponibles ---")
            request_content = {'action': 'view', 'user_fonda_id': user_fonda_id}
            request = client.Request('invnt', request_content)
            c.send(request)
            response = c.receive()
            productos = response.content.get('productos', [])
            if productos:
                for p in productos:
                    print(f"Producto: {p['producto']}, Cantidad: {p['cantidad']}, Precio: {p['precio']}")
                producto = input("\nNombre del producto a actualizar: ")
                cantidad = int(input("Nueva cantidad: "))
                precio = int(input("Nuevo precio: "))
                request_content = {'action': 'update', 'producto': producto, 'cantidad': cantidad, 'precio': precio, 'user_fonda_id': user_fonda_id}
                request = client.Request('invnt', request_content)
                c.send(request)
                response = c.receive()
                print("Respuesta:", response.content.get('message', 'Error al procesar la solicitud.'))
            else:
                print("No hay productos disponibles para actualizar.")

        elif opcion == "3":  # Eliminar producto
            print("\n--- Productos Disponibles ---")
            request_content = {'action': 'view', 'user_fonda_id': user_fonda_id}
            request = client.Request('invnt', request_content)
            c.send(request)
            response = c.receive()
            productos = response.content.get('productos', [])
            if productos:
                for p in productos:
                    print(f"Producto: {p['producto']}, Cantidad: {p['cantidad']}, Precio: {p['precio']}")
                producto = input("\nNombre del producto a eliminar: ")
                request_content = {'action': 'delete', 'producto': producto, 'user_fonda_id': user_fonda_id}
                request = client.Request('invnt', request_content)
                c.send(request)
                response = c.receive()
                print("Respuesta:", response.content.get('message', 'Error al procesar la solicitud.'))
            else:
                print("No hay productos disponibles para eliminar.")

        elif opcion == "4":  # Ver inventario
            request_content = {'action': 'view', 'user_fonda_id': user_fonda_id}
            request = client.Request('invnt', request_content)
            c.send(request)
            response = c.receive()
            productos = response.content.get('productos', [])
            if productos:
                for p in productos:
                    print(f"Producto: {p['producto']}, Cantidad: {p['cantidad']}, Precio: {p['precio']}")
            else:
                print("No hay productos en el inventario.")

        elif opcion == "5":  # Salir
            break

        else:
            print("Opción no válida.")




# Función para gestionar promociones
# Función para gestionar promociones
def gestionar_promociones(c: client.Client, user_fonda_id):
    while True:
        print("\n--- Gestión de Promociones ---")
        print("1. Agregar promoción")
        print("2. Ver promociones")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            promocion = input("Nombre de la promoción: ")
            cantidad = int(input("Cantidad: "))
            precio = int(input("Precio: "))
            request_content = {
                'action': 'add_promotion',
                'promocion': promocion,
                'cantidad': cantidad,
                'precio': precio,
                'user_fonda_id': user_fonda_id
            }
            request = client.Request('invnt', request_content)
            c.send(request)
        elif opcion == "2":
            request_content = {
                'action': 'view_promotions',
                'user_fonda_id': user_fonda_id
            }
            request = client.Request('invnt', request_content)
            c.send(request)
        elif opcion == "3":
            break
        else:
            print("Opción no válida.")

        # Manejo de respuesta
        response = c.receive()
        if opcion == "1":
            print("Respuesta:", response.content.get('message', 'Error al procesar la solicitud.'))
        elif opcion == "2":
            promociones = response.content.get('promociones', [])
            if promociones:
                print("\n--- Promociones Disponibles ---")
                for p in promociones:
                    print(f"Promoción: {p['promocion']}, Cantidad: {p['cantidad']}, Precio: {p['precio']}")
            else:
                print("No hay promociones registradas.")


# Función para gestionar mesas
def gestionar_mesas(c: client.Client, user_fonda_id):
    while True:
        print("\n--- Gestión de Mesas ---")
        print("1. Ver mesas ocupadas")
        print("2. Liberar una mesa (cobrar cuenta)")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Ver mesas ocupadas
            request_content = {'action': 'view_tables', 'fonda_id': user_fonda_id}
            request = client.Request('mesas', request_content)
            c.send(request)

            response = c.receive()
            mesas = response.content.get('mesas', [])
            if mesas:
                print("\n--- Mesas Ocupadas ---")
                for m in mesas:
                    print(f"Número: {m['numero']}, Reservado por: {m['reservado_por']}")
            else:
                print(response.content.get('message', 'No hay mesas ocupadas.'))
        elif opcion == "2":
            # Liberar mesa
            request_content = {'action': 'view_tables', 'fonda_id': user_fonda_id}
            request = client.Request('mesas', request_content)
            c.send(request)

            response = c.receive()
            mesas = response.content.get('mesas', [])
            if not mesas:
                print("No hay mesas ocupadas para liberar.")
                continue

            print("\n--- Mesas Ocupadas ---")
            for m in mesas:
                print(f"Número: {m['numero']}, Reservado por: {m['reservado_por']}")

            mesa_numero = int(input("\nNúmero de la mesa a liberar: "))
            consumo = []
            while True:
                producto = input("Producto consumido (o 'fin' para terminar): ")
                if producto.lower() == 'fin':
                    break
                cantidad = int(input(f"Cantidad de {producto}: "))
                consumo.append({'producto': producto, 'cantidad': cantidad})

            metodo_pago = input("Método de pago (efectivo, débito, crédito): ").strip().lower()

            request_content = {
                'action': 'release_table',
                'mesa_numero': mesa_numero,
                'fonda_id': user_fonda_id,
                'consumo': consumo,
                'metodo_pago': metodo_pago
            }
            request = client.Request('mesas', request_content)
            c.send(request)

            response = c.receive()
            print("Respuesta:", response.content.get('message', 'Error al procesar la solicitud.'))
        elif opcion == "3":
            # Salir al menú principal
            break
        else:
            print("Opción no válida.")




# Función para gestionar opiniones
def gestionar_opiniones(c: client.Client):
    while True:
        print("\n--- Gestión de Opiniones ---")
        print("1. Ver opiniones")
        print("2. Responder opinión")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            request_content = {'action': 'view_opinions'}
            request = client.Request('opin', request_content)
            c.send(request)
        elif opcion == "2":
            opinion_id = int(input("ID de la opinión: "))
            respuesta = input("Escriba su respuesta: ")
            request_content = {'action': 'respond_opinion', 'opinion_id': opinion_id, 'respuesta': respuesta}
            request = client.Request('opin', request_content)
            c.send(request)
        elif opcion == "3":
            break
        else:
            print("Opción no válida.")

        response = c.receive()
        print("Respuesta:", response.content.get('message', 'Error al procesar la solicitud.'))

# Función para ver estadísticas
def ver_estadisticas(c: client.Client):
    while True:
        print("\n--- Ver Estadísticas ---")
        print("1. Ventas totales")
        print("2. Productos más vendidos")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            rango = input("Ingrese el rango ('diario' o 'semanal'): ")
            request_content = {'action': 'view_sales', 'rango': rango}
            request = client.Request('stats', request_content)
            c.send(request)
        elif opcion == "2":
            request_content = {'action': 'top_products'}
            request = client.Request('stats', request_content)
            c.send(request)
        elif opcion == "3":
            break
        else:
            print("Opción no válida.")

        response = c.receive()
        if opcion == "1":
            print("Ventas totales:", response.content.get('ventas', 'Sin datos.'))
        elif opcion == "2":
            productos = response.content.get('productos', [])
            print("Productos más vendidos:")
            for p in productos:
                print(f"{p['producto']}: {p['cantidad']} unidades")

# Menú principal del operador
def menu_operador(c: client.Client, user_fonda_id):
    while True:
        print("\n--- Menú de Operador ---")
        print("1. Gestionar inventario")
        print("2. Gestionar promociones")
        print("3. Gestionar mesas")
        print("4. Gestionar opiniones")
        print("5. Ver estadísticas")
        print("6. Cerrar sesión")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            gestionar_inventario(c, user_fonda_id)
        elif opcion == "2":
            gestionar_promociones(c, user_fonda_id)
        elif opcion == "3":
            gestionar_mesas(c, user_fonda_id)
        elif opcion == "4":
            gestionar_opiniones(c, user_fonda_id)
        elif opcion == "5":
            ver_estadisticas(c, user_fonda_id)
        elif opcion == "6":
            print("Cerrando sesión...")
            break
        else:
            print("Opción no válida.")
def menu_normal():
    c = client.Client()  # Conectar al bus
    while True:
        print("\n--- Menú Principal ---")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_usuario(c)
        elif opcion == "2":
            iniciar_sesion(c)
        elif opcion == "3":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")
    c.close()

if __name__ == "__main__":
    menu_normal()
