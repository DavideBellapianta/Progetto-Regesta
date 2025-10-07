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
    { "nome": "Tavoletta di cioccolato fondente", "prezzo_lordo": 1.99, "categoria": "food", "immagine_url": "https://images.unsplash.com/photo-1623660053975-cf75a8be0908?w=1000&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Q2hvY29sYXRlJTIwJTIwYmFyfGVufDB8fDB8fHww" },
    { "nome": "Acqua minerale naturale (1L)", "prezzo_lordo": 0.25, "categoria": "food", "immagine_url": "https://images.unsplash.com/photo-1544509925-a45ab789916b?w=1000&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fEJvdHRsZSUyMG9mJTIwd2F0ZXJ8ZW58MHx8MHx8fDA%3D" },
    { "nome": "Lattina di Coca Cola", "prezzo_lordo": 0.60, "categoria": "food", "immagine_url": "https://images.unsplash.com/photo-1667204651371-5d4a65b8b5a9?w=1000&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Q29jYSUyMGNvbGElMjBjYW58ZW58MHx8MHx8fDA%3D" },
    { "nome": "Pacchetto di patatine classiche", "prezzo_lordo": 1.20, "categoria": "food", "immagine_url": "https://images.unsplash.com/photo-1741520149938-4f08654780ef?w=1000&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGNoaXBzJTIwcGFja2V0fGVufDB8fDB8fHww" },
    { "nome": "Scatola di biscotti al cioccolato", "prezzo_lordo": 2.50, "categoria": "food", "immagine_url": "https://unsplash.com/it/foto/cupcake-al-cioccolato-con-glassa-bianca-in-cima-3jNTCCeC7gI" },
    { "nome": "Spaghettoni N7 Barilla (500g)", "prezzo_lordo": 0.89, "categoria": "food", "immagine_url": "https://images.unsplash.com/photo-1718043934012-380f4e72a1cf?w=1000&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8YmFyaWxsYXxlbnwwfHwwfHx8MA%3D%3D" },
    { "nome": "Vasetto di sugo al basilico", "prezzo_lordo": 1.50, "categoria": "food", "immagine_url": "https://images.unsplash.com/photo-1741594822867-0d849faff7e3?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjJ8fHRvbWF0byUyMHNhdWNlJTIwYm90dGxlfGVufDB8fDB8fHww" },

    # Categoria Medical
    { "nome": "Confezione di cerotti assortiti", "prezzo_lordo": 4.75, "categoria": "medical", "immagine_url": "https://plus.unsplash.com/premium_photo-1672073399147-53ebffa8395b?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTd8fGJhbmQtYWlkfGVufDB8fDB8fHww" },
    { "nome": "Termometro digitale", "prezzo_lordo": 8.90, "categoria": "medical", "immagine_url": "https://images.unsplash.com/photo-1615486511369-31ff08672204?q=80&w=1332&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" },
    { "nome": "Flacone di disinfettante per le mani", "prezzo_lordo": 3.20, "categoria": "medical", "immagine_url": "https://images.unsplash.com/photo-1608564348103-2b78891150cf?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8aGFuZCUyMHNhbml0aXplcnxlbnwwfHwwfHx8MA%3D%3D" },
    { "nome": "Sciroppo per la tosse", "prezzo_lordo": 9.50, "categoria": "medical", "immagine_url": "https://images.unsplash.com/photo-1617800553712-2db4ebd9d908?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Y291Z2glMjBzeXJ1cHxlbnwwfHwwfHx8MA%3D%3D" },
    { "nome": "Pacco di mascherine chirurgiche (10 pz)", "prezzo_lordo": 5.00, "categoria": "medical", "immagine_url": "https://images.unsplash.com/photo-1622631090360-ba04acd2e02f?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fG1hc2tzfGVufDB8fDB8fHww" },

    # Categoria Other
    { "nome": "Mazzo di carte da gioco", "prezzo_lordo": 3.50, "categoria": "other", "immagine_url": "https://images.unsplash.com/photo-1501003878151-d3cb87799705?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Y2FyZCUyMGdhbWV8ZW58MHx8MHx8fDA%3D" },
    { "nome": "Set di 3 penne a sfera", "prezzo_lordo": 2.10, "categoria": "other", "immagine_url": "https://images.unsplash.com/photo-1601311911926-dbdae16e54c9?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8c2V0JTIwb2YlMjAzJTIwcGVufGVufDB8fDB8fHww" },
    { "nome": "Caricabatterie USB per smartphone", "prezzo_lordo": 15.00, "categoria": "other", "immagine_url": "https://plus.unsplash.com/premium_photo-1669262667978-5d4aafe29dd5?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8VVNCJTIwY2FibGV8ZW58MHx8MHx8fDA%3D" },
    { "nome": "Lampadina LED a risparmio energetico", "prezzo_lordo": 4.50, "categoria": "other", "immagine_url": "https://plus.unsplash.com/premium_photo-1672166939591-b2547bd18fca?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8TGVkJTIwbGFtcHxlbnwwfHwwfHx8MA%3D%3D" },
    { "nome": "Confezione di batterie stilo AAA (4 pz)", "prezzo_lordo": 3.99, "categoria": "other", "immagine_url": "https://images.unsplash.com/photo-1704895336495-bdad8efe8d4e?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8QmF0dGVyeSUyMEFBQXxlbnwwfHwwfHx8MA%3D%3D" }
]

# Inserisce tutti i prodotti
collection.insert_many(prodotti_da_inserire)

print(f"Database popolato con {len(prodotti_da_inserire)} prodotti (link manuali).")
client.close()