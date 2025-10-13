from decimal import Decimal, ROUND_DOWN, ROUND_UP #Meglio decimal di flaot per essere più precisi

ALIQUOTE_IVA = {
    "food": Decimal("0.04"),
    "medical": Decimal("0.10"),
    "other": Decimal("0.22"),
    "casa": Decimal("0.22"),
    "elettronica": Decimal("0.22"),
}

def arrotonda_a_005_inferiore(valore: Decimal) -> Decimal:
    return (valore * 20).to_integral_value(rounding=ROUND_DOWN) / 20 #Arrotondo per difetto tipo 1,28 * 20 = 25,6 si arrotonda a 25 poi / 20 = 1,25 

def calcola_scontrino(carrello: list, collection_prodotti: object) -> dict:
    righe = []
    totale_netto = Decimal("0.00")
    totale_tasse = Decimal("0.00")

    for item in carrello:
        prodotto_db = collection_prodotti.find_one({"nome": item["nome"]}) #Cerca per nome i prodotti
        if not prodotto_db:
            continue

        prezzo_lordo = Decimal(str(prodotto_db["prezzo_lordo"]))
        quantita = Decimal(item["quantita"])
        categoria = prodotto_db["categoria"]
        
        aliquota_iva = ALIQUOTE_IVA.get(categoria, ALIQUOTE_IVA["other"]) #calcola il prezzo con iva tramite categorie
        
        prezzo_lordo_riga = prezzo_lordo * quantita
        prezzo_con_iva = prezzo_lordo_riga * (Decimal("1") + aliquota_iva)
        
        prezzo_finale_arrotondato = arrotonda_a_005_inferiore(prezzo_con_iva) #arrotonda
        
        if prezzo_finale_arrotondato < prezzo_lordo_riga:
             prezzo_finale_arrotondato = prezzo_lordo_riga.quantize(Decimal("0.01"), rounding=ROUND_UP) #mi assicuro di non perdere valore (senza tasse)

        tasse_riga = prezzo_finale_arrotondato - prezzo_lordo_riga #Prezzo finale - prezzo senza tasse = tasse
        
        totale_netto += prezzo_finale_arrotondato
        totale_tasse += tasse_riga
        
        righe.append({
            "nome": item["nome"],
            "quantita": int(quantita),
            "prezzo_finale_riga": f"{prezzo_finale_arrotondato:.2f}€"
        })
        
    return {
        "righe": righe,
        "totale_tasse": f"{totale_tasse:.2f}€",
        "totale_netto": f"{totale_netto:.2f}€"
    }