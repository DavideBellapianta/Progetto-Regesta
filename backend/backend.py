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

# --- 1. CONFIGURAZIONE INIZIALE E CONNESSIONE AL DATABASE ---

# Carica le variabili d'ambiente dal file .env
load_dotenv()
username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")
ipinfo_token = os.getenv("IPINFO_TOKEN") # <-- Legge la nuova chiave API


# Controlla che le credenziali siano presenti
if not username or not password:
    raise ValueError("Le variabili MONGO_USER e MONGO_PASS devono essere definite nel file .env")

# Connessione sicura a MongoDB
encoded_password = urllib.parse.quote_plus(password)
uri = f"mongodb+srv://{username}:{encoded_password}@progetto1.baefqmn.mongodb.net/?retryWrites=true&w=majority&appName=Progetto1"
client = MongoClient(uri)
db = client['databaseProdotti']
collection = db['prodotti']
utenti_collection = db['utenti']
ordini_collection = db['ordini'] 


# --- INIZIALIZZAZIONE FLASK E JWT ---
app = Flask(__name__)
# Configura una chiave segreta per firmare i token JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key-default") # Aggiungi JWT_SECRET_KEY al tuo .env
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

@app.route('/api/registrazione', methods=['POST'])
def registrazione():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    # Recupera i nuovi campi
    nome = data.get('nome')
    cognome = data.get('cognome')

    if not email or not password or not nome or not cognome:
        return jsonify({"msg": "Tutti i campi sono richiesti"}), 400
    if utenti_collection.find_one({'email': email}):
        return jsonify({"msg": "Utente già esistente"}), 409

    password_hash = generate_password_hash(password)
    # Salva i nuovi dati nel database
    utenti_collection.insert_one({
        'email': email, 
        'password': password_hash, 
        'nome': nome,
        'cognome': cognome,
        'indirizzo': '', # Inizializza i campi opzionali
        'citta': '',
        'carrello': [],
        'preferiti': []
        
    })
    return jsonify({"msg": "Utente registrato con successo"}), 201

@app.route('/api/profilo', methods=['GET', 'POST'])
@jwt_required()
def profilo_utente():
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

    if request.method == 'GET':
        utente = utenti_collection.find_one({'email': current_user_email}, {'_id': 0, 'password': 0})
        if utente:
            return jsonify(utente)
        return jsonify({"msg": "Utente non trovato"}), 404
    
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    utente = utenti_collection.find_one({'email': email})

    if utente and check_password_hash(utente['password'], password):
        access_token = create_access_token(identity=email)
        carrello_salvato = utente.get('carrello', [])
        preferiti_salvati = utente.get('preferiti', []) # <-- AGGIUNGI QUESTO
        return jsonify(
            access_token=access_token, 
            carrello=carrello_salvato,
            preferiti=preferiti_salvati # <-- AGGIUNGI QUESTO
        )
    return jsonify({"msg": "Credenziali non valide"}), 401


@app.route('/api/preferiti', methods=['POST'])
@jwt_required()
def salva_preferiti():
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
    current_user_email = get_jwt_identity()
    carrello = request.get_json()
    utenti_collection.update_one(
        {'email': current_user_email},
        {'$set': {'carrello': carrello}}
    )
    return jsonify({"msg": "Carrello salvato"}), 200

@app.route('/prodotti', methods=['GET'])
def get_prodotti():
    """
    Restituisce i prodotti. Accetta filtri tramite query parameters:
    - ?categoria=food -> Restituisce solo prodotti della categoria 'food'
    - ?random=4      -> Restituisce 4 prodotti casuali
    """
    try:
        categoria = request.args.get('categoria')
        random_count = request.args.get('random')

        if categoria:
            query = {'categoria': categoria}
            lista_prodotti = list(collection.find(query, {'_id': 0}))
            return jsonify(lista_prodotti)

        if random_count:
            count = int(random_count)
            pipeline = [{'$sample': {'size': count}}]
            # Convertiamo il cursore in una lista subito
            lista_prodotti = list(collection.aggregate(pipeline))
            # Rimuoviamo l'_id che aggregate() include
            for p in lista_prodotti:
                p.pop('_id', None)
            return jsonify(lista_prodotti)

        # Se non ci sono filtri, restituisce tutto
        lista_prodotti = list(collection.find({}, {'_id': 0}))
        return jsonify(lista_prodotti)

    except Exception as e:
        print(f"Errore durante il recupero dei prodotti: {e}")
        return jsonify({"error": "Impossibile recuperare i prodotti"}), 500

# (La rotta /calcola rimane invariata)
@app.route('/calcola', methods=['POST'])
def gestisci_calcolo():
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
    """
    Finalizza l'ordine: calcola lo scontrino, salva l'ordine completo di tutti i dati
    e svuota il carrello dell'utente.
    """
    current_user_email = get_jwt_identity()
    data = request.get_json()
    carrello = data.get('cart') # Questo è il carrello "grezzo" dal frontend

    if not carrello:
        return jsonify({"msg": "Il carrello è vuoto"}), 400

    try:
        # 1. Ricalcola lo scontrino sul backend. Questa è la "fonte di verità".
        scontrino_calcolato = calcola_scontrino(carrello, collection)

        # 2. Arricchisci i dati da salvare.
        #    Crea un dizionario per un accesso veloce ai dati originali (come l'immagine_url).
        prodotti_info = {item['nome']: item for item in carrello}

        prodotti_per_ordine = []
        for riga_scontrino in scontrino_calcolato['righe']:
            nome_prodotto = riga_scontrino['nome']
            info_originali = prodotti_info.get(nome_prodotto, {})
            
            # Uniamo i dati calcolati con quelli originali mancanti
            prodotti_per_ordine.append({
                'nome': nome_prodotto,
                'quantita': riga_scontrino['quantita'],
                'prezzo_finale_riga': riga_scontrino['prezzo_finale_riga'],
                'immagine_url': info_originali.get('immagine_url', ''), # <-- Dato mancante aggiunto
                'prezzo_lordo': info_originali.get('prezzo_lordo', 0) # <-- Dato mancante aggiunto
            })

        # 3. Crea il documento dell'ordine con i dati arricchiti
        nuovo_ordine = {
            'utente_email': current_user_email,
            'data_ordine': datetime.utcnow(),
            'prodotti': prodotti_per_ordine, # <-- Usa la nuova lista arricchita
            'totale_netto': scontrino_calcolato['totale_netto'],
            'totale_tasse': scontrino_calcolato['totale_tasse']
        }
        ordini_collection.insert_one(nuovo_ordine)

        # 4. Svuota il carrello dell'utente
        utenti_collection.update_one(
            {'email': current_user_email},
            {'$set': {'carrello': []}}
        )

        return jsonify({"msg": "Ordine completato con successo"}), 201
    except Exception as e:
        print(f"Errore durante il checkout: {e}")
        return jsonify({"error": "Errore interno durante la finalizzazione dell'ordine"}), 500



# ROTTA PROXY PER GEOLOCALIZZAZIONE (con API Key)
@app.route('/api/geo-ip', methods=['GET'])
def get_geo_ip():
    """
    [MODALITÀ SVILUPPO] - Restituisce una posizione fissa per non consumare token.
    Per riattivare la chiamata reale, decommenta il blocco 'try...except' 
    e commenta o cancella le righe sotto 'DATI FITTIZI'.
    """
    print("--- ATTENZIONE: La geolocalizzazione è in modalità fittizia (mock) ---")
    
    # --- DATI FITTIZI (MOCK) ---
    dati_fittizi = {
        "city": "Brescia (Dev)",
        "country_code": "IT"
    }
    return jsonify(dati_fittizi)

    # --- CODICE REALE (temporaneamente disattivato con '#') ---
    # if not ipinfo_token:
    #     return jsonify({"error": "Configurazione del server incompleta per la geolocalizzazione"}), 500
    #
    # url_da_chiamare = f'https://ipinfo.io/json?token={ipinfo_token}'
    # 
    # try:
    #     response = requests.get(url_da_chiamare, timeout=10)
    #     response.raise_for_status()
    #     
    #     data = response.json()
    #     formatted_data = {
    #         "city": data.get("city"),
    #         "country_code": data.get("country")
    #     }
    #     return jsonify(formatted_data)
    #     
    # except requests.exceptions.Timeout:
    #     print(f"Errore chiamando {url_da_chiamare}: Timeout")
    #     return jsonify({"error": "Il servizio di geolocalizzazione è lento a rispondere"}), 504
    # except requests.exceptions.RequestException as e:
    #     print(f"Errore chiamando {url_da_chiamare}: {e}")
    #     return jsonify({"error": "Servizio di geolocalizzazione non raggiungibile dal server"}), 503

@app.route('/api/random-image', methods=['GET'])
def get_random_image():
    """Seleziona un prodotto a caso e ne restituisce i dati."""
    try:
        pipeline = [{'$sample': {'size': 1}}]
        random_product_list = list(collection.aggregate(pipeline))
        if not random_product_list:
            return jsonify({"error": "Nessun prodotto trovato"}), 404
        
        random_product = random_product_list[0]
        random_product.pop('_id', None)
        return jsonify(random_product)
    except Exception as e:
        print(f"Errore durante il recupero dell'immagine casuale: {e}")
        return jsonify({"error": "Impossibile recuperare l'immagine"}), 500

@app.route('/api/scontrino', methods=['POST'])
def genera_scontrino():
    """
    Riceve il carrello dal frontend, usa la logica di calcolo
    e restituisce lo scontrino completo di totali e tasse.
    """
    # Ottiene il carrello (una lista di prodotti) dal corpo della richiesta
    carrello = request.get_json()
    if not carrello or not isinstance(carrello, list):
        return jsonify({"error": "Formato carrello non valido"}), 400

    try:
        # Usa la funzione importata per fare tutti i calcoli
        scontrino_calcolato = calcola_scontrino(carrello, collection)
        return jsonify(scontrino_calcolato)
    except Exception as e:
        print(f"Errore durante la generazione dello scontrino: {e}")
        return jsonify({"error": "Errore interno durante il calcolo dello scontrino"}), 500
        

@app.route('/api/scontrino/<order_id>', methods=['GET'])
@jwt_required()
def get_scontrino(order_id):
    current_user_email = get_jwt_identity()
    
    # --- CONTROLLO DI SICUREZZA SULL'ID ---
    try:
        # Tenta di convertire l'ID. Se non è valido, lancia un errore.
        obj_id = ObjectId(order_id)
    except InvalidId:
        return "ID dell'ordine non valido.", 400

    try:
        # Ora usiamo l'ID validato per la ricerca
        ordine = ordini_collection.find_one({'_id': obj_id, 'utente_email': current_user_email})
        utente = utenti_collection.find_one({'email': current_user_email})

        if not ordine or not utente:
            return "Ordine non trovato o non autorizzato.", 404

        # --- Generazione HTML (invariata) ---
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
                    <div class="items">
        """
        # 2. CORREZIONE PREZZI: Usiamo i dati calcolati e salvati, non ricalcoliamo il lordo.
        #    Assicurati che la rotta /api/checkout salvi l'intero scontrino_calcolato.
        #    Se hai salvato le righe calcolate, 'prodotti' conterrà 'prezzo_finale_riga'.
        for item in ordine.get('prodotti', []):
            html += f"""
                        <div class="item">
                            <div style="width: 70%;">{item.get('quantita', '?')}x {item.get('nome', 'N/D')}</div>
                            <div>{item.get('prezzo_finale_riga', 'N/D')}</div>
                        </div>
            """
        html += f"""
                    </div>
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
    """
    Trova un prodotto confrontando il suo slug con quello richiesto.
    Questo metodo è più robusto perché replica la logica del frontend.
    """
    try:
        # Scansiona tutti i prodotti nel database
        for prodotto in collection.find({}, {'_id': 0}):
            # Crea uno slug dal nome del prodotto nel DB con la STESSA logica del frontend
            nome_db = prodotto['nome']
            
            # Logica di slugging identica a quella di Svelte
            slug_db = nome_db.lower()
            slug_db = re.sub(r'\s+', '-', slug_db) # Sostituisce spazi con trattini
            slug_db = re.sub(r'[()]', '', slug_db)  # Rimuove le parentesi
            slug_db = re.sub(r'[^\w-]+', '', slug_db) # Rimuove altri caratteri non validi

            if slug_db == slug_prodotto:
                return jsonify(prodotto) # Trovato! Restituisci il prodotto.
        
        # Se il ciclo finisce senza trovare nulla
        return jsonify({"error": f"Prodotto non trovato per lo slug: {slug_prodotto}"}), 404
            
    except Exception as e:
        print(f"Errore durante il recupero del prodotto singolo: {e}")
        return jsonify({"error": "Errore interno del server"}), 500

@app.route('/api/search-results', methods=['GET'])
def search_results():
    """
    Cerca nel database e restituisce i prodotti che corrispondono ai filtri.
    Filtri possibili: q (testo), categoria, prezzo_min, prezzo_max.
    """
    query = request.args.get('q', '')
    categoria = request.args.get('categoria')
    prezzo_min = request.args.get('prezzo_min')
    prezzo_max = request.args.get('prezzo_max')

    # Costruiamo la query per MongoDB dinamicamente
    mongo_query = {}

    if query:
        search_regex = re.compile(query, re.IGNORECASE)
        mongo_query['nome'] = {'$regex': search_regex}
    
    if categoria:
        mongo_query['categoria'] = categoria

    if prezzo_min or prezzo_max:
        prezzo_filter = {}
        if prezzo_min:
            try:
                prezzo_filter['$gte'] = float(prezzo_min)
            except ValueError:
                pass # Ignora se non è un numero valido
        if prezzo_max:
            try:
                prezzo_filter['$lte'] = float(prezzo_max)
            except ValueError:
                pass # Ignora se non è un numero valido
        if prezzo_filter:
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
    """Recupera la cronologia ordini dell'utente loggato."""
    current_user_email = get_jwt_identity()
    try:
        # 1. Rimuovi {'_id': 0} per includere l'ID dell'ordine
        ordini = list(ordini_collection.find(
            {'utente_email': current_user_email}
        ).sort('data_ordine', -1))
        
        # 2. Converti l'ObjectId di MongoDB in una stringa per ogni ordine
        for ordine in ordini:
            ordine['_id'] = str(ordine['_id'])
            
        return jsonify(ordini)
    except Exception as e:
        print(f"Errore durante il recupero degli ordini: {e}")
        return jsonify({"error": "Impossibile recuperare la cronologia ordini"}), 500

@app.route('/api/categorie', methods=['GET'])
def get_categorie():
    """
    Trova e restituisce una lista di tutte le categorie di prodotti uniche.
    """
    try:
        # Usiamo 'distinct' di MongoDB per ottenere una lista di valori unici dal campo 'categoria'
        lista_categorie = collection.distinct('categoria')
        return jsonify(lista_categorie)
    except Exception as e:
        print(f"Errore durante il recupero delle categorie: {e}")
        return jsonify({"error": "Impossibile recuperare le categorie"}), 500

if __name__ == '__main__':
    # debug=True ricarica il server automaticamente quando salvi le modifiche
    app.run(debug=True)