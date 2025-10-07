// src/lib/stores.js
import { writable, derived } from 'svelte/store';

function createCart() {
    const { subscribe, set, update } = writable([]);

    return {
        subscribe,
        // Funzione per aggiungere/incrementare
        add: (prodotto) => {
            update((items) => {
                const itemInCart = items.find((item) => item.nome === prodotto.nome);
                if (itemInCart) {
                    itemInCart.quantita += 1;
                } else {
                    items.push({ ...prodotto, quantita: 1 });
                }
                return items;
            });
        },
        // Funzione per rimuovere un articolo
        remove: (nomeProdotto) => {
            update((items) => items.filter((item) => item.nome !== nomeProdotto));
        },
        // Funzione per incrementare la quantità
        increment: (nomeProdotto) => {
            update((items) => {
                const itemInCart = items.find((item) => item.nome === nomeProdotto);
                if (itemInCart) itemInCart.quantita += 1;
                return items;
            });
        },
        // Funzione per decrementare la quantità (rimuove l'articolo se la quantità è 1)
        decrement: (nomeProdotto) => {
            update((items) => {
                const itemInCart = items.find((item) => item.nome === nomeProdotto);
                if (itemInCart && itemInCart.quantita > 1) {
                    itemInCart.quantita -= 1;
                    return items;
                }
                return items.filter((item) => item.nome !== nomeProdotto);
            });
        },
        reset: () => set([])
    };
}

export const cart = createCart();

export const cartItemsCount = derived(cart, ($cart) => {
    if (!$cart) return 0;
    return $cart.reduce((sum, item) => sum + item.quantita, 0);
});
export const isCartOpenMobile = writable(false);

function createFavoritesStore() {
    // Inizializziamo lo store con un Set per gestire facilmente l'unicità dei prodotti
    const { subscribe, update, set } = writable(new Set());

    return {
        subscribe,
        // Funzione per aggiungere/rimuovere un prodotto dai preferiti
        toggle: (prodotto) => {
            update((items) => {
                if (items.has(prodotto.nome)) {
                    // Se il prodotto è già nei preferiti, lo rimuoviamo
                    items.delete(prodotto.nome);
                    console.log(`Rimosso '${prodotto.nome}' dai preferiti`);
                } else {
                    // Altrimenti, lo aggiungiamo
                    items.add(prodotto.nome);
                    console.log(`Aggiunto '${prodotto.nome}' ai preferiti`);
                }
                return items; // Restituisce il Set aggiornato
            });
        },
        reset: () => set(new Set())
    };
}

export const favorites = createFavoritesStore();