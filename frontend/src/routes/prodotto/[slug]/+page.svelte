<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { cart, favorites } from '$lib/stores.js';
	import Navbar from '$lib/components/Navbar.svelte';

	let prodotto = null;
	let error = null;
	let isFavorite = false;

	onMount(async () => {
		// --- LOGICA SEMPLIFICATA E CORRETTA ---
		const slug = $page.params.slug; // Prende lo slug pulito dall'URL

		try {
			// Lo usa direttamente per chiamare l'API
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

	function toggleFavorite() { if (prodotto) favorites.toggle(prodotto); }
	function addToCart() { if (prodotto) cart.add(prodotto); }
	
	$: if (prodotto) isFavorite = $favorites.has(prodotto.nome);
</script>

<Navbar />

<main class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
	{#if prodotto}
		<div class="grid grid-cols-1 md:grid-cols-2 gap-12 items-start">
			<div class="bg-white rounded-lg shadow-lg overflow-hidden">
				<img src={prodotto.immagine_url} alt={prodotto.nome} class="w-full h-auto object-cover" />
			</div>

			<div class="flex flex-col space-y-6">
				<div>
					<span class="text-indigo-600 font-semibold uppercase tracking-wide">{prodotto.categoria}</span>
					<h1 class="text-4xl font-extrabold text-gray-900 tracking-tight mt-1">{prodotto.nome}</h1>
					<p class="text-3xl text-gray-800 font-bold mt-4">{prodotto.prezzo_lordo.toFixed(2)}€</p>
				</div>

				<div class="text-gray-600 leading-relaxed">
					<h2 class="font-semibold text-gray-800 mb-2">Descrizione</h2>
					<p>
						Questa è una descrizione di esempio per il prodotto "{prodotto.nome}". In un'applicazione reale, questo testo verrebbe caricato dal database. Offre qualità e convenienza, ideale per le tue esigenze quotidiane.
					</p>
				</div>
				
				<div class="flex items-center space-x-4">
					<button on:click={addToCart} class="flex-1 bg-indigo-600 text-white py-3 rounded-lg font-semibold text-lg transition hover:bg-indigo-700">
						Aggiungi al carrello
					</button>
					<button on:click={toggleFavorite} class="p-3 rounded-full border-2 transition" class:border-red-500={isFavorite} class:border-gray-300={!isFavorite}>
						<svg class="h-6 w-6" class:text-red-500={isFavorite} class:text-gray-400={!isFavorite} fill={isFavorite ? 'currentColor' : 'none'} viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 016.364 0L12 7.5l1.318-1.182a4.5 4.5 0 116.364 6.364L12 21.5l-7.682-7.682a4.5 4.5 0 010-6.364z"/>
						</svg>
					</button>
				</div>
			</div>
		</div>
	{:else if error}
		<p class="text-center text-red-600">{error}</p>
	{:else}
		<p class="text-center text-gray-500">Caricamento prodotto...</p>
	{/if}
</main>