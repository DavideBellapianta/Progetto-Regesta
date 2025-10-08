# seed_db.py (versione manuale)
import os
import urllib.parse
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")

# Connessione al DB
encoded_password = urllib.parse.quote_plus(password)
uri = f"mongodb+srv://{username}:{encoded_password}@progetto1.baefqmn.mongodb.net/?retryWrites=true&w=majority&appName=Progetto1"
client = MongoClient(uri)
db = client['databaseProdotti']
collection = db['prodotti']

# Pulisce la collezione per evitare duplicati
collection.delete_many({})

# Lista dei prodotti con URL delle immagini inseriti a mano
prodotti_da_inserire = [
    # Categoria Food
    { 
        "nome": "Tavoletta di cioccolato fondente 85%", 
        "prezzo_lordo": 2.49, 
        "categoria": "food", 
        "immagine_url": "https://images.unsplash.com/photo-1623660053975-cf75a8be0908?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Un'intensa esperienza di gusto con il nostro cioccolato extra fondente all'85%. Perfetto per una pausa energizzante o per la preparazione di dolci raffinati. Cacao proveniente da agricoltura sostenibile."
    },
    { 
        "nome": "Acqua Minerale Naturale (1.5L)", 
        "prezzo_lordo": 0.35, 
        "categoria": "food", 
        "immagine_url": "https://images.unsplash.com/photo-1544509925-a45ab789916b?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Acqua minerale oligominerale, microbiologicamente pura. Ideale per l'idratazione quotidiana di tutta la famiglia. Residuo fisso a 180°C: 45mg/L."
    },
    { 
        "nome": "Lattina di Coca-Cola Original Taste", 
        "prezzo_lordo": 0.79, 
        "categoria": "food", 
        "immagine_url": "https://images.unsplash.com/photo-1667204651371-5d4a65b8b5a9?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Il gusto inimitabile di Coca-Cola in un formato pratico da 33cl. Servire fredda per un'esperienza di gusto ottimale. Lattina 100% riciclabile."
    },
    { 
        "nome": "Patatine Classiche in Busta (150g)", 
        "prezzo_lordo": 1.49, 
        "categoria": "food", 
        "immagine_url": "https://images.unsplash.com/photo-1694101493160-10f1257fe9fd?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fGNoaXBzJTIwYmFnfGVufDB8fDB8fHww",
        "descrizione": "Croccanti patatine fritte dal gusto classico e irresistibile. Solo patate selezionate, olio di semi di girasole e un pizzico di sale. Senza glutine."
    },
    { 
        "nome": "Spaghettoni N.7 Barilla (500g)", 
        "prezzo_lordo": 1.29, 
        "categoria": "food", 
        "immagine_url": "https://images.unsplash.com/photo-1718043934012-380f4e72a1cf?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Spaghettoni di semola di grano duro, dalla consistenza corposa e ruvida che cattura ogni tipo di sugo. Tempo di cottura: 11 minuti. 100% grano italiano."
    },

    # Categoria Medical
    { 
        "nome": "Confezione di Cerotti Assortiti (40 pz)", 
        "prezzo_lordo": 3.99, 
        "categoria": "medical", 
        "immagine_url": "https://plus.unsplash.com/premium_photo-1672073399147-53ebffa8395b?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Set di 40 cerotti ipoallergenici e traspiranti in formati assortiti. Resistenti all'acqua e adatti per piccoli tagli e abrasioni. Indispensabili nel kit di primo soccorso."
    },
    { 
        "nome": "Termometro Digitale a Infrarossi", 
        "prezzo_lordo": 19.90, 
        "categoria": "medical", 
        "immagine_url": "https://images.unsplash.com/photo-1615486511369-31ff08672204?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Termometro frontale a infrarossi per una misurazione della temperatura rapida, precisa e senza contatto. Display LCD retroilluminato e memoria delle ultime misurazioni."
    },
    { 
        "nome": "Sciroppo per la Tosse (150ml)", 
        "prezzo_lordo": 8.50, 
        "categoria": "medical", 
        "immagine_url": "https://images.unsplash.com/photo-1617800553712-2db4ebd9d908?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Sciroppo a base di estratti naturali per calmare la tosse secca e grassa. Formula adatta per adulti e bambini sopra i 6 anni. Aroma miele e limone."
    },
    { 
        "nome": "Pacco Mascherine Chirurgiche (10 pz)", 
        "prezzo_lordo": 2.99, 
        "categoria": "medical", 
        "immagine_url": "https://images.unsplash.com/photo-1622631090360-ba04acd2e02f?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Confezione da 10 mascherine chirurgiche monouso a 3 veli. Elevata efficienza di filtrazione batterica (BFE ≥ 98%) e ottima respirabilità. Dispositivo Medico di Classe I."
    },

    # Categoria Other
    { 
        "nome": "Mazzo di Carte da Gioco Francesi", 
        "prezzo_lordo": 2.90, 
        "categoria": "other", 
        "immagine_url": "https://images.unsplash.com/photo-1501003878151-d3cb87799705?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Mazzo da 54 carte da gioco classiche con semi francesi. Finitura telata per una maggiore durata e una migliore maneggevolezza. Perfette per Poker, Burraco e altri giochi."
    },
    { 
        "nome": "Caricabatterie USB-C Rapido (20W)", 
        "prezzo_lordo": 14.99, 
        "categoria": "other", 
        "immagine_url": "https://plus.unsplash.com/premium_photo-1669262667978-5d4aafe29dd5?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Alimentatore da parete con porta USB-C da 20W e tecnologia Power Delivery. Ricarica rapidamente il tuo smartphone, tablet e altri dispositivi compatibili. Design compatto e portatile."
    },
    { 
        "nome": "Lampadina LED E27 (10W)", 
        "prezzo_lordo": 3.50, 
        "categoria": "other", 
        "immagine_url": "https://plus.unsplash.com/premium_photo-1672166939591-b2547bd18fca?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Lampadina LED con attacco E27, 10W di consumo (equivalente a 75W tradizionali). Luce bianca calda (2700K) per un'atmosfera accogliente. Classe di efficienza energetica A+."
    },
    { 
        "nome": "Confezione Batterie Stilo AAA (4 pz)", 
        "prezzo_lordo": 3.49, 
        "categoria": "other", 
        "immagine_url": "https://images.unsplash.com/photo-1704895336143-334cc3bccfc6?q=80&w=735&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "descrizione": "Pacco da 4 batterie alcaline tipo AAA a lunga durata. Ideali per telecomandi, giocattoli e piccoli dispositivi elettronici. Affidabilità garantita."
    }
]
collection.create_index([('nome', 'text')])


# Inserisce tutti i prodotti
collection.insert_many(prodotti_da_inserire)

print(f"Database popolato con {len(prodotti_da_inserire)} prodotti (link manuali).")
client.close()