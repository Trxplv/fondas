import service
import sqlite3
from datetime import datetime, timedelta

# Ver ventas totales diarias y semanales
def ver_ventas(content):
    try:
        conn = sqlite3.connect("fondas.db")
        cursor = conn.cursor()

        user_fonda_id = content['user_fonda_id']  # Fonda asociada al operador
        rango = content['rango']  # 'diario' o 'semanal'

        # Determinar el rango de fechas
        hoy = datetime.now()
        if rango == 'diario':
            fecha_inicio = hoy.strftime('%Y-%m-%d')
        elif rango == 'semanal':
            fecha_inicio = (hoy - timedelta(days=7)).strftime('%Y-%m-%d')
        else:
            return {'status': 'failure', 'message': 'Rango inválido.'}

        # Consultar ventas
        cursor.execute("""
        SELECT SUM(total) FROM ventas
        WHERE fonda_id = ? AND fecha >= ?
        """, (user_fonda_id, fecha_inicio))
        total_ventas = cursor.fetchone()[0] or 0

        return {'status': 'success', 'ventas': total_ventas}
    except Exception as e:
        return {'status': 'failure', 'message': str(e)}
    finally:
        conn.close()

# Consultar productos más vendidos
def productos_mas_vendidos(content):
    try:
        conn = sqlite3.connect("fondas.db")
        cursor = conn.cursor()

        user_fonda_id = content['user_fonda_id']  # Fonda asociada al operador

        # Consultar los productos más vendidos
        cursor.execute("""
        SELECT producto, SUM(cantidad) AS total_cantidad
        FROM inventario
        WHERE fonda_id = ?
        GROUP BY producto
        ORDER BY total_cantidad DESC
        LIMIT 5
        """, (user_fonda_id,))
        productos = cursor.fetchall()

        if productos:
            return {'status': 'success', 'productos': [
                {'producto': p[0], 'cantidad': p[1]} for p in productos
            ]}
        else:
            return {'status': 'success', 'productos': []}
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
        if action == 'view_sales':
            response_content = ver_ventas(request.content)
        elif action == 'top_products':
            response_content = productos_mas_vendidos(request.content)
        else:
            response_content = {'status': 'failure', 'message': 'Acción no válida'}

        print("Respuesta a enviar:", response_content)  # Depuración
        response = service.Response(s.name, response_content)
        s.send(response)
    s.close()

if __name__ == "__main__":
    s = service.Service('stats')  # Nombre del servicio
    run_service(s)
