# 🛒 POS REGISTER REGESTA
<div align="center">

[![Version](https://img.shields.io/badge/version-1.0.0-blue)]()
[![Python](https://img.shields.io/badge/python-3.8+-blue)]()
[![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-green)]()

</div>

> **Sistema di E-Commerce Completo con Gestione POS**

Un'applicazione web moderna per la gestione di vendite online con funzionalità complete di catalogo, carrello e sistema di pagamento.
[Manuale d'uso](https://docs.google.com/document/d/1D-iD6ySRSMTE_2vF7IYUspjGktVcQ5FYHsPTtpqSHIg/edit?usp=sharing) [TDD/BDD](https://docs.google.com/document/d/1WCHKvUJXN33FFV7T_rbOO9tqv_enCzUocbcRUm5gYcU/edit?usp=sharing)
<div align="center">

### Homepage - Catalogo Prodotti
![Homepage](frontend/src/lib/assets/Screenshot1.png)

### Carrello e Checkout
![Cart](frontend/src/lib/assets/Screenshot2.png)

</div>

---

## 🚀 Funzionalità

### 🔐 **Autenticazione**
- 📧 **Registrazione** tramite email e password
- 🔑 **Login** per utenti registrati
- 👤 **Aggiornamento profilo** (Nome, cognome, telefono, indirizzo, CAP e paese)

### 🛍️ **Catalogo Prodotti**
- 🏠 **Homepage** con prodotti organizzati per categorie
- 🔍 **Ricerca avanzata** per nome, costo o categoria
- 📋 **Dettaglio prodotto** con specifiche complete e recensioni
- ⭐ **Sistema preferiti** per salvare prodotti preferiti

### 💸 **Carrello e Acquisti**
- 🎯 **Carrello dinamico** con modifica quantità in tempo reale
- ➕➖ **Aggiunta/rimozione** prodotti dal carrello
- ❤️ **Gestione preferiti** direttamente dal carrello
- ✅ **Checkout sicuro** con inserimento dati di pagamento
- 📊 **Riepilogo ordine** prima del completamento

### 🧾 **Pagamenti e Scontrino**
- 📄 **Profilo utente** con storico ordini completo
- 🖨️ **Stampa scontrini** per acquisti effettuati
- ⚙️ **Gestione dati personali** e preferenze

## 👑 **Gestione Amministratore**
- 🛡️ Accesso basato su ruoli con poteri specifici per gli amministratori.
- 📊 Pannello di controllo integrato nella pagina profilo per la gestione del magazzino.
- ⚠️ Monitoraggio scorte critiche con visualizzazione prioritaria dei prodotti esauriti o in backorder.
- ⬆️ Funzionalità di Restock rapida per rifornire i prodotti direttamente dal pannello.
- 📝 Gestione catalogo (CRUD) tramite API protette per aggiungere, modificare o eliminare prodotti.

---

## 🛠️ Tecnologie

- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Python
- **Database:** MongoDB
- **Authentication:** JWT

## 🧪 Testing
- **Test Automatici**: Inclusa un'applicazione dedicata in Python (Selenium) per testare le funzionalità principali del servizio.








