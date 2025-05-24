from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialisierung des SQLAlchemy-Objekts (wird in app.py eingebunden)
db = SQLAlchemy()

# ──────────────────────────────────────────────
# Modell: Speise (Eintrag in der digitalen Speisekarte)
# ──────────────────────────────────────────────
class Speise(db.Model):
    __tablename__ = 'speisen'

    id = db.Column(db.Integer, primary_key=True)      # Eindeutige ID
    name = db.Column(db.String(100), nullable=False)  # Name des Gerichts
    preis = db.Column(db.Float, nullable=False)       # Preis in CHF

    def __repr__(self):
        return f"<Speise {self.name}>"

# ──────────────────────────────────────────────
# Modell: Bestellung (Eintrag bei abgeschickter Bestellung)
# ──────────────────────────────────────────────
class Bestellung(db.Model):
    __tablename__ = 'bestellungen'

    id = db.Column(db.Integer, primary_key=True)        # Eindeutige ID
    tisch_nr = db.Column(db.Integer, nullable=False)    # Tischnummer
    speisen = db.Column(db.String(255), nullable=False) # CSV-Liste z. B. "1,3,3"
    zeitpunkt = db.Column(db.DateTime, default=datetime.now)  # Zeitstempel

    def __repr__(self):
        return f"<Bestellung Tisch {self.tisch_nr} – {self.speisen}>"
