import service
import sqlite3

# Ver mesas ocupadas
def ver_mesas_ocupadas(content):
    try:
        conn = sqlite3.connect("fondas.db")
        cursor = conn.cursor()

        fonda_id = content['fonda_id']

        # Obtener mesas reservadas
        cursor.execute("""
        SELECT numero, reservado_por
        FROM mesas
        WHERE fonda_id = ? AND estado = 'reservada'
        """, (fonda_id,))
        mesas = cursor.fetchall()

        if mesas:
            return {
                'status': 'success',
                'mesas': [{'numero': m[0], 'reservado_por': m[1]} for m in mesas]
            }
        else:
            return {'status': 'success', 'mesas': [], 'message': 'No hay mesas ocupadas.'}
    except Exception as e:
        return {'status': 'failure', 'message': str(e)}
    finally:
        conn.close()

# Liberar una mesa y registrar el consumo
def liberar_mesa(content):
    try:
        conn = sqlite3.connect("fondas.db")
        cursor = conn.cursor()

        mesa_numero = content['mesa_numero']
        fonda_id = content['fonda_id']
        consumo = content['consumo']  # Lista de productos y cantidades consumidas
        metodo_pago = content['metodo_pago']

        # Verificar que la mesa está ocupada
        cursor.execute("""
        SELECT estado, reservado_por FROM mesas
        WHERE fonda_id = ? AND numero = ?
        """, (fonda_id, mesa_numero))
        mesa = cursor.fetchone()

        if not mesa:
            return {'status': 'failure', 'message': 'La mesa no existe.'}

        if mesa[0] != 'reservada':
            return {'status': 'failure', 'message': 'La mesa no está reservada.'}

        # Actualizar el inventario en base al consumo
        for item in consumo:
            producto = item['producto']
            cantidad = item['cantidad']

            # Verificar si el producto existe y tiene suficiente cantidad
            cursor.execute("""
            SELECT cantidad FROM inventario
            WHERE fonda_id = ? AND producto = ?
            """, (fonda_id, producto))
            inventario = cursor.fetchone()

            if not inventario or inventario[0] < cantidad:
                return {'status': 'failure', 'message': f'No hay suficiente cantidad de {producto}.'}

            # Reducir cantidad en el inventario
            cursor.execute("""
            UPDATE inventario
            SET cantidad = cantidad - ?
            WHERE fonda_id = ? AND producto = ?
            """, (cantidad, fonda_id, producto))

        # Liberar la mesa
        cursor.execute("""
        UPDATE mesas
        SET estado = 'disponible', reservado_por = NULL
        WHERE fonda_id = ? AND numero = ?
        """, (fonda_id, mesa_numero))

        conn.commit()

        return {
            'status': 'success',
            'message': f'Mesa {mesa_numero} liberada exitosamente. Método de pago: {metodo_pago.capitalize()}'
        }
    except Exception as e:
        return {'status': 'failure', 'message': str(e)}
    finally:
        conn.close()

# Servicio principal
def run_service(s: service.Service):
    s.sinit()  # Inicializar el servicio con el bus
    while True:
        request = s.receive()  # Recibir solicitudes del bus
        print("Solicitud recibida:", request.content)  # Depuración

        action = request.content.get('action')
        if action == 'view_tables':
            response_content = ver_mesas_ocupadas(request.content)
        elif action == 'release_table':
            response_content = liberar_mesa(request.content)
        else:
            response_content = {'status': 'failure', 'message': 'Acción no válida'}

        print("Respuesta a enviar:", response_content)  # Depuración
        response = service.Response(s.name, response_content)
        s.send(response)
    s.close()

if __name__ == "__main__":
    s = service.Service('mesas')  # Nombre del servicio
    run_service(s)
