import psycopg2

# Configuración de la conexión
conn_params = {
    "user": "postgres.gwjbtxqgdottlkficmic",
    "password": "C0nr@Proj3ct2025",  # Reemplázalo con tu contraseña real
    "host": "aws-0-us-east-1.pooler.supabase.com",
    "port": "6543",
    "dbname": "postgres"
}

query = 'SELECT "idCuentas", "nombreCuenta" FROM cuentas'

def ejecutar_consulta(query):
 
    try:
        # Conectarse a la base de datos
        conn = psycopg2.connect(**conn_params)
        print("Conexión exitosa")

        # Crear un cursor para ejecutar consultas
        cur = conn.cursor()

        # Ejecutar la consulta
        cur.execute(query)

        # Obtener los resultados
        resultados = cur.fetchall()

        # Cerrar cursor y conexión
        cur.close()
        conn.close()

        return print(resultados)

    except Exception as e:
        print("Error al conectar o ejecutar la consulta:", e)
        return None

ejecutar_consulta(query)