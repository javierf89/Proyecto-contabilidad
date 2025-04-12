import psycopg2
from datetime import datetime

# Parámetros de conexión
conn_params = {
    "user": "postgres.gwjbtxqgdottlkficmic",
    "password": "C0nr@Proj3ct2025",
    "host": "aws-0-us-east-1.pooler.supabase.com",
    "port": "6543",
    "dbname": "postgres"
}

# Nuevos datos a insertar
cuentas_data_3 = [
    ('2.2', 'Pasivo No Corriente (deudas mayor a un año) (a largo plazo)'),
    ('2.2.1', 'Cuentas y documentos por pagar'),
    ('2.2.1.1', 'Acreedores varios'),
    ('2.2.1.2', 'Documentos por pagar'),
    ('2.2.2', 'Préstamos'),
    ('2.2.2.1', 'Préstamos bancarios'),
    ('2.2.2.2', 'Préstamos hipotecarios'),
    ('2.2.3', 'Provisiones'),
    ('2.2.3.1', 'Provisiones para compensaciones a empleados'),
    ('2.2.3.2', 'Provisiones para cubrir garantías a clientes'),
    ('2.2.3.3', 'Provisiones para cubrir reclamos legales'),
    ('2.2.4', 'Cobros anticipados'),
    ('2.2.4.1', 'Rentas cobradas por anticipado'),
    ('2.2.4.2', 'Intereses cobrados por anticipado'),
    ('2.2.4.3', 'Servicios cobrados por anticipado'),
    ('3', 'Patrimonio Neto'),
    ('3.1', 'Comerciante individual'),
    ('3.1.1', 'Capital'),
    ('3.1.2', 'Resultados acumulados'),
    ('3.1.2.1', 'Utilidades o pérdidas de años anteriores (del 2023 hacia atrás)'),
    ('3.1.2.2', 'Utilidad o pérdida neta del período (del 2024)'),
    ('3.2', 'Empresa jurídica'),
    ('3.2.1', 'Capital social (aportaciones de los socios)'),
    ('3.2.2', 'Reservas'),
    ('3.2.2.1', 'Reserva legal (5% de la utilidad lo establece el código de comercio)'),
    ('3.2.2.2', 'Reservas estatutarias (si lo dice en la reserva de constitución) COMPLM'),
    ('3.2.2.3', 'Reserva voluntaria (si quieren o no hacerla) COMPLEM'),
    ('3.2.3', 'Resultados acumulados'),
    ('3.2.3.1', 'Utilidad o pérdida de años anteriores o utilidades no distribuidas'),
    ('3.2.3.2', 'Utilidad o pérdida neta del ejercicio')
]

# Función para insertar los datos
def insertar_cuentas_3():
    try:
        conn = psycopg2.connect(**conn_params)
        print("Conexión exitosa")
        cur = conn.cursor()

        # Iterar sobre las cuentas y realizar las inserciones
        for cuenta in cuentas_data_3:
            query = 'INSERT INTO cuentas ("idCuentas", "nombreCuenta", "tipoCuenta") VALUES (%s, %s, %s);'
            # Asumimos que el tipo de cuenta es un número o ID predefinido, como 1 para "Activo"
            tipo_cuenta = 1  # Aquí deberías cambiar el valor según el tipo correspondiente
            cur.execute(query, (cuenta[0], cuenta[1], tipo_cuenta))

        # Confirmar los cambios
        conn.commit()
        print("Datos insertados correctamente")
        cur.close()
        conn.close()
    except Exception as e:
        print("Error al insertar:", e)

# Ejecutar la inserción
insertar_cuentas_3()
