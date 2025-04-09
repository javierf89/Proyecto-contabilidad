from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AsientoContable(db.Model):
    __tablename__ = 'asientos_contables'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    cuenta = db.Column(db.String(255), nullable=False)
    debe = db.Column(db.Float, nullable=False)
    haber = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(255))

    def __init__(self, fecha, cuenta, debe, haber, descripcion):
        self.fecha = fecha
        self.cuenta = cuenta
        self.debe = debe
        self.haber = haber
        self.descripcion = descripcion

    def __repr__(self):
        return f"<AsientoContable {self.id}>"
