<script>
	import { onMount } from 'svelte';
	import { cart, cartItemsCount, isCartOpenMobile } from '../stores.js';
	import CartMenu from './CartMenu.svelte';
	import { createSlug } from '$lib/utils.js';
	import { page } from '$app/stores';
	import { utente } from '../stores.js';

	const API_BASE_URL = 'http://127.0.0.1:5000';
	const SEARCH_DEBOUNCE_MS = 300;

	let location = 'Caricamento...';
	let locationSource = null;
	let isLoadingPrecise = false;
	let searchTerm = '';
	let searchResults = [];
	let debounceTimer;
	let isSearchFocused = false;
	let isUserMenuOpen = false;
	let isMobileSearchOpen = false;

	// Gestione del carrello mobile
	function toggleCartMenu() {
		isCartOpenMobile.update((isOpen) => !isOpen);
	}

	// Gestione del menu utente
	function toggleUserMenu() {
		isUserMenuOpen = !isUserMenuOpen;
	}

	// Chiude il carrello quando si clicca fuori
	function clickOutsideCarrello(node) {
		const handleClick = (event) => {
			if (node && !node.contains(event.target) && !event.defaultPrevented) {
				isCartOpenMobile.set(false);
			}
		};
		document.addEventListener('click', handleClick, true);
		return {
			destroy() {
				document.removeEventListener('click', handleClick, true);
			}
		};
	}

	// Chiude il menu utente quando si clicca fuori
	function clickOutsideUser(node) {
		const handleClick = (event) => {
			if (node && !node.contains(event.target) && !event.defaultPrevented) {
				isUserMenuOpen = false;
			}
		};
		document.addEventListener('click', handleClick, true);
		return {
			destroy() {
				document.removeEventListener('click', handleClick, true);
			}
		};
	}

	// Gestione submit della ricerca
	function handleSearchSubmit() {
		if (searchTerm.trim() !== '') {
			window.location.href = `/cerca?q=${encodeURIComponent(searchTerm.trim())}`;
		}
	}

	// Gestione input ricerca con debounce
	async function onSearchInput() {
		clearTimeout(debounceTimer);
		if (searchTerm.length < 2) {
			searchResults = [];
			return;
		}
		debounceTimer = setTimeout(async () => {
			try {
				const response = await fetch(
					`${API_BASE_URL}/api/cerca?q=${encodeURIComponent(searchTerm)}`
				);
				if (response.ok) searchResults = await response.json();
			} catch (e) {
				console.error('Errore autocompletamento ricerca:', e);
			}
		}, SEARCH_DEBOUNCE_MS);
	}

	// Ottiene la posizione precisa tramite geolocalizzazione del browser
	async function getPreciseLocation() {
		if (!('geolocation' in navigator)) return;
		isLoadingPrecise = true;
		navigator.geolocation.getCurrentPosition(
			async (position) => {
				const { latitude, longitude } = position.coords;
				try {
					const response = await fetch(
						`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`
					);
					if (response.ok) {
						const data = await response.json();
						const city = data.address.city || data.address.town || data.address.village;
						const country = data.address.country_code.toUpperCase();
						location = `${city}, ${country}`;
						locationSource = 'precise';
					} else {
						location = `Lat: ${latitude.toFixed(2)}, Lon: ${longitude.toFixed(2)}`;
						locationSource = 'precise';
					}
				} catch (error) {
					location = 'Indirizzo non trovato';
				}
				isLoadingPrecise = false;
			},
			(error) => {
				console.error('Errore geolocalizzazione:', error);
				if (error.code === 1) alert('Hai negato il permesso alla geolocalizzazione.');
				isLoadingPrecise = false;
			}
		);
	}

	// Inizializzazione al mount del componente
	onMount(async () => {
		try {
			const response = await fetch(`${API_BASE_URL}/api/geo-ip`);
			if (response.ok) {
				const data = await response.json();
				location = data.error ? data.error : `${data.city}, ${data.country_code}`;
				if (!data.error) locationSource = 'ip';
			} else {
				location = 'Posizione non trovata';
			}
		} catch (error) {
			console.error('Errore nel fetch della geolocalizzazione IP:', error);
			location = 'Backend non raggiungibile';
		}
	});
</script>

<nav class="navbar-theme sticky top-0 z-50 shadow-lg">
	<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
		<div class="flex h-16 items-center justify-between gap-8">
			<!-- Logo e posizione -->
			<div class="flex items-center gap-6">
				<div class="flex-shrink-0">
					<a href="/" class="text-2xl font-bold text-black hover:text-indigo-300"> POS Register </a>
				</div>

				<!-- Indicatore posizione -->
				<div class="hidden items-center text-sm text-black lg:flex">
					<svg class="mr-2 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
						<path
							fill-rule="evenodd"
							d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
							clip-rule="evenodd"
						/>
					</svg>
					<span>{location}</span>
					{#if locationSource === 'ip' && !isLoadingPrecise}
						<button
							on:click={getPreciseLocation}
							title="Migliora precisione"
							class="ml-2 text-indigo-400 hover:text-indigo-300"
						>
							<svg class="h-5 w-5" viewBox="0 0 20 20" fill="black">
								<path
									d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"
								/>
							</svg>
						</button>
					{/if}
					{#if isLoadingPrecise}
						<div class="ml-2">
							<svg class="h-5 w-5 animate-spin text-black" fill="none" viewBox="0 0 24 24">
								<circle
									class="opacity-25"
									cx="12"
									cy="12"
									r="10"
									stroke="currentColor"
									stroke-width="4"
								></circle>
								<path
									class="opacity-75"
									fill="currentColor"
									d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
								></path>
							</svg>
						</div>
					{/if}
				</div>
			</div>

			<!-- Barra di ricerca desktop -->
			<div class="hidden flex-grow items-center justify-center md:flex">
				<div
					class="relative w-full max-w-md"
					on:focusin={() => (isSearchFocused = true)}
					on:focusout={() => setTimeout(() => (isSearchFocused = false), 200)}
				>
					<form on:submit|preventDefault={handleSearchSubmit}>
						<input
							type="text"
							bind:value={searchTerm}
							on:input={onSearchInput}
							placeholder="Cerca prodotti..."
							class="search-theme w-full rounded-full border py-2 pl-10 pr-4 text-black transition focus:outline-none focus:ring-2 focus:ring-indigo-500"
						/>
						<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
							<svg class="h-5 w-5 text-slate-500" viewBox="0 0 20 20" fill="currentColor">
								<path
									fill-rule="evenodd"
									d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
									clip-rule="evenodd"
								/>
							</svg>
						</div>
					</form>

					<!-- Risultati ricerca autocompletamento -->
					{#if isSearchFocused && searchResults.length > 0}
						<div
							class="absolute top-full z-20 mt-2 w-full overflow-hidden rounded-lg bg-white shadow-lg"
						>
							<ul class="divide-y divide-gray-200">
								{#each searchResults as prodotto}
									<li class="hover:bg-gray-100">
										<a
											href="/prodotto/{createSlug(prodotto.nome)}"
											class="flex items-center p-3 text-gray-800"
										>
											<img
												src={prodotto.immagine_url}
												alt={prodotto.nome}
												class="mr-3 h-10 w-10 rounded-md object-cover"
											/>
											<span>{prodotto.nome}</span>
										</a>
									</li>
								{/each}
							</ul>
						</div>
					{/if}
				</div>
			</div>

			<!-- Icone azioni utente -->
			<div class="flex flex-shrink-0 items-center space-x-2">
				<!-- Pulsante ricerca mobile -->
				<button
					on:click={() => (isMobileSearchOpen = true)}
					class="rounded-full p-2 transition-colors hover:bg-slate-800 md:hidden"
					aria-label="Apri ricerca"
				>
					<svg
						class="h-6 w-6 text-white"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
						/>
					</svg>
				</button>

				<!-- Carrello -->
				<div class="relative" use:clickOutsideCarrello>
					<button
						on:click={toggleCartMenu}
						class="relative rounded-full p-2 transition-colors hover:bg-slate-800"
						title="Carrello"
						aria-label="Apri menù carrello"
					>
						<svg
							class="h-6 w-6 text-black"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
							/>
						</svg>
						{#if $cartItemsCount > 0}
							<span
								class="absolute right-0 top-0 flex h-5 w-5 items-center justify-center rounded-full bg-red-600 text-xs text-white ring-2 ring-slate-900"
							>
								{$cartItemsCount}
							</span>
						{/if}
					</button>

					<!-- Menu carrello -->
					{#if $isCartOpenMobile}
						<CartMenu />
					{/if}
				</div>

				<!-- Menu utente -->
				<div class="relative" use:clickOutsideUser>
					<button
						on:click={toggleUserMenu}
						class="rounded-full p-2 transition-colors hover:bg-slate-800"
						aria-label="Apri menù utente"
					>
						<svg class="h-6 w-6 text-black" viewBox="0 0 20 20" fill="currentColor">
							<path
								fill-rule="evenodd"
								d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
								clip-rule="evenodd"
							/>
						</svg>
					</button>

					<!-- Dropdown menu utente -->
					{#if isUserMenuOpen}
						<div
							class="absolute right-0 z-10 mt-2 w-56 rounded-md bg-white py-1 text-black shadow-lg"
						>
							{#if $utente}
								<div class="border-b px-4 py-2 text-sm text-gray-500">
									Accesso effettuato come:<br />
									<span class="font-medium text-gray-800">{$utente.email}</span>
								</div>
								<a href="/profilo" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
									Il Mio Profilo
								</a>
								<button
									on:click={() => {
										utente.logout();
										isUserMenuOpen = false;
									}}
									class="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100"
								>
									Logout
								</button>
							{:else}
								<a
									href="/login?redirectTo={$page.url.pathname}"
									class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
								>
									Accedi
								</a>
								<a
									href="/registrazione?redirectTo={$page.url.pathname}"
									class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
								>
									Registrati
								</a>
							{/if}
						</div>
					{/if}
				</div>
			</div>
		</div>
	</div>
</nav>

<!-- Overlay ricerca mobile -->
{#if isMobileSearchOpen}
	<div class="fixed inset-0 z-50 bg-white/50 backdrop-blur-sm" aria-modal="true">
		<div class="p-4">
			<form on:submit|preventDefault={handleSearchSubmit} class="relative">
				<input
					type="search"
					bind:value={searchTerm}
					placeholder="Cerca prodotti..."
					class="search-theme w-full rounded-full border py-3 pl-12 pr-10 text-black transition focus:outline-none focus:ring-2 focus:ring-indigo-500"
				/>
				<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4">
					<svg class="h-5 w-5 text-slate-500" viewBox="0 0 20 20" fill="currentColor">
						<path
							fill-rule="evenodd"
							d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
							clip-rule="evenodd"
						/>
					</svg>
				</div>
			</form>
			<button
				on:click={() => (isMobileSearchOpen = false)}
				class="absolute right-6 top-6 text-slate-400 hover:text-white"
				aria-label="Chiudi ricerca"
			>
				<svg class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
					<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
				</svg>
			</button>
		</div>
	</div>
{/if}