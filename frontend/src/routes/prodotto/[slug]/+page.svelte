<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { cart, favorites } from '$lib/stores.js';
	import Navbar from '$lib/components/Navbar.svelte';
	import Review from '$lib/components/Review.svelte';
	import cuore from '$lib/assets/heart_pieno.png';
	import cuore_vuoto from '$lib/assets/heart_vuoto.png';
	import cuore_rosso from '$lib/assets/heart_pieno_rosso.png';

	let prodotto = null;
	let error = null;
	let isFavorite = false;

	// NUOVA VARIABILE DI STATO PER LA QUANTITÀ
	let quantitaRimanente = null;

	onMount(async () => {
		const slug = $page.params.slug;

		try {
			const response = await fetch(`http://127.0.0.1:5000/api/prodotto/${slug}`);
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

	// NUOVA FUNZIONE PER RECUPERARE LA QUANTITÀ
	async function fetchQuantita(slug) {
		try {
			const response = await fetch(`http://127.0.0.1:5000/api/prodotto/${slug}/quantita`);
			if (response.ok) {
				const data = await response.json();
				quantitaRimanente = data.quantita;
			} else {
				quantitaRimanente = 0; // Se non trova il prodotto, la quantità è 0
			}
		} catch (e) {
			console.error('Errore nel recupero della quantità:', e);
			quantitaRimanente = 0; // In caso di errore, mettiamo 0
		}
	}

	function toggleFavorite() {
		if (prodotto) favorites.toggle(prodotto);
	}
	function addToCart() {
		if (prodotto) cart.add(prodotto);
	}

	$: if (prodotto) isFavorite = $favorites.has(prodotto.nome);

	// BLOCCO REATTIVO: quando 'prodotto' viene caricato, parte la fetch per la quantità
	$: if (prodotto) {
		fetchQuantita($page.params.slug);
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
		<Review category={prodotto.categoria} />
	{:else if error}
		<p class="text-black-600 text-center">{error}</p>
	{:else}
		<p class="text-center text-gray-500">Caricamento prodotto...</p>
	{/if}
</main>
