from flask import Flask, request, render_template, jsonify, session, Response
from flask_session import Session
from datetime import datetime
import pdfkit
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
import conexion
CUENTAS = {}

def cuenta():
    try:
        conn = conexion.psycopg2.connect(**conexion.conn_params)
        cur = conn.cursor()
        cur.execute('SELECT "idCuentas", "nombreCuenta" FROM cuentas')
        resultados = cur.fetchall()
        cur.close()
        conn.close()

        # Llenar el diccionario global CUENTAS
        global CUENTAS
        CUENTAS = {str(idCuenta): {'nombre': nombreCuenta} for idCuenta, nombreCuenta in resultados}
        print("CUENTAS cargadas:", CUENTAS)

    except Exception as e:
        print("Error al cargar cuentas:", e)

# Llamar la función para cargar los datos al iniciar
cuenta()

    
ASIENTOS = []

# Configuración explícita de wkhtmltopdf (ajusta esta ruta según tu instalación)
config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

@app.route('/')
def index():
    session['asiento'] = []
    return render_template('index.html', asientos=ASIENTOS)

@app.route('/buscar_cuenta', methods=['POST'])
def buscar_cuenta():
    codigo = request.form.get('codigo')
    if codigo in CUENTAS:
        cuenta = CUENTAS[codigo]
        return jsonify({
            'success': True,
            'codigo': codigo,
            'nombre': cuenta['nombre']
        })
    return jsonify({'success': False, 'mensaje': 'Cuenta no encontrada'})

@app.route('/agregar_linea', methods=['POST'])
def agregar_linea():
    codigo = request.form.get('codigo')
    monto = float(request.form.get('monto'))
    naturaleza = request.form.get('naturaleza')
    descripcion_linea = request.form.get('descripcion_linea')

    if codigo in CUENTAS:
        cuenta = CUENTAS[codigo]
        linea = {
            'codigo': codigo,
            'nombre': cuenta['nombre'],
            'naturaleza': naturaleza,
            'monto': monto,
            'descripcion_linea': descripcion_linea
        }
        if 'asiento' not in session:
            session['asiento'] = []
        session['asiento'].append(linea)
        session.modified = True
        return jsonify({'success': True, 'linea': linea})
    return jsonify({'success': False, 'mensaje': 'Error al agregar línea'})

@app.route('/finalizar_asiento', methods=['POST'])
def finalizar_asiento():
    descripcion_general = request.form.get('descripcion_general')
    fecha = request.form.get('fecha')

    if 'asiento' not in session or not session['asiento']:
        return jsonify({'success': False, 'mensaje': 'No hay líneas en el asiento'})

    for asiento_existente in ASIENTOS:
        if asiento_existente['fecha'] == fecha:
            return jsonify({'success': False, 'mensaje': f'Ya existe un asiento con la fecha {fecha}'})

    total_debe = sum(linea['monto'] for linea in session['asiento'] if linea['naturaleza'] == 'Debe')
    total_haber = sum(linea['monto'] for linea in session['asiento'] if linea['naturaleza'] == 'Haber')

    if total_debe != total_haber:
        return jsonify({'success': False, 'mensaje': f'El asiento no cuadra: Debe (L {total_debe:,.2f}) ≠ Haber (L {total_haber:,.2f})'})

    asiento_completo = {
        'fecha': fecha,
        'descripcion_general': descripcion_general,
        'lineas': session['asiento'],
        'total_debe': total_debe,
        'total_haber': total_haber
    }

    ASIENTOS.append(asiento_completo)
    session['asiento'] = []
    session.modified = True

    return jsonify({'success': True, 'asiento': asiento_completo})

@app.route('/generar_pdf', methods=['POST'])
def generar_pdf():
    nombre_empresa = request.form.get('nombre_empresa')
    if not nombre_empresa:
        return jsonify({'success': False, 'mensaje': 'Debe ingresar el nombre de la empresa'})

    # Plantilla HTML para el PDF
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>- {nombre_empresa}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ text-align: center; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
            th {{ background-color: #e9ecef; }}
            .fecha {{ text-align: center; font-weight: bold; }}
            .totales {{ font-weight: bold; }}
            .descripcion-general {{ font-style: italic; background-color: #f1f3f5; }}
            .descripcion-linea {{ font-size: 0.9em; color: #6c757d; }}
        </style>
    </head>
    <body>
        <h1>Historial de Asientos - {nombre_empresa}</h1>
        <table>
            <thead>
                <tr>
                    <th>Fecha</th>
                    <th>Código</th>
                    <th>Nombre</th>
                    <th>Debe</th>
                    <th>Haber</th>
                </tr>
            </thead>
            <tbody>
    """

    for asiento in ASIENTOS:
        num_lineas = len(asiento['lineas'])
        html += f"""
            <tr>
                <td rowspan="{num_lineas + 2}" class="fecha">{asiento['fecha']}</td>
                <td colspan="4">Asiento Registrado</td>
            </tr>
        """
        for linea in asiento['lineas']:
            debe = f"{linea['monto']:,.2f}" if linea['naturaleza'] == 'Debe' else ''
            haber = f"{linea['monto']:,.2f}" if linea['naturaleza'] == 'Haber' else ''
            html += f"""
            <tr>
                <td>{linea['codigo']}</td>
                <td>{linea['nombre']}<br><span class="descripcion-linea">{linea['descripcion_linea'] or ''}</span></td>
                <td>{debe}</td>
                <td>{haber}</td>
            </tr>
            """
        html += f"""
            <tr class="totales">
                <td>Totales</td>
                <td></td>
                <td>{asiento['total_debe']:,.2f}</td>
                <td>{asiento['total_haber']:,.2f}</td>
            </tr>
            <tr class="descripcion-general">
                <td colspan="5">Descripción General: {asiento['descripcion_general']}</td>
            </tr>
        """

    html += """
            </tbody>
        </table>
    </body>
    </html>
    """

    # Generar el PDF usando la configuración explícita
    try:
        pdf = pdfkit.from_string(html, False, configuration=config)
        return Response(pdf, mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=Historial_Asientos_{nombre_empresa}.pdf'})
    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error al generar el PDF: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)