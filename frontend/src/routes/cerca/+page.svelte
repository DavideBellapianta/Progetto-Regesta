<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import Card from '$lib/components/Card.svelte'; // Il componente card che già usi

	let searchTerm = '';
	let results = [];
	let isLoading = true;

	onMount(async () => {
		// Legge il termine di ricerca dai parametri dell'URL
		searchTerm = $page.url.searchParams.get('q') || '';
		if (searchTerm) {
			try {
				const response = await fetch(`http://127.0.0.1:5000/api/cerca?q=${encodeURIComponent(searchTerm)}`);
				if (response.ok) {
					results = await response.json();
				}
			} catch (e) {
				console.error("Errore nella pagina di ricerca:", e);
			}
		}
		isLoading = false;
	});
</script>

<main class="max-w-7xl mx-auto py-8 px-4">
	<h1 class="text-3xl font-bold text-gray-900">
		Risultati per: <span class="text-indigo-600">"{searchTerm}"</span>
	</h1>

	{#if isLoading}
		<p class="mt-8 text-gray-500">Ricerca in corso...</p>
	{:else if results.length > 0}
		<div class="mt-8 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
			{#each results as prodotto}
				<Card {prodotto} />
			{/each}
		</div>
	{:else}
		<p class="mt-8 text-gray-500">Nessun prodotto trovato per "{searchTerm}". Prova con un altro termine.</p>
	{/if}
</main>