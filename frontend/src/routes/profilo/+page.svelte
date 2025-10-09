<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { utente } from '$lib/stores.js';
	import { createSlug } from '$lib/utils.js';
;

	let userProfile = null;
	let orderHistory = [];
	let error = null;
	let successMsg = '';
	let isLoading = true;

	onMount(() => {
		const unsubscribe = utente.subscribe((currentUser) => {
			if (currentUser === undefined) {
				return; 
			}

			if (currentUser) {
				loadPageData();
			} else {
				goto(`/login?redirectTo=/profilo`);
			}
		});

		return () => unsubscribe();
	});

	async function loadPageData() {
		isLoading = true;
		const token = localStorage.getItem('jwt_token');
		if (!token) {
			error = 'Token di autenticazione non trovato.';
			isLoading = false;
			return;
		}

		try {
			const [profileRes, ordersRes] = await Promise.all([
				fetch('http://127.0.0.1:5000/api/profilo', { headers: { Authorization: `Bearer ${token}` } }),
				fetch('http://127.0.0.1:5000/api/ordini', { headers: { Authorization: `Bearer ${token}` } })
			]);

			if (profileRes.ok) {
				userProfile = await profileRes.json();
			} else {
				throw new Error('Impossibile caricare il profilo.');
			}

			if (ordersRes.ok) {
				orderHistory = await ordersRes.json();
			} else {
				throw new Error('Impossibile caricare la cronologia ordini.');
			}
		} catch (e) {
			error = e.message;
		} finally {
			isLoading = false;
		}
	}

	async function handleUpdateProfile() {
		successMsg = '';
		error = null;
		const token = localStorage.getItem('jwt_token');
		if (!token || !userProfile) return;

		try {
			const response = await fetch('http://127.0.0.1:5000/api/profilo', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
				body: JSON.stringify(userProfile)
			});

			if (response.ok) {
				successMsg = 'Profilo aggiornato con successo!';
				setTimeout(() => (successMsg = ''), 3000); 
			} else {
				const data = await response.json();
				throw new Error(data.msg || "Errore durante l'aggiornamento.");
			}
		} catch (e) {
			error = e.message;
		}
	}
	async function handleDownloadReceipt(orderId) {
		const token = localStorage.getItem('jwt_token');
		if (!token) {
			alert('Devi essere loggato per scaricare uno scontrino.');
			return;
		}
		try {
			const response = await fetch(`http://127.0.0.1:5000/api/scontrino/${orderId}`, {
				headers: { Authorization: `Bearer ${token}` }
			});

			if (response.ok) {
				const receiptHtml = await response.text();
				const blob = new Blob([receiptHtml], { type: 'text/html' });
				const url = URL.createObjectURL(blob);
				window.open(url, '_blank'); 
			} else {
				throw new Error('Impossibile scaricare lo scontrino.');
			}
		} catch (e) {
			alert(e.message);
		}
	}
</script>


<main class="mx-auto max-w-4xl px-4 py-10">
	<h1 class="mb-8 text-3xl font-bold text-gray-900">Il Mio Profilo</h1>

	{#if isLoading}
		<p class="text-center text-gray-500">Caricamento profilo...</p>
	{:else if error}
		<p class="text-center text-red-500">{error}</p>
	{:else if userProfile}
		<form on:submit|preventDefault={handleUpdateProfile} class="space-y-8 rounded-lg bg-white p-8 shadow-lg">
			<div>
				<h2 class="border-b pb-4 text-xl font-semibold text-gray-800">Informazioni di Contatto</h2>
				<div class="mt-6 grid grid-cols-1 gap-y-6 sm:grid-cols-2 sm:gap-x-6">
					<div>
						<label for="nome" class="block text-sm font-medium text-gray-700">Nome</label>
						<input bind:value={userProfile.nome} type="text" id="nome" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" />
					</div>
					<div>
						<label for="cognome" class="block text-sm font-medium text-gray-700">Cognome</label>
						<input bind:value={userProfile.cognome} type="text" id="cognome" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" />
					</div>
					<div class="sm:col-span-2">
						<label for="email" class="block text-sm font-medium text-gray-700">Email (non modificabile)</label>
						<input type="email" id="email" value={userProfile.email} disabled class="mt-1 block w-full cursor-not-allowed rounded-md border-gray-300 bg-gray-100 shadow-sm" />
					</div>
					<div class="sm:col-span-2">
						<label for="telefono" class="block text-sm font-medium text-gray-700">Telefono</label>
						<input bind:value={userProfile.telefono} type="tel" id="telefono" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" />
					</div>
				</div>
			</div>

			<div>
				<h2 class="border-b pb-4 text-xl font-semibold text-gray-800">Indirizzo di Spedizione</h2>
				<div class="mt-6 grid grid-cols-1 gap-y-6 sm:grid-cols-2 sm:gap-x-6">
					<div class="sm:col-span-2">
						<label for="indirizzo" class="block text-sm font-medium text-gray-700">Indirizzo</label>
						<input bind:value={userProfile.indirizzo} type="text" id="indirizzo" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" />
					</div>
					<div>
						<label for="citta" class="block text-sm font-medium text-gray-700">Città</label>
						<input bind:value={userProfile.citta} type="text" id="citta" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" />
					</div>
					<div>
						<label for="cap" class="block text-sm font-medium text-gray-700">CAP</label>
						<input bind:value={userProfile.cap} type="text" id="cap" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" />
					</div>
				</div>
			</div>

			{#if error} <p class="text-sm text-red-600">{error}</p> {/if}
			{#if successMsg} <p class="text-sm text-green-600">{successMsg}</p> {/if}

			<div class="pt-4 text-right">
				<button type="submit" class="rounded-md bg-indigo-600 px-6 py-2 text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
					Salva Modifiche
				</button>
			</div>
		</form>

		<section class="mt-12">
			<h2 class="mb-6 text-2xl font-bold text-gray-900">Cronologia Ordini</h2>
			<div class="space-y-8">
				{#if orderHistory.length > 0}
					{#each orderHistory as order}
						<div class="rounded-lg bg-white p-6 shadow-lg">
							<div class="mb-4 flex items-center justify-between border-b border-gray-200 pb-4">
								<div>
									<p class="font-semibold text-gray-800">
										Ordine del {new Date(order.data_ordine).toLocaleDateString('it-IT', {
											year: 'numeric',
											month: 'long',
											day: 'numeric'
										})}
									</p>
									<p class="text-sm text-gray-500">Totale: {order.totale_netto}</p>
								</div>
								<button on:click={() => handleDownloadReceipt(order._id)} class="rounded-lg bg-gray-200 px-4 py-2 text-sm font-semibold text-gray-800 hover:bg-gray-300">
									Vedi Scontrino
								</button>
							</div>
							<ul class="divide-y divide-gray-200">
								{#each order.prodotti as item}
									<li class="flex items-center py-2">
										<a href="/prodotto/{createSlug(item.nome)}">
											<img src={item.immagine_url} alt={item.nome} class="h-12 w-12 rounded-md object-cover" />
										</a>
										<div class="ml-4 flex-1">
											<a href="/prodotto/{createSlug(item.nome)}" class="text-sm font-medium text-gray-800 hover:text-indigo-600">
												{item.nome}
											</a>
											<p class="text-xs text-gray-500">Quantità: {item.quantita}</p>
										</div>
										<p class="text-sm font-medium text-gray-900">
											{item.prezzo_finale_riga}
										</p>
									</li>
								{/each}
							</ul>
						</div>
					{/each}
				{:else}
					<div class="rounded-lg bg-white p-8 text-center shadow-lg">
						<p class="text-gray-500">Non hai ancora effettuato nessun ordine.</p>
					</div>
				{/if}
			</div>
		</section>
	{/if}
</main>