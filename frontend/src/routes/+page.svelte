<script>
	import { onMount } from 'svelte';
	import Navbar from '$lib/components/Navbar.svelte';
	import ProductCart from '$lib/components/ProductCart.svelte';
	import DebugImage from '$lib/components/DebugImage.svelte';
	import { isCartOpenMobile } from '$lib/stores.js';

	let randomProducts = [];
	let foodProducts = [];
	let medicalProducts = [];
	let ElettronicaProducts = [];
	let casaProducts = [];

	onMount(async () => {
		try {
			const [randomRes, foodRes, medicalRes, eletronRes, casaRes] = await Promise.all([
				fetch('http://127.0.0.1:5000/prodotti?random=6'), 
				fetch('http://127.0.0.1:5000/prodotti?categoria=food'),
				fetch('http://127.0.0.1:5000/prodotti?categoria=medical'), 
				fetch('http://127.0.0.1:5000/prodotti?categoria=elettronica'),
				fetch('http://127.0.0.1:5000/prodotti?categoria=casa')
			]);

			randomProducts = await randomRes.json();
			foodProducts = await foodRes.json();
			medicalProducts = await medicalRes.json();
			ElettronicaProducts = await eletronRes.json();
			casaProducts = await casaRes.json();
		} catch (error) {
			console.error('Errore nel caricamento dei dati dalla homepage:', error);
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
