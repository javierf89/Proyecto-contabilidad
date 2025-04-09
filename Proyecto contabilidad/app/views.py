from flask import Flask, request, jsonify
from app.models import db, AsientoContable
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)

    @app.route('/asientos', methods=['POST'])
    def agregar_asiento():
        data = request.get_json()

        try:
            fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
            cuenta = data['cuenta']
            debe = data['debe']
            haber = data['haber']
            descripcion = data.get('descripcion', '')

            nuevo_asiento = AsientoContable(fecha, cuenta, debe, haber, descripcion)
            db.session.add(nuevo_asiento)
            db.session.commit()

            return jsonify({'message': 'Asiento contable agregado exitosamente'}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'message': str(e)}), 400

    @app.route('/asientos', methods=['GET'])
    def obtener_asientos():
        asientos = AsientoContable.query.all()
        resultado = [
            {
                'id': asiento.id,
                'fecha': asiento.fecha.strftime('%Y-%m-%d'),
                'cuenta': asiento.cuenta,
                'debe': asiento.debe,
                'haber': asiento.haber,
                'descripcion': asiento.descripcion
            }
            for asiento in asientos
        ]
        return jsonify(resultado)

    return app
