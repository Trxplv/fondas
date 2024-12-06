import service
import sqlite3
from datetime import datetime, timedelta

# Crear una fonda
def crear_fonda(content):
    try:
        conn = sqlite3.connect("fondas.db")
        cursor = conn.cursor()

        nombre = content['nombre']
        mesas = content['mesas']

        # Verificar si la fonda ya existe
        cursor.execute("SELECT COUNT(*) FROM fondas WHERE nombre = ?", (nombre,))
        if cursor.fetchone()[0] > 0:
            return {'status': 'failure', 'message': 'La fonda ya existe.'}

        # Crear la fonda
        cursor.execute("INSERT INTO fondas (nombre, mesas) VALUES (?, ?)", (nombre, mesas))
        conn.commit()

        return {'status': 'success', 'message': 'Fonda creada exitosamente.'}
    except Exception as e:
        return {'status': 'failure', 'message': str(e)}
    finally:
        conn.close()

# Listar fondas
def listar_fondas(content):
    try:
        conn = sqlite3.connect("fondas.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id, nombre, mesas FROM fondas")
        fondas = cursor.fetchall()

        if fondas:
            return {'status': 'success', 'fondas': [{'id': f[0], 'nombre': f[1], 'mesas': f[2]} for f in fondas]}
        else:
            return {'status': 'success', 'fondas': []}
    except Exception as e:
        return {'status': 'failure', 'message': str(e)}
    finally:
        conn.close()


# Eliminar fonda y sus operadores
def eliminar_fonda(content):
    try:
        conn = sqlite3.connect("fondas.db")
        cursor = conn.cursor()

        fonda_id = content['fonda_id']

        # Eliminar usuarios asociados a la fonda
        cursor.execute("DELETE FROM usuarios WHERE rol = 'operador' AND username IN (SELECT username FROM usuarios WHERE rol = 'operador')")
        # Eliminar la fonda
        cursor.execute("DELETE FROM fondas WHERE id = ?", (fonda_id,))
        conn.commit()

        if cursor.rowcount > 0:
            return {'status': 'success', 'message': 'Fonda eliminada exitosamente.'}
        else:
            return {'status': 'failure', 'message': 'Fonda no encontrada.'}
    except Exception as e:
        return {'status': 'failure', 'message': str(e)}
    finally:
        conn.close()

# Ver ventas totales
def ver_ventas(content):
    try:
        conn = sqlite3.connect("fondas.db")
        cursor = conn.cursor()

        fonda_id = content['fonda_id']
        rango = content['rango']  # 'diario' o 'semanal'

        # Verificar si la fonda existe
        cursor.execute("SELECT COUNT(*) FROM fondas WHERE id = ?", (fonda_id,))
        if cursor.fetchone()[0] == 0:
            return {'status': 'failure', 'message': 'La fonda no existe.'}

        # Determinar el rango de fechas
        hoy = datetime.now()
        if rango == 'diario':
            fecha_inicio = hoy
        elif rango == 'semanal':
            fecha_inicio = hoy - timedelta(days=7)

        # Calcular las ventas
        cursor.execute("""
        SELECT SUM(total) FROM ventas
        WHERE fonda_id = ? AND fecha >= ?
        """, (fonda_id, fecha_inicio.strftime('%Y-%m-%d')))
        total = cursor.fetchone()[0] or 0

        return {'status': 'success', 'total': total}
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
        if action == 'create':
            response_content = crear_fonda(request.content)
        elif action == 'list':
            response_content = listar_fondas(request.content)
        elif action == 'delete_fonda':
            response_content = eliminar_fonda(request.content)
        elif action == 'view_sales':
            response_content = ver_ventas(request.content)
        else:
            response_content = {'status': 'failure', 'message': 'Acción no válida'}

        print("Respuesta a enviar:", response_content)  # Depuración
        response = service.Response(s.name, response_content)
        s.send(response)
    s.close()

if __name__ == "__main__":
    s = service.Service('fonda')  # Nombre del servicio
    run_service(s)
