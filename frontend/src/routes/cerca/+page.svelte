<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import Card from '$lib/components/Card.svelte';
	import Navbar from '$lib/components/Navbar.svelte';

	let searchTerm = '';
	let results = [];
	let isLoading = true;
	let selectedCategory = '';
	let minPrice = '';
	let maxPrice = '';
	let allCategories = [];

	onMount(async () => {
		try {
			const catResponse = await fetch('http://127.0.0.1:5000/api/categorie');
			if (catResponse.ok) allCategories = await catResponse.json();
		} catch (e) {
			console.error("Errore caricamento categorie:", e);
		}
	});

	$: if ($page.url.searchParams) {
		const params = $page.url.searchParams;
		searchTerm = params.get('q') || '';
		selectedCategory = params.get('categoria') || '';
		minPrice = params.get('prezzo_min') || '';
		maxPrice = params.get('prezzo_max') || '';
		
		fetchResults();
	}

	async function fetchResults() {
		isLoading = true;
		const params = new URLSearchParams({
			q: searchTerm,
			categoria: selectedCategory,
			prezzo_min: minPrice,
			prezzo_max: maxPrice
		});
		try {
			const response = await fetch(`http://127.0.0.1:5000/api/search-results?${params.toString()}`);
			if (response.ok) {
				results = await response.json();
			}
		} catch (e) {
			console.error('Errore nella pagina di ricerca:', e);
		}
		isLoading = false;
	}

	function applyFilters() {
		const params = new URLSearchParams({
			q: searchTerm,
			categoria: selectedCategory,
			prezzo_min: minPrice,
			prezzo_max: maxPrice
		});
		goto(`/cerca?${params.toString()}`);
	}
</script>

<main class="mx-auto max-w-7xl px-4 py-8">
	<h1 class="text-3xl font-bold text-gray-900">
		Risultati per: <span class="text-indigo-600">"{searchTerm || 'tutti i prodotti'}"</span>
	</h1>

	<div class="mt-6 p-4 bg-white rounded-lg shadow-md flex flex-col sm:flex-row gap-4 items-center">
		<span class="font-semibold text-gray-700">Filtra per:</span>
		
		<select bind:value={selectedCategory} class="rounded-md border-gray-300 shadow-sm">
			<option value="">Tutte le categorie</option>
			{#each allCategories as category}
				<option value={category} class="capitalize">{category}</option>
			{/each}
		</select>

		<div class="flex items-center gap-2">
			<input type="number" bind:value={minPrice} placeholder="Prezzo min" class="w-24 rounded-md border-gray-300 shadow-sm"/>
			<span class="text-gray-500">-</span>
			<input type="number" bind:value={maxPrice} placeholder="Prezzo max" class="w-24 rounded-md border-gray-300 shadow-sm"/>
			<span>€</span>
		</div>

		<button on:click={applyFilters} class="bg-indigo-600 text-white px-6 py-2 rounded-md hover:bg-indigo-700">
			Applica
		</button>
	</div>

	{#if isLoading}
		<p class="mt-8 text-gray-500">Ricerca in corso...</p>
	{:else if results.length > 0}
		<div class="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
			{#each results as prodotto}
				<Card {prodotto} />
			{/each}
		</div>
	{:else}
		<p class="mt-8 text-gray-500">Nessun prodotto trovato. Prova a modificare i filtri.</p>
	{/if}
</main>