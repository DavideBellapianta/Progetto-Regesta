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
        add: (prodotto) => //Aggiunge il prodotto al carrello
            update((items) => {
                const itemInCart = items.find((i) => i.nome === prodotto.nome);
                if (itemInCart) itemInCart.quantita += 1;
                else items.push({ ...prodotto, quantita: 1 });
                saveCartToDB(items);
                return items;
            }),
        remove: (nome) => //Rimuove il prodotto dal carrello
            update((items) => {
                const updatedItems = items.filter((i) => i.nome !== nome);
                saveCartToDB(updatedItems);
                return updatedItems;
            }),

        increment: (nomeProdotto) => //Incrementa la quantità del prodotto nel carrello
            update((items) => {
                const itemInCart = items.find((i) => i.nome === nomeProdotto);
                if (itemInCart) {
                    itemInCart.quantita += 1;
                }
                saveCartToDB(items);
                return items;
            }),

        decrement: (nomeProdotto) => //Decrementa la quantità del prodotto nel carrello
            update((items) => {
                const itemInCart = items.find((i) => i.nome === nomeProdotto);
                if (itemInCart && itemInCart.quantita > 1) {
                    itemInCart.quantita -= 1;
                    saveCartToDB(items);
                    return items;
                } else {
                    const updatedItems = items.filter((i) => i.nome !== nomeProdotto);
                    saveCartToDB(updatedItems);
                    return updatedItems;
                }
            }),

        reset: () => { //Svuota il carrello
            set([]);
            saveCartToDB([]);
        }
    };
}

function createUtenteStore() {
    const { subscribe, set } = writable(null);

    return {
        subscribe,
        login: async (email, password) => { //chiama il backend per il login
            let localCart = [];
            const unsubscribe = cart.subscribe(value => {
                localCart = value;
            });
            unsubscribe();

            const response = await fetch(`${API_BASE_URL}/api/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                if (browser) localStorage.setItem('jwt_token', data.access_token); //salva il token
                set({ email });

                let cartFromDB = data.carrello || [];

                localCart.forEach(localItem => {
                    const itemInDB = cartFromDB.find(dbItem => dbItem.nome === localItem.nome);
                    if (itemInDB) {
                        itemInDB.quantita += localItem.quantita;
                    } else {
                        cartFromDB.push(localItem);
                    }
                });

                cart.set(cartFromDB);

            } else {
                throw new Error('Login fallito. Controlla le credenziali.');
            }
        },
        logout: () => { //effettua il logout e rimuove il token
            if (browser) {
                localStorage.removeItem('jwt_token'); 
            }
            cart.reset(); 
            set(null);
        },

        checkAuth: async () => { //Se esiste un token lo verifica con il backend
            if (!browser) return;

            const token = localStorage.getItem('jwt_token');

            if (token) {
                try {
                    const response = await fetch(`${API_BASE_URL}/api/profilo`, {
                        headers: { Authorization: `Bearer ${token}` }
                    });

                    if (response.ok) {
                        const userProfile = await response.json();
                        set({ email: userProfile.email }); 
                        cart.set(userProfile.carrello || []); 
                        favorites.set(new Set(userProfile.preferiti || []));
                    } else {
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
//
    async function saveFavoritesToDB(itemsSet) { //Salva i preferiti nel database
        if (!browser) return;
        const token = localStorage.getItem('jwt_token');
        if (token) {
            try {
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
        set, 
        toggle: (prodotto) => {
            update((items) => {
                if (items.has(prodotto.nome)) {
                    items.delete(prodotto.nome);
                } else {
                    items.add(prodotto.nome);
                }
                saveFavoritesToDB(items); 
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