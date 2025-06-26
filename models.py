from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Datenbank-Objekt initialisieren
db = SQLAlchemy()

# Modell: Speise (Essen/Getränk)
class Speise(db.Model):
    __tablename__ = 'speisen'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    preis = db.Column(db.Float, nullable=False)
    kategorie = db.Column(db.String(20), nullable=False)  # z. B. 'Essen' oder 'Getränk'

    def __repr__(self):
        return f"<Speise {self.name} ({self.kategorie})>"


# Modell: Bestellung
class Bestellung(db.Model):
    __tablename__ = 'bestellungen'
    id = db.Column(db.Integer, primary_key=True)
    tisch_nr = db.Column(db.Integer, nullable=False)
    speisen = db.Column(db.String(255), nullable=False)  # CSV-Liste der Speisen/Getränke
    zeitpunkt = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Bestellung Tisch {self.tisch_nr} – {self.speisen}>"
