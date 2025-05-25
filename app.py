import os
from flask import Flask, render_template, request, redirect, url_for
from models import db, Speise, Bestellung

# Absoluter Pfad zur Datenbank (lokal, wie in der Arbeit gefordert)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)
DB_PATH = os.path.join(BASE_DIR, "database/restaurant.db")

# Flask-Anwendung konfigurieren
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Weiterleitung auf /speisekarte
@app.route('/')
def index():
    return redirect(url_for('speisekarte'))

# Anzeige der Speisekarte mit Formular für Bestellung
@app.route('/speisekarte')
def speisekarte():
    speisen = Speise.query.all()
    endbetrag = sum(s.preis for s in speisen)
    return render_template('speisekarte.html', speisen=speisen, endbetrag=endbetrag)

# Verarbeitung der Bestellung (POST aus Formular)
@app.route('/bestellen', methods=['POST'])
def bestellen():
    speisen_ids = []
    for key, value in request.form.items():
        if key.startswith("speise_") and value.isdigit() and int(value) > 0:
            speisen_id = key.split("_")[1]
            speisen_ids.extend([speisen_id] * int(value))

    tisch_nr = request.form.get('tisch', 1)
    speisen_csv = ','.join(speisen_ids)

    neue_bestellung = Bestellung(tisch_nr=tisch_nr, speisen=speisen_csv)
    db.session.add(neue_bestellung)
    db.session.commit()
    return redirect(url_for('danke'))

# Bestätigungsseite nach erfolgreicher Bestellung
@app.route('/danke')
def danke():
    bestellung = Bestellung.query.order_by(Bestellung.id.desc()).first()
    speisen_ids = bestellung.speisen.split(',') if bestellung else []

    speisen_liste = []
    summe = 0.0
    if speisen_ids:
        from collections import Counter
        zähler = Counter(speisen_ids)
        for speise_id, menge in zähler.items():
            speise = Speise.query.get(int(speise_id))
            if speise:
                gesamt = speise.preis * menge
                summe += gesamt
                speisen_liste.append({
                    'name': speise.name,
                    'preis': speise.preis,
                    'menge': menge
                })

    return render_template('danke.html', bestellung=bestellung, speisen=speisen_liste, summe=summe)


# Initialisierung & Start des Servers
if __name__ == '__main__':
    with app.app_context():
        # Datenbank erstellen (falls nicht vorhanden)
        db.create_all()

        # Nur beim ersten Start: Beispieldaten in Speisekarte einfügen
        if not Speise.query.first():
            db.session.add_all([
                Speise(name="Pizza Margherita", preis=12.50),
                Speise(name="Spaghetti Carbonara", preis=14.00),
                Speise(name="Gemischter Salat", preis=8.50)
            ])
            db.session.commit()

    # Anwendung starten (lokal)
    app.run(debug=True)
