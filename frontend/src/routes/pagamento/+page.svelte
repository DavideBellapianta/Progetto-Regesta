<script>
	import { cart } from '$lib/stores.js';

	// --- STATO DEL COMPONENTE ---
	let selectedShipping = 'classico'; // Default iniziale
	$: {
		if (subtotal >= 100) {
			selectedShipping = 'rapido'; // Se il subtotale è >= 100, preseleziona la spedizione rapida (che sarà gratuita)
		} else {
			// Se scende di nuovo sotto 100, torna a quella classica per evitare costi a sorpresa
			if (selectedShipping === 'rapido') {
				selectedShipping = 'classico';
			}
		}
	}
	function createSlug(name) {
		return name
			.toLowerCase()
			.replace(/\s+/g, '-')
			.replace(/[()]/g, '')
			.replace(/[^\w-]+/g, '');
	}

	// Dati del form, raccolti in un unico oggetto
	let formData = {
		email: '',
		telefono: '',
		nomeCompleto: '',
		indirizzo: '',
		citta: '',
		cap: '',
		paese: 'Italia',
		numeroCarta: '',
		scadenzaCarta: '',
		cvc: '',
		orderNotes: ''
	};

	// --- LOGICA REATTIVA PER I CALCOLI ---
	// $: -> Queste variabili si ricalcolano automaticamente quando le loro dipendenze cambiano

	// Calcola il subtotale ogni volta che il carrello ($cart) cambia
	$: subtotal = $cart.reduce((sum, item) => sum + item.prezzo_lordo * item.quantita, 0);

	// Calcola il costo di spedizione ogni volta che 'selectedShipping' o 'subtotal' cambiano
	$: shippingCost = (() => {
		if (selectedShipping === 'rapido' && subtotal < 100) {
			return 10.0;
		}
		return 0.0; // Spedizione classica o rapida per ordini > 100€ è gratis
	})();

	// Calcola il totale finale ogni volta che 'subtotal' o 'shippingCost' cambiano
	$: total = subtotal + shippingCost;

	// Funzione per simulare l'invio del pagamento
	function handlePayment() {
		// In un'applicazione reale, qui invieresti 'formData' e '$cart' al tuo backend
		// per l'elaborazione del pagamento con un servizio come Stripe o PayPal.
		console.log('Dati ordine inviati:', {
			datiCliente: formData,
			ordine: $cart,
			costi: {
				subtotal: subtotal.toFixed(2),
				shipping: shippingCost.toFixed(2),
				total: total.toFixed(2)
			}
		});

		alert(`Pagamento di ${total.toFixed(2)}€ inviato con successo! (Simulazione)`);
	}
</script>

<div class="bg-gray-50">
	<main class="mx-auto max-w-7xl px-4 pb-24 pt-16 sm:px-6 lg:px-8">
		<h1 class="text-center text-3xl font-extrabold tracking-tight text-gray-900">Checkout</h1>

		<form
			on:submit|preventDefault={handlePayment}
			class="mt-12 lg:grid lg:grid-cols-2 lg:gap-x-12 xl:gap-x-16"
		>
			<div class="space-y-8">
				<div>
					<h2 class="text-lg font-medium text-gray-900">Informazioni di Contatto</h2>
					<div class="mt-4 grid grid-cols-1 gap-y-6 sm:grid-cols-2 sm:gap-x-4">
						<div class="sm:col-span-2">
							<label for="email" class="block text-sm font-medium text-gray-700">Email</label>
							<input
								bind:value={formData.email}
								type="email"
								id="email"
								required
								class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
							/>
						</div>
						<div class="sm:col-span-2">
							<label for="telefono" class="block text-sm font-medium text-gray-700">Telefono</label>
							<input
								bind:value={formData.telefono}
								type="tel"
								id="telefono"
								required
								class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
							/>
						</div>
					</div>
				</div>

				<div>
					<h2 class="text-lg font-medium text-gray-900">Indirizzo di Spedizione</h2>
					<div class="mt-4 grid grid-cols-1 gap-y-6 sm:grid-cols-2 sm:gap-x-4">
						<div class="sm:col-span-2">
							<label for="nomeCompleto" class="block text-sm font-medium text-gray-700"
								>Nome e Cognome</label
							>
							<input
								bind:value={formData.nomeCompleto}
								type="text"
								id="nomeCompleto"
								required
								class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
							/>
						</div>
						<div class="sm:col-span-2">
							<label for="indirizzo" class="block text-sm font-medium text-gray-700"
								>Indirizzo</label
							>
							<input
								bind:value={formData.indirizzo}
								type="text"
								id="indirizzo"
								required
								class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
							/>
						</div>
						<div>
							<label for="citta" class="block text-sm font-medium text-gray-700">Città</label>
							<input
								bind:value={formData.citta}
								type="text"
								id="citta"
								required
								class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
							/>
						</div>
						<div>
							<label for="cap" class="block text-sm font-medium text-gray-700">CAP</label>
							<input
								bind:value={formData.cap}
								type="text"
								id="cap"
								required
								class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
							/>
						</div>
					</div>
				</div>

				<div>
					<h2 class="text-lg font-medium text-gray-900">Dettagli Pagamento</h2>
					<div class="mt-4 grid grid-cols-1 gap-y-6 sm:grid-cols-4 sm:gap-x-4">
						<div class="sm:col-span-4">
							<label for="numeroCarta" class="block text-sm font-medium text-gray-700"
								>Numero Carta</label
							>
							<input
								bind:value={formData.numeroCarta}
								type="text"
								id="numeroCarta"
								required
								class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
							/>
						</div>
						<div class="sm:col-span-2">
							<label for="scadenzaCarta" class="block text-sm font-medium text-gray-700"
								>Scadenza (MM/AA)</label
							>
							<input
								bind:value={formData.scadenzaCarta}
								type="text"
								id="scadenzaCarta"
								required
								placeholder="MM/AA"
								class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
							/>
						</div>
						<div class="sm:col-span-2">
							<label for="cvc" class="block text-sm font-medium text-gray-700">CVC</label>
							<input
								bind:value={formData.cvc}
								type="text"
								id="cvc"
								required
								class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
							/>
						</div>
					</div>
				</div>

				<div>
					<label for="orderNotes" class="block text-sm font-medium text-gray-700"
						>Note sull'ordine (opzionale)</label
					>
					<textarea
						bind:value={formData.orderNotes}
						id="orderNotes"
						rows="4"
						class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
					></textarea>
				</div>
			</div>

			<div class="mt-10 lg:mt-0">
				<h2 class="text-lg font-medium text-gray-900">Riepilogo Ordine</h2>
				<div class="mt-4 rounded-lg border border-gray-200 bg-white shadow-sm">
					<h3 class="sr-only">Articoli nel tuo carrello</h3>
					<ul class="divide-y divide-gray-200">
						{#each $cart as item}
							<li class="flex px-4 py-6 sm:px-6">
								<a href="/prodotto/{createSlug(item.nome)}" class="flex-shrink-0">
									<img
										src={item.immagine_url}
										alt={item.nome}
										class="h-20 w-20 rounded-md object-cover"
									/>
								</a>

								<div class="ml-6 flex flex-1 flex-col">
									<div class="flex">
										<div class="min-w-0 flex-1">
											<h4 class="text-sm font-medium text-gray-700 hover:text-indigo-600">
												<a href="/prodotto/{createSlug(item.nome)}">{item.nome}</a>
											</h4>
											<p class="mt-1 text-sm text-gray-500">x {item.quantita}</p>
										</div>
									</div>
								</div>

								<p class="text-sm font-medium text-gray-900">
									{(item.prezzo_lordo * item.quantita).toFixed(2)}€
								</p>
							</li>
						{/each}
					</ul>

					<div class="border-t border-gray-200 px-4 py-6 sm:px-6">
						<h3 class="text-md font-medium text-gray-900">Spedizione</h3>
						<div class="mt-4 space-y-4">
							<div class="flex items-center">
								<input
									bind:group={selectedShipping}
									value="classico"
									id="shipping-classico"
									type="radio"
									class="h-4 w-4 border-gray-300 text-indigo-600 focus:ring-indigo-500"
								/>
								<label for="shipping-classico" class="ml-3 block text-sm font-medium text-gray-700">
									Classica <span class="text-gray-500">(Gratuita)</span>
								</label>
							</div>
							<div class="flex items-center">
								<input
									bind:group={selectedShipping}
									value="rapido"
									id="shipping-rapido"
									type="radio"
									class="h-4 w-4 border-gray-300 text-indigo-600 focus:ring-indigo-500"
								/>
								<label for="shipping-rapido" class="ml-3 block text-sm font-medium text-gray-700">
									Rapida <span class="text-gray-500">(10.00€ se ordine &lt; 100€)</span>
								</label>
							</div>
						</div>
					</div>

					<dl class="space-y-4 border-t border-gray-200 px-4 py-6 sm:px-6">
						<div class="flex items-center justify-between">
							<dt class="text-sm text-gray-600">Subtotale</dt>
							<dd class="text-sm font-medium text-gray-900">{subtotal.toFixed(2)}€</dd>
						</div>
						<div class="flex items-center justify-between">
							<dt class="text-sm text-gray-600">Spedizione</dt>
							<dd class="text-sm font-medium text-gray-900">{shippingCost.toFixed(2)}€</dd>
						</div>
						<div class="flex items-center justify-between border-t border-gray-200 pt-4">
							<dt class="text-base font-medium text-gray-900">Totale Ordine</dt>
							<dd class="text-base font-medium text-gray-900">{total.toFixed(2)}€</dd>
						</div>
					</dl>
				</div>
				<div class="mt-6">
					<button
						type="submit"
						class="w-full rounded-md border border-transparent bg-indigo-600 px-4 py-3 text-base font-medium text-white shadow-sm hover:bg-indigo-700"
					>
						Paga Ora
					</button>
				</div>
			</div>
		</form>
	</main>
</div>
