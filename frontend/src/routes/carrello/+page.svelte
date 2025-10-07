<script>
	import { onMount } from 'svelte';
	import { cart, favorites } from '$lib/stores.js';
	import Navbar from '$lib/components/Navbar.svelte';

	let scontrino = null;
	let error = null;
	let allProducts = [];
	let favoriteProductsDetails = [];

	// --- LOGICA PER CARICARE I DATI DEI PRODOTTI (per i preferiti) ---
	onMount(async () => {
		try {
			const res = await fetch('http://127.0.0.1:5000/prodotti');
			if (res.ok) {
				allProducts = await res.json();
			}
		} catch (e) {
			console.error('Impossibile caricare i prodotti per i preferiti', e);
		}
	});

	// --- MODIFICA CHIAVE: BLOCCO REATTIVO PER IL CALCOLO DELLO SCONTRINO ---

	let debounceTimer; // Timer per il ritardo

	// Questo blocco di codice viene eseguito AUTOMATICAMENTE ogni volta che '$cart' cambia.
	$: if ($cart) {
		clearTimeout(debounceTimer); // Annulla il timer precedente se l'utente è veloce
		
		// Imposta un piccolo ritardo (200ms) prima di chiamare l'API
		debounceTimer = setTimeout(async () => {
			if ($cart.length === 0) {
				scontrino = { righe: [], totale_tasse: '0.00€', totale_netto: '0.00€' };
				return;
			}
			try {
				const response = await fetch('http://127.0.0.1:5000/api/scontrino', {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify($cart)
				});
				if (response.ok) {
					scontrino = await response.json();
				} else {
					throw new Error('Errore nella risposta del server');
				}
			} catch (e) {
				console.error('Impossibile calcolare lo scontrino:', e);
				error = 'Non è stato possibile calcolare il totale. Riprova più tardi.';
			}
		}, 200); // 200 millisecondi di ritardo
	}

	// Logica reattiva per i preferiti (invariata)
	$: favoriteProductsDetails = allProducts.filter((p) => $favorites.has(p.nome));
</script>

<div class="min-h-screen bg-gray-100">
	<main class="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
		<h1 class="mb-8 text-4xl font-extrabold tracking-tight text-gray-900">Il Tuo Carrello</h1>

		{#if error}
			<div class="rounded-lg border border-red-400 bg-red-100 px-4 py-3 text-red-700" role="alert">
				{error}
			</div>
		{:else if scontrino}
			<div class="overflow-hidden rounded-lg bg-white shadow-lg">
				<div class="p-6">
					<h2 class="mb-4 text-xl font-semibold">Riepilogo Ordine</h2>
					{#if $cart.length > 0}
						<ul class="divide-y divide-gray-200">
							{#each $cart as item}
								<li class="flex items-center py-4">
									<img
										src={item.immagine_url}
										alt={item.nome}
										class="h-20 w-20 rounded-md object-cover"
									/>
									<div class="ml-4 flex-1">
										<p class="font-semibold text-gray-800">{item.nome}</p>
										<p class="text-sm text-gray-500">
											Quantità: {item.quantita}
										</p>
									</div>
									<div class="text-right">
										<p class="font-semibold text-gray-800">
											{(item.prezzo_lordo * item.quantita).toFixed(2)}€
										</p>
										<p class="text-sm text-gray-500">
											({item.prezzo_lordo.toFixed(2)}€ cad.)
										</p>
									</div>
								</li>
							{/each}
						</ul>
					{:else}
						<p class="py-12 text-center text-gray-500">Il tuo carrello è vuoto.</p>
					{/if}
				</div>

				{#if $cart.length > 0}
					<div class="border-t border-gray-200 bg-gray-50 p-6">
						<div class="space-y-2">
							<div class="flex justify-between text-gray-600">
								<span>Subtotale (Lordo)</span>
								<span>
									{$cart.reduce((sum, p) => sum + p.prezzo_lordo * p.quantita, 0).toFixed(2)}€
								</span>
							</div>
							<div class="flex justify-between text-gray-600">
								<span>Tasse (IVA)</span>
								<span>{scontrino.totale_tasse}</span>
							</div>
							<div class="mt-2 flex justify-between border-t pt-2 text-xl font-bold text-gray-900">
								<span>Totale da Pagare</span>
								<span>{scontrino.totale_netto}</span>
							</div>
						</div>
						<button
							class="mt-6 w-full rounded-lg bg-indigo-600 py-3 text-lg font-semibold text-white transition hover:bg-indigo-700"
						>
							Procedi al Checkout
						</button>
					</div>
				{/if}
			</div>
			<section class="mt-12">
				<h2 class="mb-6 text-2xl font-bold text-gray-900">La tua Lista Desideri</h2>
				{#if favoriteProductsDetails.length > 0}
					<div class="rounded-lg bg-white p-6 shadow-lg">
						<ul class="divide-y divide-gray-200">
							{#each favoriteProductsDetails as prodotto}
								<li class="flex items-center py-4">
									<img
										src={prodotto.immagine_url}
										alt={prodotto.nome}
										class="h-16 w-16 rounded-md object-cover"
									/>
									<div class="ml-4 flex-1">
										<p class="font-semibold text-gray-800">{prodotto.nome}</p>
										<p class="text-sm text-gray-600">{prodotto.prezzo_lordo.toFixed(2)}€</p>
									</div>
									<button
										on:click={() => cart.add(prodotto)}
										class="rounded-lg bg-gray-200 px-4 py-2 text-sm font-semibold text-gray-800 hover:bg-gray-300"
									>
										Aggiungi
									</button>
								</li>
							{/each}
						</ul>
					</div>
				{:else}
					<div class="rounded-lg bg-white p-12 text-center shadow-lg">
						<p class="text-gray-500">
							Non hai ancora aggiunto prodotti ai preferiti. Clicca sul ♡ sulle card dei prodotti!
						</p>
					</div>
				{/if}
			</section>
		{:else}
			<div class="py-12 text-center text-gray-500">
				<p>Calcolo del totale in corso...</p>
			</div>
		{/if}
	</main>
</div>
