import os
import urllib.parse
import random
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()
username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")
admin_email = os.getenv("ADMIN_EMAIL")
admin_password = os.getenv("ADMIN_PASSWORD")

encoded_password = urllib.parse.quote_plus(password)
uri = f"mongodb+srv://{username}:{encoded_password}@progetto1.baefqmn.mongodb.net/?retryWrites=true&w=majority&appName=Progetto1"
client = MongoClient(uri)
db = client['databaseProdotti']
collection = db['prodotti']
utenti_collection = db['utenti']

collection.delete_many({})

prodotti_da_inserire = [
    { 
        "nome": "Tavoletta di cioccolato fondente 85%", 
        "prezzo_lordo": 2.49, 
        "categoria": "food", 
        "immagine_url": "https://images.unsplash.com/photo-1623660053975-cf75a8be0908?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Un'intensa esperienza di gusto con il nostro cioccolato extra fondente all'85%. Perfetto per una pausa energizzante o per la preparazione di dolci raffinati. Cacao proveniente da agricoltura sostenibile.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Acqua Minerale Naturale (1.5L)", 
        "prezzo_lordo": 0.35, 
        "categoria": "food", 
        "immagine_url": "https://images.unsplash.com/photo-1544509925-a45ab789916b?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Acqua minerale oligominerale, microbiologicamente pura. Ideale per l'idratazione quotidiana di tutta la famiglia. Residuo fisso a 180°C: 45mg/L.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Lattina di Coca-Cola Original Taste", 
        "prezzo_lordo": 0.79, 
        "categoria": "food", 
        "immagine_url": "https://images.unsplash.com/photo-1667204651371-5d4a65b8b5a9?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Il gusto inimitabile di Coca-Cola in un formato pratico da 33cl. Servire fredda per un'esperienza di gusto ottimale. Lattina 100% riciclabile.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Patatine Classiche in Busta (150g)", 
        "prezzo_lordo": 1.49, 
        "categoria": "food", 
        "immagine_url": "https://images.unsplash.com/photo-1694101493160-10f1257fe9fd?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fGNoaXBzJTIwYmFnfGVufDB8fDB8fHww",
        "descrizione": "Croccanti patatine fritte dal gusto classico e irresistibile. Solo patate selezionate, olio di semi di girasole e un pizzico di sale. Senza glutine.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Spaghettoni N.7 Barilla (500g)", 
        "prezzo_lordo": 1.29, 
        "categoria": "food", 
        "immagine_url": "https://images.unsplash.com/photo-1718043934012-380f4e72a1cf?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Spaghettoni di semola di grano duro, dalla consistenza corposa e ruvida che cattura ogni tipo di sugo. Tempo di cottura: 11 minuti. 100% grano italiano.",
        "quantita": random.randint(35, 100)
    },

    { 
        "nome": "Confezione di Cerotti Assortiti (40 pz)", 
        "prezzo_lordo": 3.99, 
        "categoria": "medical", 
        "immagine_url": "https://plus.unsplash.com/premium_photo-1672073399147-53ebffa8395b?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Set di 40 cerotti ipoallergenici e traspiranti in formati assortiti. Resistenti all'acqua e adatti per piccoli tagli e abrasioni. Indispensabili nel kit di primo soccorso.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Termometro Digitale a Infrarossi", 
        "prezzo_lordo": 19.90, 
        "categoria": "medical", 
        "immagine_url": "https://images.unsplash.com/photo-1615486511369-31ff08672204?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Termometro frontale a infrarossi per una misurazione della temperatura rapida, precisa e senza contatto. Display LCD retroilluminato e memoria delle ultime misurazioni.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Sciroppo per la Tosse (150ml)", 
        "prezzo_lordo": 8.50, 
        "categoria": "medical", 
        "immagine_url": "https://images.unsplash.com/photo-1617800553712-2db4ebd9d908?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Sciroppo a base di estratti naturali per calmare la tosse secca e grassa. Formula adatta per adulti e bambini sopra i 6 anni. Aroma miele e limone.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Pacco Mascherine Chirurgiche (10 pz)", 
        "prezzo_lordo": 2.99, 
        "categoria": "medical", 
        "immagine_url": "https://images.unsplash.com/photo-1622631090360-ba04acd2e02f?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Confezione da 10 mascherine chirurgiche monouso a 3 veli. Elevata efficienza di filtrazione batterica (BFE ≥ 98%) e ottima respirabilità. Dispositivo Medico di Classe I.",
        "quantita": random.randint(35, 100)
    },

    { 
        "nome": "Mazzo di Carte da Gioco Francesi", 
        "prezzo_lordo": 2.90, 
        "categoria": "other", 
        "immagine_url": "https://images.unsplash.com/photo-1501003878151-d3cb87799705?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Mazzo da 54 carte da gioco classiche con semi francesi. Finitura telata per una maggiore durata e una migliore maneggevolezza. Perfette per Poker, Burraco e altri giochi.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Caricabatterie USB-C Rapido (20W)", 
        "prezzo_lordo": 14.99, 
        "categoria": "other", 
        "immagine_url": "https://plus.unsplash.com/premium_photo-1669262667978-5d4aafe29dd5?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Alimentatore da parete con porta USB-C da 20W e tecnologia Power Delivery. Ricarica rapidamente il tuo smartphone, tablet e altri dispositivi compatibili. Design compatto e portatile.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Lampadina LED E27 (10W)", 
        "prezzo_lordo": 3.50, 
        "categoria": "other", 
        "immagine_url": "https://plus.unsplash.com/premium_photo-1672166939591-b2547bd18fca?w=1000&auto=format&fit=crop&q=60",
        "descrizione": "Lampadina LED con attacco E27, 10W di consumo (equivalente a 75W tradizionali). Luce bianca calda (2700K) per un'atmosfera accogliente. Classe di efficienza energetica A+.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Confezione Batterie Stilo AAA (4 pz)", 
        "prezzo_lordo": 3.49, 
        "categoria": "other", 
        "immagine_url": "https://images.unsplash.com/photo-1704895336143-334cc3bccfc6?q=80&w=735&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "descrizione": "Pacco da 4 batterie alcaline tipo AAA a lunga durata. Ideali per telecomandi, giocattoli e piccoli dispositivi elettronici. Affidabilità garantita.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Cuffie Bluetooth con Cancellazione del Rumore", 
        "prezzo_lordo": 79.99, 
        "categoria": "elettronica", 
        "immagine_url": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/airpods-pro-3-hero-select-202509_FMT_WHH?wid=752&hei=636&fmt=jpeg&qlt=90&.v=1758077264181",
        "descrizione": "Immergiti nella tua musica preferita con queste cuffie wireless. Tecnologia di cancellazione attiva del rumore (ANC) e fino a 30 ore di autonomia.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Mouse Wireless Ergonomico", 
        "prezzo_lordo": 99.90, 
        "categoria": "elettronica", 
        "immagine_url": "https://resource.logitech.com/c_fill,q_auto,f_auto,dpr_1.0/d_transparent.gif/content/dam/logitech/en/products/mice/mx-vertical/gallery/mx-vertical-gallery-04.png",
        "descrizione": "Mouse senza fili progettato per il massimo comfort. Sensore ottico di precisione e rotellina di scorrimento silenziosa. Compatibile con Windows e macOS.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Tastiera Meccanica Retroilluminata RGB", 
        "prezzo_lordo": 65.50, 
        "categoria": "elettronica", 
        "immagine_url": "https://coffeekeys.eu/cdn/shop/files/DSC03210_b99ccbeb-2243-45a9-bb2b-e5ccf86bbda2.webp?v=1750089673&width=1800",
        "descrizione": "Tastiera da gaming con switch meccanici per una risposta tattile superiore. Retroilluminazione RGB personalizzabile e layout italiano.",
        "quantita": random.randint(35, 100)
    },    { 
        "nome": "Set di 3 Asciugamani in Cotone Egiziano", 
        "prezzo_lordo": 29.99, 
        "categoria": "casa", 
        "immagine_url": "https://www.lisolastore.it/cdn/shop/products/coppia-di-spugna-in-cotone-egiziano-egoist-coppia-di-spugna-graccioza-877133.jpg?crop=center&height=3847&v=1648826873&width=3847",
        "descrizione": "Morbido set di tre asciugamani (viso, ospite, telo doccia) in puro cotone egiziano. Massima assorbenza e comfort sulla pelle.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Flacone Detersivo per Piatti (1L)", 
        "prezzo_lordo": 1.89, 
        "categoria": "casa", 
        "immagine_url": "https://content.dambros.it/uploads/2023/03/20093818/0000217782.png",
        "descrizione": "Detersivo liquido concentrato per la pulizia di piatti e stoviglie. Formula sgrassante efficace anche in acqua fredda. Profumazione al limone.",
        "quantita": random.randint(35, 100)
    },
{ 
        "nome": "Apple Watch Ultra 2", 
        "prezzo_lordo":729.99, 
        "categoria": "elettronica", 
        "immagine_url": "https://static.comet.it/b2c/public/e-cat/APL03770Z/APL03770Z-ab74f87efd-0.jpg",
        "descrizione": "Tieni traccia dei tuoi allenamenti e notifiche. Display a colori ad alta risoluzione, monitoraggio della frequenza cardiaca e GPS integrato.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Power Bank Portatile 10000mAh", 
        "prezzo_lordo": 19.99, 
        "categoria": "elettronica", 
        "immagine_url": "https://m.media-amazon.com/images/I/51ff4eEtmeL._UF1000,1000_QL80_.jpg",
        "descrizione": "Non rimanere mai senza batteria. Caricatore portatile compatto con due porte USB per ricaricare i tuoi dispositivi ovunque ti trovi.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Webcam Full HD 1080p con Microfono", 
        "prezzo_lordo": 35.00, 
        "categoria": "elettronica", 
        "immagine_url": "https://m.media-amazon.com/images/I/71eGb1FcyiL._UF894,1000_QL80_.jpg",
        "descrizione": "Perfetta per videochiamate e streaming. Risoluzione Full HD, microfono integrato con riduzione del rumore e clip universale per monitor.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Set 6 Bicchieri da Acqua in Vetro", 
        "prezzo_lordo": 14.99, 
        "categoria": "casa", 
        "immagine_url": "https://media-gommalacca.r1-it.storage.cloud.it/uploads/2021/07/gw05tdisegual-bicchiere-acqua-vetro-trasparente-800x534.jpg",
        "descrizione": "Set di sei bicchieri in vetro resistente dal design moderno ed elegante. Perfetti per l'uso quotidiano. Lavabili in lavastoviglie.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Moka Caffettiera 3 Tazze", 
        "prezzo_lordo": 18.90, 
        "categoria": "casa", 
        "immagine_url": "https://m.media-amazon.com/images/I/71cQb7iaMOL.jpg",
        "descrizione": "La caffettiera tradizionale per un caffè italiano dal gusto autentico. Realizzata in alluminio di alta qualità con manico ergonomico.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Padella Antiaderente 24cm", 
        "prezzo_lordo": 22.50, 
        "categoria": "casa", 
        "immagine_url": "https://cucinosano.it/cdn/shop/files/Padella_24_Cucinosano_1.webp?v=1717592771",
        "descrizione": "Padella con rivestimento antiaderente rinforzato per una cottura uniforme senza grassi. Adatta a tutti i piani cottura, inclusa l'induzione.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Pellicola Trasparente per Alimenti (30m)", 
        "prezzo_lordo": 1.20, 
        "categoria": "casa", 
        "immagine_url": "https://www.cicalia.com/it/img/imgproducts/46752/l_46752.jpg",
        "descrizione": "Pellicola per alimenti extra resistente per conservare la freschezza dei tuoi cibi. Pratico sistema di taglio per un utilizzo facile e veloce.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Yogurt Greco Bianco 0% Grassi (170g)", 
        "prezzo_lordo": 1.19, 
        "categoria": "food", 
        "immagine_url": "https://www.carrefour.it/on/demandware.static/-/Sites-carrefour-master-catalog-IT/default/dw9adf1027/large/FAGETOTAL0450GR-5201054017616-1.png",
        "descrizione": "Yogurt greco colato, denso e cremoso, senza grassi. Ricco di proteine, perfetto per una colazione sana o uno spuntino leggero.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Confezione di Uova Fresche Biologiche (6 pz)", 
        "prezzo_lordo": 3.20, 
        "categoria": "food", 
        "immagine_url": "https://www.aiafood.com/_next/image/?url=https%3A%2F%2Fbackoffice.aiafood.com%2Fuploads%2Fxxl_B5172_6_uova_bio_703030780d.webp&w=1920&q=80",
        "descrizione": "Uova fresche da galline allevate all'aperto con metodo biologico. Ideali per ogni preparazione, dalla colazione alla pasticceria.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Succo di Arancia 100% Frutta (1L)", 
        "prezzo_lordo": 1.89, 
        "categoria": "food", 
        "immagine_url": "https://www.tigros.it/photo2/2022/11/04/0/main/large/pim-00000005410188019162-main-20221103-200326.jpg",
        "descrizione": "Spremuta di arance 100% frutta senza zuccheri aggiunti. Una fonte naturale di Vitamina C per iniziare la giornata con energia.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Caffè Macinato Qualità Oro (250g)", 
        "prezzo_lordo": 4.50, 
        "categoria": "food", 
        "immagine_url": "https://caffecorsini.com/cdn/shop/files/DCC189_shop.jpg?v=1714378657&width=2048",
        "descrizione": "Pregiata miscela di caffè 100% Arabica dal gusto dolce e aromatico. Macinatura ideale per moka, per un espresso a regola d'arte.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Mozzarella Fresca di Bufala (125g)", 
        "prezzo_lordo": 2.80, 
        "categoria": "food", 
        "immagine_url": "https://www.galbani.ch/wp-content/uploads/2018/04/01-3D-Mozzarella-di-Bufala-DOP-frontal-view_2025-1.png",
        "descrizione": "Autentica mozzarella di bufala campana DOP. Sapore ricco e consistenza morbida, perfetta da gustare da sola o in una caprese.",
        "quantita": random.randint(35, 100)
    },
    { 
        "nome": "Olio Extra Vergine di Oliva (750ml)", 
        "prezzo_lordo": 8.99, 
        "categoria": "food", 
        "immagine_url": "https://static.planeat.eco/media/planeat_it_mi/item_pics/olio-extra-vergine-di-oliva-600x400.jpg",
        "descrizione": "Olio EVO estratto a freddo da olive 100% italiane. Gusto fruttato ed equilibrato, ideale per condire a crudo insalate, verdure e bruschette.",
        "quantita": random.randint(35, 100)
    }
]
if admin_email and admin_password:
    # Controlla se l'admin esiste già
    admin_user = utenti_collection.find_one({'email': admin_email})
    
    if not admin_user:
        print(f"Creazione dell'utente amministratore: {admin_email}")
        utenti_collection.insert_one({
            'email': admin_email,
            'password': generate_password_hash(admin_password),
            'nome': 'Admin',
            'cognome': 'User',
            'ruolo': 'admin',  # Assegnazione del ruolo di admin
            'indirizzo': '',
            'citta': '',
            'carrello': [],
            'preferiti': []
        })
    else:
        print(f"Utente amministratore '{admin_email}' già esistente.")
else:
    print("ATTENZIONE: Credenziali ADMIN_EMAIL e ADMIN_PASSWORD non trovate nel file .env. Admin non creato.")

collection.create_index([('nome', 'text')])

collection.insert_many(prodotti_da_inserire)

print(f"Database popolato con {len(prodotti_da_inserire)} prodotti (link manuali).")
client.close()