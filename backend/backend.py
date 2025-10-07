import os
import urllib.parse
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from calcolatore_iva import calcola_scontrino
import re 

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

# --- 2. INIZIALIZZAZIONE DELL'APPLICAZIONE FLASK ---

app = Flask(__name__)
# Abilita CORS per permettere la comunicazione con il frontend Svelte
CORS(app)

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

# --- 4. ROTTA PROXY PER LA GEOLOCALIZZAZIONE (LA CORREZIONE CHIAVE) ---

# backend.py

# ... (tutto il resto del codice rimane uguale) ...

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
# --- 5. AVVIO DEL SERVER ---

if __name__ == '__main__':
    # debug=True ricarica il server automaticamente quando salvi le modifiche
    app.run(debug=True)