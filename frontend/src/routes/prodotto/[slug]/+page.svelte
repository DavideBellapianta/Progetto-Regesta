<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { cart, favorites } from '$lib/stores.js';
    import Review from '$lib/components/Review.svelte';
    import cuore_vuoto from '$lib/assets/heart_vuoto.png';
    import cuore_rosso from '$lib/assets/heart_pieno_rosso.png';

    let prodotto = null;
    let error = null;
    let isFavorite = false;
    let quantitaRimanente = null;

    const nomi = ['Marco', 'Laura', 'Luca', 'Giulia', 'Alessandro', 'Chiara', 'Matteo', 'Sara', 'Davide', 'Federica', 'Simone', 'Elisa', 'Andrea', 'Valentina', 'Riccardo', 'Marta'];
    const cognomi = ['R.', 'B.', 'M.', 'F.', 'C.', 'G.', 'S.', 'L.', 'P.', 'D.', 'V.', 'T.', 'Z.', 'N.'];

    const templates = { //Varii template per le recensioni
        food: {
            pro: [
                'Gusto eccezionale, si sente la qualità degli ingredienti.',
                'Sapore autentico, come fatto in casa. Tutta la famiglia lo ha apprezzato.',
                'Molto buono e fresco, la confezione era pratica e ben sigillata.',
                'Il migliore che abbia mai provato! Vale ogni centesimo speso.',
                'Ottimo per uno spuntino veloce e salutare.',
                'Ingredienti di prima scelta, un prodotto davvero superiore.',
                'Consegna rapidissima e prodotto arrivato in perfette condizioni.'
            ],
            con: [
                'Il sapore è un po’ anonimo rispetto ad altre marche.',
                'Un po\' troppo caro per la quantità offerta.',
                'La confezione è arrivata leggermente danneggiata.',
                'Non mi ha convinto del tutto, mi aspettavo di più.',
                'Scadenza un po\' troppo ravvicinata per i miei gusti.',
                'Gusto troppo forte, non incontra le mie preferenze.'
            ]
        },
        medical: {
            pro: [
                'Prodotto efficace e facile da usare, ha risolto il mio problema in poco tempo.',
                'Indispensabile da tenere in casa per ogni evenienza. Consigliatissimo.',
                'Mi è stato consigliato dal medico e devo dire che è un prodotto validissimo.',
                'Fa quello che promette, ottimo rapporto qualità-prezzo.',
                'Spedizione rapida e prodotto conforme alla descrizione. Fa il suo dovere.',
                'Nessun effetto collaterale, molto delicato.'
            ],
            con: [
                'Su di me non ha avuto l\'effetto sperato. Molto deludente.',
                'L\'odore è un po\' sgradevole, difficile da sopportare.',
                'Le istruzioni all\'interno non erano molto chiare.',
                'Prezzo eccessivo rispetto a prodotti simili che si trovano in farmacia.',
                'La confezione era difficile da aprire.'
            ]
        },
        elettronica: {
            pro: [
                'Performance incredibili, veloce e reattivo. Superiore alle aspettative.',
                'La batteria dura tantissimo, anche con un uso intenso.',
                'Si connette subito e non perde mai il segnale. Un prodotto davvero affidabile.',
                'Installazione semplicissima, ha funzionato al primo colpo. Lo adoro.',
                'Bello esteticamente, design moderno e materiali di qualità.',
                'Il display è luminoso e i colori sono brillanti.'
            ],
            con: [
                'Il software è un po\' da migliorare, qualche bug occasionale.',
                'I materiali sembrano un po\' economici al tatto, scricchiola.',
                'È molto più piccolo di quanto pensassi guardando le foto.',
                'Si surriscalda un po\' dopo un uso prolungato.',
                'Mancava un cavo nella confezione, ho dovuto comprarlo a parte.'
            ]
        },
        casa: {
            pro: [
                'Prodotto di grande utilità in cucina, mi ha semplificato la vita.',
                'Robusto, facile da pulire e ben costruito. Sembra durevole.',
                'Si abbina perfettamente all\'arredamento del mio salotto, design azzeccato.',
                'Efficace e silenzioso, esattamente come speravo.',
                'Pratico, funzionale e occupa poco spazio. Esattamente quello che mi serviva.',
                'Il montaggio è stato sorprendentemente semplice e veloce.'
            ],
            con: [
                'Le dimensioni non corrispondevano esattamente a quelle indicate.',
                'Il montaggio è stato più complicato del previsto, ci ho messo ore.',
                'Si è rotto dopo pochi utilizzi, qualità davvero deludente.',
                'Il colore è leggermente diverso da quello mostrato online.',
                'Un po\' rumoroso durante il funzionamento.'
            ]
        },
        other: {
            pro: [
                'Materiali di ottima qualità, molto robusto e ben rifinito.',
                'Un prodotto versatile e utile in molte situazioni diverse.',
                'Esattamente quello che cercavo. Arrivato in un giorno, servizio impeccabile.',
                'Facile da usare, le istruzioni erano chiare e semplici.'
            ],
            con: [
                'Il design potrebbe essere migliorato, è un po’ ingombrante.',
                'Qualità pessima, sconsiglio assolutamente l\'acquisto.',
                'È arrivato con un pezzo mancante, ho dovuto contattare l\'assistenza.',
                'Funziona, ma non è nulla di speciale, si trova di meglio.'
            ]
        }
    };

    function generateReviews() {
        const reviews = [];
        const categorie = Object.keys(templates);

        categorie.forEach(category => {
            const numReviews = 6 + Math.floor(Math.random() * 5);

            for (let i = 0; i < numReviews; i++) {
                const autore = `${nomi[Math.floor(Math.random() * nomi.length)]} ${cognomi[Math.floor(Math.random() * cognomi.length)]}`;
                const categoryTemplates = templates[category];
                
                let testo;
                let rating;
                const randomChance = Math.random();

                if (randomChance < 0.6) { //percentuali di stelle
                    testo = categoryTemplates.pro[Math.floor(Math.random() * categoryTemplates.pro.length)];
                    rating = Math.random() < 0.7 ? 5 : 4; 
                } else if (randomChance < 0.85) { 
                    const pro = categoryTemplates.pro[Math.floor(Math.random() * categoryTemplates.pro.length)];
                    const con = categoryTemplates.con[Math.floor(Math.random() * categoryTemplates.con.length)];
                    testo = `${pro} L'unico neo è che ${con.toLowerCase()}`;
                    rating = 3;
                } else { 
                    testo = categoryTemplates.con[Math.floor(Math.random() * categoryTemplates.con.length)];
                    rating = Math.random() < 0.7 ? 1 : 2;
                }

                reviews.push({
                    category: category,
                    author: autore,
                    rating: rating,
                    text: testo
                });
            }
        });
        return reviews;
    }

    const allReviews = generateReviews();

	let averageRating = 0;
    let reviewCount = 0;

    onMount(async () => {
        const slug = $page.params.slug;
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/prodotto/${slug}`); //dati prodotto
            if (response.ok) {
                prodotto = await response.json();
            } else {
                throw new Error(`Prodotto non trovato (${response.status})`);
            }
        } catch (e) {
            console.error('Impossibile caricare il prodotto:', e);
            error = 'Non è stato possibile trovare il prodotto richiesto.';
        }
    });

    async function fetchQuantita(slug) { //richiesta quantità
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/prodotto/${slug}/quantita`);
            if (response.ok) {
                const data = await response.json();
                quantitaRimanente = data.quantita;
            } else {
                quantitaRimanente = 0;
            }
        } catch (e) {
            console.error('Errore nel recupero della quantità:', e);
            quantitaRimanente = 0;
        }
    }

    function toggleFavorite() {
        if (prodotto) favorites.toggle(prodotto); //aggiunge / rimuove dai preferiti
    }
    function addToCart() {
        if (prodotto) cart.add(prodotto); //aggiunge al carrello
    }

    $: if (prodotto) isFavorite = $favorites.has(prodotto.nome);
    $: if (prodotto) {
        fetchQuantita($page.params.slug);

        const relevantReviews = allReviews.filter(review => review.category === prodotto.categoria);
        reviewCount = relevantReviews.length;

        if (reviewCount > 0) {
            const totalRating = relevantReviews.reduce((sum, review) => sum + review.rating, 0);
            averageRating = totalRating / reviewCount;
        } else {
            averageRating = 0;
        }
    }
</script>

<main class="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
    {#if prodotto}
        <div class="grid grid-cols-1 items-start gap-12 md:grid-cols-2">
            <div class="overflow-hidden rounded-lg bg-white shadow-lg">
                <img src={prodotto.immagine_url} alt={prodotto.nome} class="h-auto w-full object-cover" />
            </div>

            <div class="flex flex-col space-y-6">
                <div>
                    <span class="font-semibold uppercase tracking-wide text-indigo-600"
                        >{prodotto.categoria}</span
                    >
                    <h1 class="mt-1 text-4xl font-extrabold tracking-tight text-gray-900">{prodotto.nome}</h1>

                    {#if reviewCount > 0}
                        <div class="mt-3 flex items-center">
                            <div class="flex items-center">
                                {#each { length: 5 } as _, i}
                                    <svg
                                        class="h-6 w-6 flex-shrink-0"
                                        class:text-yellow-400={i < Math.round(averageRating)}
                                        class:text-gray-300={i >= Math.round(averageRating)}
                                        fill="currentColor"
                                        viewBox="0 0 20 20"
                                    >
                                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                    </svg>
                                {/each}
                            </div>
                            <p class="ml-2 text-lg text-gray-600">
                                {averageRating.toFixed(1)} su 5 ({reviewCount} recensioni)
                            </p>
                        </div>
                    {/if}
                    
                    <p class="mt-4 text-3xl font-bold text-gray-800">{prodotto.prezzo_lordo.toFixed(2)}€</p>
                </div>

                <div class="leading-relaxed text-gray-600">
                    <h2 class="mb-2 font-semibold text-gray-800">Descrizione</h2>
                    <p>
                        {prodotto.descrizione}
                    </p>
                </div>

                <div class="flex flex-col space-y-4">
                    <div class="flex items-center space-x-4">
                        <button
                            on:click={addToCart}
                            disabled={quantitaRimanente <= 0}
                            class="flex-1 rounded-lg bg-indigo-600 py-3 text-lg font-semibold text-white transition hover:bg-indigo-700
                disabled:cursor-not-allowed disabled:bg-gray-400"
                        >
                            Aggiungi al carrello
                        </button>

                        <button
                            on:click={toggleFavorite}
                            class="rounded-full border-2 p-3 transition"
                            class:border-red-500={isFavorite}
                            class:border-gray-300={!isFavorite}
                            aria-label={isFavorite ? 'Rimuovi dai preferiti' : 'Aggiungi ai preferiti'}
                        >
                            <img
                                src={isFavorite ? cuore_rosso : cuore_vuoto}
                                alt={isFavorite ? 'Rimuovi dai preferiti' : 'Aggiungi ai preferiti'}
                                class="h-6 w-6"
                            />
                        </button>
                    </div>

                    <div class="mb-2 mt-4 space-y-1 text-lg">
                        {#if quantitaRimanente === null}
                            <div class="flex items-center gap-x-2">
                                <p class="animate-pulse text-slate-600">Verifica disponibilità in corso...</p>
                            </div>
                        {:else if quantitaRimanente > 10}
                            <div class="flex items-center gap-x-2">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    class="h-5 w-5 flex-shrink-0 text-green-600"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                    stroke-width="2"
                                >
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                </svg>
                                <p class="font-semibold text-gray-800">Disponibilità immediata.</p>
                            </div>
                            <p class="pl-7 text-base text-slate-700">
                                Consegna stimata entro martedì prossimo. Ordina subito per non perdere la priorità.
                            </p>
                            <p class="pl-7 text-sm text-slate-500">Venduto e spedito da POS Register.</p>
                        {:else if quantitaRimanente > 0}
                            <div class="flex items-center gap-x-2">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    class="h-5 w-5 flex-shrink-0 text-amber-500"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                    stroke-width="2"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                                    />
                                </svg>
                                <p class="font-semibold text-amber-700">
                                    Affrettati! Solo {quantitaRimanente} rimasti in magazzino.
                                </p>
                            </div>
                            <p class="pl-7 text-base text-slate-700">
                                Questo articolo è molto richiesto e potrebbe esaurirsi a breve.
                            </p>
                        {:else}
                            <div class="flex items-center gap-x-2">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    class="h-5 w-5 flex-shrink-0 text-red-600"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                    stroke-width="2"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
                                    />
                                </svg>
                                <p class="font-semibold text-red-700">Attualmente non disponibile.</p>
                            </div>
                            <p class="pl-7 text-base text-slate-700">
                                Non sappiamo se e quando questo articolo tornerà disponibile.
                            </p>
                            <p class="pl-7 text-sm text-slate-500">
                                Aggiungilo ai preferiti per ricevere una notifica.
                            </p>
                        {/if}
                    </div>
                </div>
            </div>
        </div>
        <Review category={prodotto.categoria} {allReviews} />
    {:else if error}
        <p class="text-black-600 text-center">{error}</p>
    {:else}
        <p class="text-center text-gray-500">Caricamento prodotto...</p>
    {/if}
</main>