from decimal import Decimal, ROUND_DOWN, ROUND_UP

ALIQUOTE_IVA = {
    "food": Decimal("0.04"),
    "medical": Decimal("0.10"),
    "other": Decimal("0.22")
}

def arrotonda_a_005_inferiore(valore: Decimal) -> Decimal:
    return (valore * 20).to_integral_value(rounding=ROUND_DOWN) / 20

def calcola_scontrino(carrello: list, collection_prodotti: object) -> dict:
    righe = []
    totale_netto = Decimal("0.00")
    totale_tasse = Decimal("0.00")

    for item in carrello:
        prodotto_db = collection_prodotti.find_one({"nome": item["nome"]})
        if not prodotto_db:
            continue

        prezzo_lordo = Decimal(str(prodotto_db["prezzo_lordo"]))
        quantita = Decimal(item["quantita"])
        categoria = prodotto_db["categoria"]
        
        aliquota_iva = ALIQUOTE_IVA.get(categoria, ALIQUOTE_IVA["other"])
        
        prezzo_lordo_riga = prezzo_lordo * quantita
        prezzo_con_iva = prezzo_lordo_riga * (Decimal("1") + aliquota_iva)
        
        prezzo_finale_arrotondato = arrotonda_a_005_inferiore(prezzo_con_iva)
        
        if prezzo_finale_arrotondato < prezzo_lordo_riga:
             prezzo_finale_arrotondato = prezzo_lordo_riga.quantize(Decimal("0.01"), rounding=ROUND_UP)

        tasse_riga = prezzo_finale_arrotondato - prezzo_lordo_riga
        
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