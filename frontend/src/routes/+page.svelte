<script>
	import { onMount } from 'svelte';
	import Navbar from '$lib/components/Navbar.svelte';
	import ProductCart from '$lib/components/ProductCart.svelte';
	import DebugImage from '$lib/components/DebugImage.svelte';
	import { isCartOpenMobile } from '$lib/stores.js';

	// Variabili di stato per contenere i dati dal backend
	let randomProducts = [];
	let foodProducts = [];
	let medicalProducts = [];
	let ElettronicaProducts = [];
	let casaProducts = [];

	// Appena la pagina è pronta, parte il caricamento dei dati
	onMount(async () => {
		try {
			// Per velocizzare, facciamo partire tutte le chiamate API in parallelo
			const [randomRes, foodRes, medicalRes, eletronRes, casaRes] = await Promise.all([
				fetch('http://127.0.0.1:5000/prodotti?random=6'), // Chiede 4 prodotti casuali
				fetch('http://127.0.0.1:5000/prodotti?categoria=food'), // Chiede i prodotti 'food'
				fetch('http://127.0.0.1:5000/prodotti?categoria=medical'), // Chiede i prodotti 'medical'
				fetch('http://127.0.0.1:5000/prodotti?categoria=elettronica'), // Chiede i prodotti 'medical'
				fetch('http://127.0.0.1:5000/prodotti?categoria=casa') // Chiede i prodotti 'medical'
			]);

			// Aspettiamo le risposte e le convertiamo in JSON
			randomProducts = await randomRes.json();
			foodProducts = await foodRes.json();
			medicalProducts = await medicalRes.json();
			ElettronicaProducts = await eletronRes.json();
			casaProducts = await casaRes.json();
		} catch (error) {
			console.error('Errore nel caricamento dei dati dalla homepage:', error);
			// Qui potresti impostare una variabile per mostrare un messaggio di errore all'utente
		}
	});
</script>

<div
	class="min-h-screen transition-all duration-300"
	class:pb-96={$isCartOpenMobile}
	class:md:pb-0={true}
>
	<main class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
		<ProductCart title="Offerte del Giorno" products={randomProducts} />
		<ProductCart title="Cibo e Bevande" products={foodProducts} />
		<ProductCart title="Articoli Sanitari" products={medicalProducts} />
		<ProductCart title="Elettronica" products={ElettronicaProducts} />
		<ProductCart title="Articoli per casa" products={casaProducts} />
	</main>
</div>
