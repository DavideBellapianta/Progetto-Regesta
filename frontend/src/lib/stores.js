// src/lib/stores.js
import { writable, derived } from 'svelte/store';
import { browser } from '$app/environment';

const API_BASE_URL = 'http://127.0.0.1:5000';

function createCart() {
    const { subscribe, set, update } = writable([]);

    async function saveCartToDB(items) {
        if (!browser) return;
        const token = localStorage.getItem('jwt_token');
        if (token) { // Salva il carrello solo se l'utente è loggato
            try {
                await fetch(`${API_BASE_URL}/api/carrello`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
                    body: JSON.stringify(items)
                });
            } catch (e) {
                console.error("Impossibile salvare il carrello:", e);
            }
        }
    }
    return {
        subscribe,
        set,
        add: (prodotto) =>
            update((items) => {
                const itemInCart = items.find((i) => i.nome === prodotto.nome);
                if (itemInCart) itemInCart.quantita += 1;
                else items.push({ ...prodotto, quantita: 1 });
                saveCartToDB(items);
                return items;
            }),
        remove: (nome) =>
            update((items) => {
                const updatedItems = items.filter((i) => i.nome !== nome);
                saveCartToDB(updatedItems);
                return updatedItems;
            }),

        // ===== FUNZIONE INCREMENT COMPLETATA =====
        increment: (nomeProdotto) =>
            update((items) => {
                const itemInCart = items.find((i) => i.nome === nomeProdotto);
                if (itemInCart) {
                    itemInCart.quantita += 1;
                }
                saveCartToDB(items);
                return items;
            }),

        // ===== FUNZIONE DECREMENT COMPLETATA =====
        decrement: (nomeProdotto) =>
            update((items) => {
                const itemInCart = items.find((i) => i.nome === nomeProdotto);
                if (itemInCart && itemInCart.quantita > 1) {
                    // Se la quantità è maggiore di 1, semplicemente la decrementiamo
                    itemInCart.quantita -= 1;
                    saveCartToDB(items);
                    return items;
                } else {
                    // Altrimenti (se la quantità è 1), rimuoviamo l'articolo dal carrello
                    const updatedItems = items.filter((i) => i.nome !== nomeProdotto);
                    saveCartToDB(updatedItems);
                    return updatedItems;
                }
            }),

        reset: () => {
            set([]);
            saveCartToDB([]);
        }
    };
}

function createUtenteStore() {
    const { subscribe, set } = writable(null);

    return {
        subscribe,
        login: async (email, password) => {
            // 1. Salva una copia del carrello locale PRIMA del login
            let localCart = [];
            const unsubscribe = cart.subscribe(value => {
                localCart = value;
            });
            unsubscribe(); // Annulla l'iscrizione subito dopo aver letto il valore

            const response = await fetch(`${API_BASE_URL}/api/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                if (browser) localStorage.setItem('jwt_token', data.access_token);
                set({ email });

                // 2. Unisci il carrello del database con quello locale
                let cartFromDB = data.carrello || [];

                localCart.forEach(localItem => {
                    const itemInDB = cartFromDB.find(dbItem => dbItem.nome === localItem.nome);
                    if (itemInDB) {
                        // Se l'articolo esiste già, somma le quantità
                        itemInDB.quantita += localItem.quantita;
                    } else {
                        // Altrimenti, aggiungi l'articolo locale al carrello del DB
                        cartFromDB.push(localItem);
                    }
                });

                // 3. Imposta il carrello unito come nuovo stato e salvalo
                cart.set(cartFromDB);

            } else {
                throw new Error('Login fallito. Controlla le credenziali.');
            }
        },
        logout: () => {
            if (browser) {
                localStorage.removeItem('jwt_token'); // Rimuove il token dal "blocco note"
            }
            cart.reset(); // Svuota il carrello
            set(null); // Imposta lo stato utente a 'non loggato'
        },

        // --- FUNZIONE CHECKAUTH (COMPLETATA) ---
        checkAuth: async () => {
            if (!browser) return;

            const token = localStorage.getItem('jwt_token'); // Controlla se c'è un token salvato

            if (token) {
                try {
                    // Usa il token per chiedere al backend "chi sono?"
                    const response = await fetch(`${API_BASE_URL}/api/profilo`, {
                        headers: { Authorization: `Bearer ${token}` }
                    });

                    if (response.ok) {
                        const userProfile = await response.json();
                        set({ email: userProfile.email }); // Autentica l'utente
                        cart.set(userProfile.carrello || []); // Carica il suo carrello salvato
                        favorites.set(new Set(userProfile.preferiti || []));
                    } else {
                        // Se il token non è valido (es. scaduto), pulisci tutto
                        localStorage.removeItem('jwt_token');
                        set(null);
                    }
                } catch (e) {
                    console.error('Errore durante il check dell\'autenticazione:', e);
                    localStorage.removeItem('jwt_token');
                    set(null);
                }
            }
        }
    };
}

export const utente = createUtenteStore();

export const cart = createCart();

export const cartItemsCount = derived(cart, ($cart) => {
    if (!$cart) return 0;
    return $cart.reduce((sum, item) => sum + item.quantita, 0);
});
export const isCartOpenMobile = writable(false);

function createFavoritesStore() {
    const { subscribe, set, update } = writable(new Set());

    async function saveFavoritesToDB(itemsSet) {
        if (!browser) return;
        const token = localStorage.getItem('jwt_token');
        if (token) {
            try {
                // Convertiamo il Set in un Array per inviarlo come JSON
                const itemsArray = Array.from(itemsSet);
                await fetch(`${API_BASE_URL}/api/preferiti`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
                    body: JSON.stringify(itemsArray)
                });
            } catch (e) {
                console.error("Impossibile salvare i preferiti:", e);
            }
        }
    }

    return {
        subscribe,
        set, // Esponiamo 'set' per poter caricare i dati al login
        toggle: (prodotto) => {
            update((items) => {
                if (items.has(prodotto.nome)) {
                    items.delete(prodotto.nome);
                } else {
                    items.add(prodotto.nome);
                }
                saveFavoritesToDB(items); // Salva le modifiche sul DB
                return items;
            });
        },
        reset: () => {
            set(new Set());
            saveFavoritesToDB(new Set());
        }
    };
}


export const favorites = createFavoritesStore();