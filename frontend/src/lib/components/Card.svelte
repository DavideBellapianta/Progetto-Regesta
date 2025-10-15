<script>
	import { cart, favorites } from '../stores.js';
	import { createSlug } from '$lib/utils.js';

	import cuore_vuoto from '$lib/assets/heart_vuoto.png';
	import cuore_rosso from '$lib/assets/heart_pieno_rosso.png';

	export let prodotto;

	function addToCart() {
		cart.add(prodotto); //Aggiunge il prodotto al carrello
	}

	function toggleFavorite() {
		favorites.toggle(prodotto); //Aggiunge o rimuove dai preferiti
	}

	let isFavorite = false;
	$: isFavorite = $favorites.has(prodotto.nome);
</script>

<a
	href="/prodotto/{createSlug(prodotto.nome)}"
	class="card-theme hover:shadow-accent/30 group block overflow-hidden rounded-lg
           shadow-md transition-all
           duration-300 hover:-translate-y-1
           hover:scale-[1.02] hover:shadow-[0_10px_25px_-5px_var(--accent)]"
>
	<div class="relative h-64 overflow-hidden">
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
				<img src={cuore_rosso} alt="Rimuovi dai preferiti" class="h-6 w-6" />
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
    class="card-buttonTheme mt-4 w-full rounded-lg 
           bg-gradient-to-r from-cyan-700 via-blue-500 to-indigo-600 
           py-2 font-semibold text-white 
           transition-all duration-200 ease-in-out
           hover:shadow-lg hover:shadow-indigo-500/50 hover:-translate-y-0.5
           active:scale-95 active:bg-gradient-to-br"
>
    Aggiungi al carrello
</button>
	</div>
</a>
