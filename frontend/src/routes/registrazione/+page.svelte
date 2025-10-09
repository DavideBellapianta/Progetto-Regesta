<script>
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import Navbar from '$lib/components/Navbar.svelte';

	let email = '';
	let password = '';
	let nome = '';
	let cognome = '';

	let error = null;
	let success = null;
	let isLoading = false;

	async function handleRegister() {
		isLoading = true;
		error = null;
		success = null;

		try {
			const response = await fetch('http://127.0.0.1:5000/api/registrazione', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				// 2. Invia tutti e quattro i campi
				body: JSON.stringify({ email, password, nome, cognome })
			});
			const data = await response.json();
			if (response.ok) {
				success = 'Registrazione riuscita! Verrai reindirizzato al login...';
				setTimeout(() => {
					const redirectTo = $page.url.searchParams.get('redirectTo') || '/';
					goto(`/login?redirectTo=${redirectTo}`);
				}, 2000);
			} else {
				throw new Error(data.msg || 'Errore durante la registrazione.');
			}
		} catch (e) {
			error = e.message;
		}
		isLoading = false;
	}
</script>

<main class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
	<div class="sm:mx-auto sm:w-full sm:max-w-sm">
		<h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
			Crea un nuovo account
		</h2>
	</div>

	<div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
		<form class="space-y-6" on:submit|preventDefault={handleRegister}>
			
            <div class="grid grid-cols-2 gap-4">
				<div>
					<label for="nome" class="block text-sm font-medium leading-6 text-gray-900">Nome</label>
					<div class="mt-2">
						<input bind:value={nome} id="nome" type="text" required class="block w-full rounded-md border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300"/>
					</div>
				</div>
				<div>
					<label for="cognome" class="block text-sm font-medium leading-6 text-gray-900">Cognome</label>
					<div class="mt-2">
						<input bind:value={cognome} id="cognome" type="text" required class="block w-full rounded-md border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300"/>
					</div>
				</div>
			</div>
			
			<div>
				<label for="email" class="block text-sm font-medium leading-6 text-gray-900">Email</label>
				<div class="mt-2">
					<input bind:value={email} id="email" type="email" autocomplete="email" required class="block w-full rounded-md border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300"/>
				</div>
			</div>

			<div>
				<label for="password" class="block text-sm font-medium leading-6 text-gray-900">Password</label>
				<div class="mt-2">
					<input bind:value={password} id="password" type="password" autocomplete="new-password" required class="block w-full rounded-md border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300"/>
				</div>
			</div>
			
			{#if error} <p class="text-sm text-red-600">{error}</p> {/if}
			{#if success} <p class="text-sm text-green-600">{success}</p> {/if}

			<div>
				<button type="submit" disabled={isLoading} class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 ...">
					{isLoading ? 'Registrazione in corso...' : 'Registrati'}
				</button>
			</div>
		</form>

		<p class="mt-10 text-center text-sm text-gray-500">
			Sei già membro?
			<a href="/login" class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">Accedi</a>
		</p>
	</div>
</main>