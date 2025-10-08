<script>
	import { onMount } from 'svelte';
	import { cart, favorites } from '$lib/stores.js';
    import { goto } from '$app/navigation';
    import { utente } from '$lib/stores.js';

    onMount(() => {
        // Usa 'setTimeout' per dare allo store 'utente' il tempo di caricarsi
        setTimeout(() => {
            // Se lo store '$utente' è nullo (utente non loggato)
            if (!$utente) {
                // Reindirizza alla pagina di login, ricordando da dove veniamo
                goto(`/login?redirectTo=/carrello`);
            }
        }, 100);
    });

	let scontrino = null;
	let error = null;
	let allProducts = [];
	let favoriteProductsDetails = [];

	let debounceTimer;

	// Blocco reattivo che ricalcola lo scontrino ogni volta che il carrello cambia
	$: if ($cart) {
		clearTimeout(debounceTimer);
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
				error = 'Non è stato possibile calcolare il totale.';
			}
		}, 200);
	}

	// Caricamento dei dati per i preferiti (solo una volta)
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

	$: favoriteProductsDetails = allProducts.filter((p) => $favorites.has(p.nome));
</script>

<div class="min-h-screen ">
	<main class="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
		<h1 class="mb-8 text-4xl font-extrabold tracking-tight text-gray-900">Il Tuo Carrello</h1>

		{#if error}
			<div
				class="text-black-700 rounded-lg border border-red-400 bg-red-100 px-4 py-3"
				role="alert"
			>
				{error}
			</div>
		{:else if scontrino}
			<div class="overflow-hidden rounded-lg bg-white shadow-lg">
				<div class="p-6">
					<h2 class="mb-4 text-xl font-semibold">Riepilogo Ordine</h2>
					{#if $cart.length > 0}
						<ul class="divide-y divide-gray-200">
							{#each $cart as item}
								<li class="flex items-center py-6">
									<img
										src={item.immagine_url}
										alt={item.nome}
										class="h-24 w-24 rounded-md object-cover"
									/>
									<div class="ml-4 flex-1">
										<p class="font-semibold text-gray-800">{item.nome}</p>
										<div class="mt-2 flex items-center">
											<div class="flex items-center text-sm text-gray-700">
												<button
													on:click={() => cart.decrement(item.nome)}
													class="rounded-l-md border px-3 py-1 hover:bg-gray-100">-</button
												>
												<span class="border-b border-t px-4 py-1 font-bold">{item.quantita}</span>
												<button
													on:click={() => cart.increment(item.nome)}
													class="rounded-r-md border px-3 py-1 hover:bg-gray-100">+</button
												>
											</div>
											<button
												on:click={() => cart.remove(item.nome)}
												class="text-black-600 ml-4 text-sm hover:underline"
											>
												Rimuovi
											</button>
										</div>
									</div>
									<div class="text-right">
										<p class="text-lg font-semibold text-gray-800">
											{(item.prezzo_lordo * item.quantita).toFixed(2)}€
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
								<span
									>{$cart
										.reduce((sum, p) => sum + p.prezzo_lordo * p.quantita, 0)
										.toFixed(2)}€</span
								>
							</div>
							<div class="flex justify-between text-gray-600">
								<span>Tasse (IVA)</span>
								<span class="font-medium">{scontrino.totale_tasse}</span>
							</div>
							<div class="mt-2 flex justify-between border-t pt-2 text-xl font-bold text-gray-900">
								<span>Totale da Pagare</span>
								<span>{scontrino.totale_netto}</span>
							</div>
						</div>
						<a
							href="/pagamento"
							class="mt-6 block w-full rounded-lg bg-indigo-600 py-3 text-center text-lg font-semibold text-white transition hover:bg-indigo-700"
						>
							Procedi al Checkout
						</a>
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
										Aggiungi al Carrello
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
