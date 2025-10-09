import os
import urllib.parse
import requests
import re
from pymongo import MongoClient
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from calcolatore_iva import calcola_scontrino
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId

#Vari dati per la connessione al db / API per ip
load_dotenv()
username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")
ipinfo_token = os.getenv("IPINFO_TOKEN")

if not username or not password:
    raise ValueError("Le variabili MONGO_USER e MONGO_PASS devono essere definite nel file .env")

encoded_password = urllib.parse.quote_plus(password)
uri = f"mongodb+srv://{username}:{encoded_password}@progetto1.baefqmn.mongodb.net/?retryWrites=true&w=majority&appName=Progetto1"
client = MongoClient(uri)
db = client['databaseProdotti']
collection = db['prodotti']
utenti_collection = db['utenti']
ordini_collection = db['ordini']

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key-default")
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


@app.route('/api/registrazione', methods=['POST'])
def registrazione():
    """Registrazione dell'utente"""
    data = request.get_json()
    required_fields = ['email', 'password', 'nome', 'cognome']
    
    if not all(data.get(field) for field in required_fields):
        return jsonify({"msg": "Tutti i campi sono richiesti"}), 400
        
    if utenti_collection.find_one({'email': data['email']}):
        return jsonify({"msg": "Utente già esistente"}), 409

    utenti_collection.insert_one({
        'email': data['email'],
        'password': generate_password_hash(data['password']),
        'nome': data['nome'],
        'cognome': data['cognome'],
        'indirizzo': '',
        'citta': '',
        'carrello': [],
        'preferiti': []
    })
    
    return jsonify({"msg": "Utente registrato con successo"}), 201


@app.route('/api/profilo', methods=['GET', 'POST'])
@jwt_required()
def profilo_utente():
    """Ottiene i dati dell'utente / modifica i dati dell'utente """
    current_user_email = get_jwt_identity()

    if request.method == 'POST':
        data = request.get_json()
        update_fields = {
            'nome': data.get('nome'), 'cognome': data.get('cognome'), 'telefono': data.get('telefono'),
            'indirizzo': data.get('indirizzo'), 'citta': data.get('citta'), 'cap': data.get('cap')
        }
        update_fields = {k: v for k, v in update_fields.items() if v is not None}
        
        if not update_fields:
            return jsonify({"msg": "Nessun dato da aggiornare"}), 400
            
        utenti_collection.update_one({'email': current_user_email}, {'$set': update_fields})
        return jsonify({"msg": "Profilo aggiornato con successo"}), 200

    utente = utenti_collection.find_one({'email': current_user_email}, {'_id': 0, 'password': 0})
    return jsonify(utente) if utente else (jsonify({"msg": "Utente non trovato"}), 404)


@app.route('/api/login', methods=['POST'])
def login():
    """Login con autenticazione e JWT"""
    data = request.get_json()
    utente = utenti_collection.find_one({'email': data.get('email')})

    if utente and check_password_hash(utente['password'], data.get('password')):
        access_token = create_access_token(identity=data.get('email'))
        return jsonify(
            access_token=access_token,
            carrello=utente.get('carrello', []),
            preferiti=utente.get('preferiti', [])
        )
        
    return jsonify({"msg": "Credenziali non valide"}), 401


@app.route('/api/preferiti', methods=['POST'])
@jwt_required()
def salva_preferiti():
    """Salva nel db i preferiti per ogni utente"""
    current_user_email = get_jwt_identity()
    preferiti = request.get_json()
    
    if not isinstance(preferiti, list):
        return jsonify({"msg": "Formato dati non valido"}), 400
        
    utenti_collection.update_one(
        {'email': current_user_email},
        {'$set': {'preferiti': preferiti}}
    )
    
    return jsonify({"msg": "Preferiti salvati"}), 200


@app.route('/api/carrello', methods=['POST'])
@jwt_required()
def salva_carrello():
    """Salva il carrello dell'utente"""
    current_user_email = get_jwt_identity()
    carrello = request.get_json()
    
    utenti_collection.update_one(
        {'email': current_user_email},
        {'$set': {'carrello': carrello}}
    )
    
    return jsonify({"msg": "Carrello salvato"}), 200


@app.route('/prodotti', methods=['GET'])
def get_prodotti():
    """Ritorna il prodotto per categoria / random"""
    categoria = request.args.get('categoria')
    random_count = request.args.get('random')

    try:
        if categoria:
            prodotti = list(collection.find({'categoria': categoria}, {'_id': 0}))
        elif random_count:
            prodotti = list(collection.aggregate([{'$sample': {'size': int(random_count)}}]))
            for p in prodotti:
                p.pop('_id', None)
        else:
            prodotti = list(collection.find({}, {'_id': 0}))
            
        return jsonify(prodotti)
    except Exception as e:
        print(f"Errore durante il recupero dei prodotti: {e}")
        return jsonify({"error": "Impossibile recuperare i prodotti"}), 500


@app.route('/calcola', methods=['POST'])
def gestisci_calcolo():
    """Gestione dei costi dello scontrio"""
    carrello = request.get_json()
    
    if not carrello:
        return jsonify({"error": "Carrello vuoto o formato non valido"}), 400
        
    try:
        risultato = calcola_scontrino(carrello, collection)
        return jsonify(risultato)
    except Exception as e:
        print(f"Errore durante il calcolo dello scontrino: {e}")
        return jsonify({"error": "Errore interno durante il calcolo"}), 500


@app.route('/api/checkout', methods=['POST'])
@jwt_required()
def checkout():
    """completa l'ordine e salvalo"""
    current_user_email = get_jwt_identity()
    carrello = request.get_json().get('cart')

    if not carrello:
        return jsonify({"msg": "Il carrello è vuoto"}), 400

    try:
        scontrino = calcola_scontrino(carrello, collection)
        prodotti_info = {item['nome']: item for item in carrello}

        prodotti_ordine = []
        for riga in scontrino['righe']:
            info_originali = prodotti_info.get(riga['nome'], {})
            prodotti_ordine.append({
                'nome': riga['nome'],
                'quantita': riga['quantita'],
                'prezzo_finale_riga': riga['prezzo_finale_riga'],
                'immagine_url': info_originali.get('immagine_url', ''),
                'prezzo_lordo': info_originali.get('prezzo_lordo', 0)
            })

        ordini_collection.insert_one({
            'utente_email': current_user_email,
            'data_ordine': datetime.utcnow(),
            'prodotti': prodotti_ordine,
            'totale_netto': scontrino['totale_netto'],
            'totale_tasse': scontrino['totale_tasse']
        })

        utenti_collection.update_one(
            {'email': current_user_email},
            {'$set': {'carrello': []}}
        )

        return jsonify({"msg": "Ordine completato con successo"}), 201
    except Exception as e:
        print(f"Errore durante il checkout: {e}")
        return jsonify({"error": "Errore interno durante la finalizzazione dell'ordine"}), 500


@app.route('/api/geo-ip', methods=['GET'])
def get_geo_ip():
    """Restituisce la zona in cui vivi (SERVE CHIAVE API)"""
    if not ipinfo_token:
        return jsonify({"error": "Configurazione del server incompleta per la geolocalizzazione"}), 500

    try:
        response = requests.get(f'https://ipinfo.io/json?token={ipinfo_token}', timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return jsonify({
            "city": data.get("city"),
            "country_code": data.get("country")
        })
    except requests.exceptions.Timeout:
        return jsonify({"error": "Il servizio di geolocalizzazione è lento a rispondere"}), 504
    except requests.exceptions.RequestException as e:
        print(f"Errore chiamando il servizio di geolocalizzazione: {e}")
        return jsonify({"error": "Servizio di geolocalizzazione non raggiungibile dal server"}), 503


@app.route('/api/random-image', methods=['GET'])
def get_random_image():
    """restituisce prodotto e immagine random"""
    try:
        random_product = list(collection.aggregate([{'$sample': {'size': 1}}]))[0]
        random_product.pop('_id', None)
        return jsonify(random_product)
    except Exception as e:
        print(f"Errore durante il recupero dell'immagine casuale: {e}")
        return jsonify({"error": "Impossibile recuperare l'immagine"}), 500


@app.route('/api/scontrino', methods=['POST'])
def genera_scontrino():
    """Genera lo scontrino"""
    carrello = request.get_json()
    
    if not carrello or not isinstance(carrello, list):
        return jsonify({"error": "Formato carrello non valido"}), 400

    try:
        scontrino_calcolato = calcola_scontrino(carrello, collection)
        return jsonify(scontrino_calcolato)
    except Exception as e:
        print(f"Errore durante la generazione dello scontrino: {e}")
        return jsonify({"error": "Errore interno durante il calcolo dello scontrino"}), 500


@app.route('/api/scontrino/<order_id>', methods=['GET'])
@jwt_required()
def get_scontrino(order_id):
    """Stampa dello scontrino tramite una pagina HTML Simil scontrino"""
    current_user_email = get_jwt_identity()
    
    try:
        obj_id = ObjectId(order_id)
    except InvalidId:
        return "ID dell'ordine non valido.", 400

    try:
        ordine = ordini_collection.find_one({'_id': obj_id, 'utente_email': current_user_email})
        utente = utenti_collection.find_one({'email': current_user_email})

        if not ordine or not utente:
            return "Ordine non trovato o non autorizzato.", 404

        html_items = "".join(
            f"""<div class="item">
                    <div style="width: 70%;">{item.get('quantita', '?')}x {item.get('nome', 'N/D')}</div>
                    <div>{item.get('prezzo_finale_riga', 'N/D')}</div>
                </div>"""
            for item in ordine.get('prodotti', [])
        )

        html = f"""
        <html>
            <head>
                <title>Scontrino Ordine</title>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: monospace; margin: 2rem; }}
                    .container {{ max-width: 400px; margin: auto; border: 1px solid #ccc; padding: 20px; }}
                    .header, .footer {{ text-align: center; }}
                    .items {{ border-top: 1px dashed #000; border-bottom: 1px dashed #000; margin: 15px 0; padding: 15px 0; }}
                    .item, .total {{ display: flex; justify-content: space-between; }}
                    .item div {{ white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
                    .total {{ font-weight: bold; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>POS Register</h2>
                        <p>Grazie per il tuo acquisto!</p>
                        <p>Cliente: {utente.get('nome', '')} {utente.get('cognome', '')}</p>
                        <p>Data: {ordine['data_ordine'].strftime('%d/%m/%Y %H:%M')}</p>
                    </div>
                    <div class="items">{html_items}</div>
                    <div class="totals">
                        <div class="total"><span>Totale Tasse (IVA)</span><span>{ordine.get('totale_tasse', 'N/D')}</span></div>
                        <div class="total" style="font-size: 1.2em; margin-top: 10px;"><span>TOTALE</span><span>{ordine.get('totale_netto', 'N/D')}</span></div>
                    </div>
                    <div class="footer" style="margin-top: 20px;">
                        <p>POS Register Regesta❤️</p>
                    </div>
                </div>
            </body>
        </html>
        """
        return html
    except Exception as e:
        print(f"Errore nella generazione dello scontrino HTML: {e}")
        return "Errore interno del server durante la creazione dello scontrino.", 500


@app.route('/api/prodotto/<slug_prodotto>', methods=['GET'])
def get_prodotto_singolo(slug_prodotto):
    """Restituisce il prodotto da slug"""
    try:
        for prodotto in collection.find({}, {'_id': 0}):
            slug_db = re.sub(r'[^\w-]+', '', re.sub(r'[()]', '', prodotto['nome'].lower().replace(' ', '-')))
            if slug_db == slug_prodotto:
                return jsonify(prodotto)
                
        return jsonify({"error": f"Prodotto non trovato per lo slug: {slug_prodotto}"}), 404
    except Exception as e:
        print(f"Errore durante il recupero del prodotto singolo: {e}")
        return jsonify({"error": "Errore interno del server"}), 500


@app.route('/api/search-results', methods=['GET'])
def search_results():
    """ricerca prodotti con filtri"""
    query = request.args.get('q', '')
    categoria = request.args.get('categoria')
    prezzo_min = request.args.get('prezzo_min')
    prezzo_max = request.args.get('prezzo_max')

    mongo_query = {}

    if query:
        mongo_query['nome'] = {'$regex': re.compile(query, re.IGNORECASE)}
    if categoria:
        mongo_query['categoria'] = categoria
    if prezzo_min or prezzo_max:
        prezzo_filter = {}
        if prezzo_min:
            prezzo_filter['$gte'] = float(prezzo_min)
        if prezzo_max:
            prezzo_filter['$lte'] = float(prezzo_max)
        mongo_query['prezzo_lordo'] = prezzo_filter

    try:
        risultati = list(collection.find(mongo_query, {'_id': 0}))
        return jsonify(risultati)
    except Exception as e:
        print(f"Errore durante la ricerca filtrata: {e}")
        return jsonify({"error": "Errore interno del server"}), 500


@app.route('/api/ordini', methods=['GET'])
@jwt_required()
def get_ordini():
    """cronologia degli ordini"""
    current_user_email = get_jwt_identity()
    
    try:
        ordini = list(ordini_collection.find(
            {'utente_email': current_user_email}
        ).sort('data_ordine', -1))
        
        for ordine in ordini:
            ordine['_id'] = str(ordine['_id'])
            
        return jsonify(ordini)
    except Exception as e:
        print(f"Errore durante il recupero degli ordini: {e}")
        return jsonify({"error": "Impossibile recuperare la cronologia ordini"}), 500


@app.route('/api/categorie', methods=['GET'])
def get_categorie():
    """ritorna le varie categorie dal db degli oggetti"""
    try:
        categorie = collection.distinct('categoria')
        return jsonify(categorie)
    except Exception as e:
        print(f"Errore durante il recupero delle categorie: {e}")
        return jsonify({"error": "Impossibile recuperare le categorie"}), 500


if __name__ == '__main__':
    app.run(debug=True)