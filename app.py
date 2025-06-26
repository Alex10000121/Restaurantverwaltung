import os
from flask import Flask, render_template, request, redirect, url_for
from models import db, Speise, Bestellung

# Absoluter Pfad zur Datenbank
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
    speisen = Speise.query.filter_by(kategorie="Essen").all()
    getraenke = Speise.query.filter_by(kategorie="Getränk").all()
    return render_template('speisekarte.html', speisen=speisen, getraenke=getraenke)


# Verarbeitung der Bestellung
@app.route('/bestellen', methods=['POST'])
def bestellen():
    bestell_ids = []

    for key, value in request.form.items():
        if value.isdigit() and int(value) > 0:
            if key.startswith("speise_") or key.startswith("getraenk_"):
                artikel_id = key.split("_")[1]
                bestell_ids.extend([artikel_id] * int(value))

    if not bestell_ids:
        # Kein Artikel ausgewählt
        speisen = Speise.query.filter_by(kategorie="Essen").all()
        getraenke = Speise.query.filter_by(kategorie="Getränk").all()
        fehler = "Bitte wählen Sie mindestens ein Produkt aus."
        return render_template('speisekarte.html', speisen=speisen, getraenke=getraenke, fehler=fehler)

    tisch_nr = request.form.get('tisch', 1)
    neue_bestellung = Bestellung(tisch_nr=tisch_nr, speisen=",".join(bestell_ids))
    db.session.add(neue_bestellung)
    db.session.commit()
    return redirect(url_for('danke'))



# Bestätigungsseite nach erfolgreicher Bestellung
@app.route('/danke')
def danke():
    bestellung = Bestellung.query.order_by(Bestellung.id.desc()).first()
    speisen_ids = bestellung.speisen.split(',') if bestellung else []

    from collections import Counter
    zähler = Counter(speisen_ids)

    speisen_liste = []
    getraenke_liste = []
    summe = 0.0

    for id_str, menge in zähler.items():
        speise = Speise.query.get(int(id_str))
        if speise:
            gesamt = speise.preis * menge
            summe += gesamt
            eintrag = {
                'name': speise.name,
                'preis': speise.preis,
                'menge': menge
            }
            if speise.kategorie == "Essen":
                speisen_liste.append(eintrag)
            elif speise.kategorie == "Getränk":
                getraenke_liste.append(eintrag)

    return render_template('danke.html',
                           speisen=speisen_liste,
                           getraenke=getraenke_liste,
                           summe=summe)


# Initialisierung und Start des Servers
if __name__ == '__main__':
    with app.app_context():
        # Datenbank erstellen (falls nicht vorhanden)
        db.create_all()

        # Nur beim ersten Start: Beispieldaten in Speisekarte einfügen
        if not Speise.query.first():
            db.session.add_all([
                Speise(name="Pizza Margherita", preis=12.50, kategorie="Essen"),
                Speise(name="Spaghetti Carbonara", preis=14.00, kategorie="Essen"),
                Speise(name="Gemischter Salat", preis=8.50, kategorie="Essen"),
                Speise(name="Lasagne Bolognese", preis=15.00, kategorie="Essen"),
                Speise(name="Ravioli mit Ricotta", preis=13.00, kategorie="Essen"),
                Speise(name="Panna Cotta", preis=6.50, kategorie="Essen"),
                Speise(name="Mineralwasser 0.5L", preis=3.00, kategorie="Getränk"),
                Speise(name="Cola 0.5L", preis=3.50, kategorie="Getränk"),
                Speise(name="Apfelschorle 0.5L", preis=3.50, kategorie="Getränk"),
                Speise(name="Espresso", preis=2.50, kategorie="Getränk"),
                Speise(name="Cappuccino", preis=4.00, kategorie="Getränk")
            ])
            db.session.commit()

    # Anwendung starten (lokal)
    app.run(debug=True)
