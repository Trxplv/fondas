import service
import sqlite3

# Ver opiniones de una fonda
def ver_opiniones(content):
    try:
        conn = sqlite3.connect("fondas.db")
        cursor = conn.cursor()

        user_fonda_id = content['user_fonda_id']  # Fonda asociada al operador

        cursor.execute("""
        SELECT o.id, u.nombre || ' ' || u.apellido AS cliente, o.comentario, o.estrellas, o.respuesta
        FROM opiniones o
        JOIN usuarios u ON o.usuario_id = u.id
        WHERE o.fonda_id = ?
        """, (user_fonda_id,))
        opiniones = cursor.fetchall()

        if opiniones:
            return {'status': 'success', 'opiniones': [
                {'id': o[0], 'cliente': o[1], 'comentario': o[2], 'estrellas': o[3], 'respuesta': o[4]} for o in opiniones
            ]}
        else:
            return {'status': 'success', 'opiniones': []}
    except Exception as e:
        return {'status': 'failure', 'message': str(e)}
    finally:
        conn.close()

# Responder una opinión
def responder_opinion(content):
    try:
        conn = sqlite3.connect("fondas.db")
        cursor = conn.cursor()

        opinion_id = content['opinion_id']
        respuesta = content['respuesta']

        # Actualizar respuesta de la opinión
        cursor.execute("""
        UPDATE opiniones
        SET respuesta = ?
        WHERE id = ?
        """, (respuesta, opinion_id))
        conn.commit()

        if cursor.rowcount > 0:
            return {'status': 'success', 'message': 'Respuesta enviada exitosamente.'}
        else:
            return {'status': 'failure', 'message': 'Opinión no encontrada.'}
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
        if action == 'view_opinions':
            response_content = ver_opiniones(request.content)
        elif action == 'respond_opinion':
            response_content = responder_opinion(request.content)
        else:
            response_content = {'status': 'failure', 'message': 'Acción no válida'}

        print("Respuesta a enviar:", response_content)  # Depuración
        response = service.Response(s.name, response_content)
        s.send(response)
    s.close()

if __name__ == "__main__":
    s = service.Service('opins')  # Nombre del servicio
    run_service(s)
