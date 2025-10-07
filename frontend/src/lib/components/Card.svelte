<script>
	import { cart, favorites } from '../stores.js';

	import cuore from '$lib/assets/heart_pieno.png';
	import cuore_vuoto from '$lib/assets/heart_vuoto.png';

	export let prodotto;

	function createSlug(name) {
		return name
			.toLowerCase() // 1. Minuscolo
			.replace(/\s+/g, '-') // 2. Spazi -> trattini
			.replace(/[()]/g, '') // 3. Rimuove parentesi
			.replace(/[^\w-]+/g, ''); // 4. Rimuove altri caratteri
	}

	// Funzioni per interagire con gli store
	function addToCart() {
		cart.add(prodotto);
	}

	function toggleFavorite() {
		favorites.toggle(prodotto);
	}

	// Variabile reattiva per lo stato dei preferiti
	let isFavorite = false;
	$: isFavorite = $favorites.has(prodotto.nome);
</script>

<a
	href="/prodotto/{createSlug(prodotto.nome)}"
	class="group block overflow-hidden rounded-lg bg-white shadow-md transition-all duration-300 hover:-translate-y-1 hover:shadow-xl"
>
	<div class="relative h-48 overflow-hidden">
		<img
			src={prodotto.immagine_url}
			alt={prodotto.nome}
			class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-110"
		/>

		<button
			on:click|stopPropagation|preventDefault={toggleFavorite}
			class="absolute right-2 top-2 rounded-full bg-white/70 p-2 backdrop-blur-sm transition hover:bg-white"
			aria-label="Aggiungi ai preferiti"
		>
			{#if isFavorite}
				<img src={cuore} alt="Rimuovi dai preferiti" class="h-6 w-6" />
			{:else}
				<img src={cuore_vuoto} alt="Aggiungi ai preferiti" class="h-6 w-6" />
			{/if}
		</button>
	</div>

	<div class="flex flex-col p-4">
		<h3 class="h-14 truncate text-lg font-semibold text-gray-800" title={prodotto.nome}>
			{prodotto.nome}
		</h3>
		<p class="mt-1 text-xl font-bold text-gray-600">{prodotto.prezzo_lordo.toFixed(2)}€</p>

		<button
			on:click|stopPropagation|preventDefault={addToCart}
			class="mt-4 w-full rounded-lg bg-indigo-600 py-2 font-semibold text-white transition hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
		>
			Aggiungi al carrello
		</button>
	</div>
</a>
