-- Tabella per le Categorie dei Prodotti
CREATE TABLE Categorie (
    id_categoria INT AUTO_INCREMENT,
    nome_categoria VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY (id_categoria)
);

-- Tabella per gli Utenti
CREATE TABLE Utenti (
    id_utente INT AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    cognome VARCHAR(100) NOT NULL,
    indirizzo VARCHAR(255),
    citta VARCHAR(100),
    ruolo VARCHAR(20) NOT NULL DEFAULT 'utente',
    PRIMARY KEY (id_utente)
);

-- Tabella per i Prodotti
CREATE TABLE Prodotti (
    id_prodotto INT AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    prezzo_lordo DECIMAL(10, 2) NOT NULL,
    descrizione TEXT,
    immagine_url VARCHAR(2083),
    quantita_disponibile INT NOT NULL DEFAULT 0,
    id_categoria INT,
    PRIMARY KEY (id_prodotto),
    FOREIGN KEY (id_categoria) REFERENCES Categorie(id_categoria) ON DELETE SET NULL
);

-- Tabella per gli Ordini
CREATE TABLE Ordini (
    id_ordine INT AUTO_INCREMENT,
    id_utente INT NOT NULL,
    data_ordine DATETIME NOT NULL,
    totale_netto DECIMAL(10, 2) NOT NULL,
    totale_tasse DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (id_ordine),
    FOREIGN KEY (id_utente) REFERENCES Utenti(id_utente) ON DELETE CASCADE
);

-- Tabella Associativa per i Dettagli dell'Ordine
CREATE TABLE DettagliOrdine (
    id_dettaglio INT AUTO_INCREMENT,
    id_ordine INT NOT NULL,
    id_prodotto INT NOT NULL,
    quantita_acquistata INT NOT NULL,
    prezzo_al_momento DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (id_dettaglio),
    FOREIGN KEY (id_ordine) REFERENCES Ordini(id_ordine) ON DELETE CASCADE,
    FOREIGN KEY (id_prodotto) REFERENCES Prodotti(id_prodotto) ON DELETE RESTRICT
);

-- Tabella Associativa per i Preferiti
CREATE TABLE Preferiti (
    id_utente INT NOT NULL,
    id_prodotto INT NOT NULL,
    PRIMARY KEY (id_utente, id_prodotto),
    FOREIGN KEY (id_utente) REFERENCES Utenti(id_utente) ON DELETE CASCADE,
    FOREIGN KEY (id_prodotto) REFERENCES Prodotti(id_prodotto) ON DELETE CASCADE
);