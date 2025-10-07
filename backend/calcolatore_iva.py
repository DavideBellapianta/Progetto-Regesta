import math
from decimal import Decimal, ROUND_DOWN

# Dizionario con le aliquote IVA per categoria
ALIQUOTE_IVA = {
    "food": Decimal("0.04"),      # 4% per cibo e bevande
    "medical": Decimal("0.10"),   # 10% per prodotti medici
    "other": Decimal("0.22")      # 22% per tutte le altre categorie
}

# Un "centesimo" rappresentato come Decimal per i calcoli
CENT = Decimal("0.01")

def arrotonda_a_005_inferiore(valore: Decimal) -> Decimal:
    """
    Arrotonda un valore per difetto al multiplo di 0.05 più vicino.
    Esempio: 6.09€ -> 6.05€; 6.04€ -> 6.00€
    """
    # Moltiplichiamo per 20 (1 / 0.05), arrotondiamo per difetto all'intero e dividiamo di nuovo per 20.
    return (valore * 20).to_integral_value(rounding=ROUND_DOWN) / 20

def calcola_scontrino(carrello: list, collection_prodotti) -> dict:
    """
    Calcola i dettagli dello scontrino basandosi sul carrello e sui prodotti nel database.

    Args:
        carrello: Una lista di dizionari, es. [{'nome': 'chocolate bar', 'quantita': 2}, ...]
        collection_prodotti: La collezione MongoDB da cui recuperare i dettagli dei prodotti.

    Returns:
        Un dizionario con i dettagli dello scontrino.
    """
    dettagli_scontrino = []
    totale_netto_finale = Decimal("0.00")
    totale_tasse_finale = Decimal("0.00")

    for item_carrello in carrello:
        nome_prodotto = item_carrello["nome"]
        quantita = int(item_carrello["quantita"])

        # Recupera i dettagli del prodotto dal database
        prodotto_db = collection_prodotti.find_one({"nome": nome_prodotto})
        if not prodotto_db:
            # Salta il prodotto se non viene trovato nel database
            continue

        prezzo_lordo_unitario = Decimal(str(prodotto_db["prezzo_lordo"]))
        categoria = prodotto_db["categoria"]
        aliquota_iva = ALIQUOTE_IVA.get(categoria, ALIQUOTE_IVA["other"])

        # Calcola i totali per la riga corrente
        prezzo_lordo_riga = prezzo_lordo_unitario * quantita
        prezzo_netto_riga_non_arrotondato = prezzo_lordo_riga * (1 + aliquota_iva)

        # Applica la regola di arrotondamento speciale
        prezzo_netto_riga_arrotondato = arrotonda_a_005_inferiore(prezzo_netto_riga_non_arrotondato)
        
        # Regola di controllo: il prezzo finale non può essere inferiore a quello lordo
        if prezzo_netto_riga_arrotondato < prezzo_lordo_riga:
             # In casi molto rari con prezzi bassissimi, l'arrotondamento potrebbe violare la regola.
             # In tal caso, si arrotonda al centesimo superiore.
             prezzo_netto_riga_arrotondato = prezzo_lordo_riga.quantize(CENT, rounding=ROUND_UP)

        # Calcola l'importo delle tasse per questa riga come differenza
        tasse_riga = prezzo_netto_riga_arrotondato - prezzo_lordo_riga

        # Aggiungi ai totali finali
        totale_netto_finale += prezzo_netto_riga_arrotondato
        totale_tasse_finale += tasse_riga

        dettagli_scontrino.append({
            "nome": nome_prodotto,
            "quantita": quantita,
            "prezzo_finale_riga": f"{prezzo_netto_riga_arrotondato:.2f}€"
        })

    # Prepara l'oggetto finale da restituire
    risultato = {
        "righe": dettagli_scontrino,
        "totale_tasse": f"{totale_tasse_finale:.2f}€",
        "totale_netto": f"{totale_netto_finale:.2f}€"
    }

    return risultato