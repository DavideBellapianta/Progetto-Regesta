<script>
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { utente } from '$lib/stores.js';


	let email = '';
	let password = '';
	let error = null;
	let isLoading = false;

	async function handleLogin() {
		isLoading = true;
		error = null;
		try {
			await utente.login(email, password);
			const redirectTo = $page.url.searchParams.get('redirectTo') || '/';
			goto(redirectTo);
		} catch (e) {
			error = e.message;
		}
		isLoading = false;
	}
</script>

<main class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
	<div class="sm:mx-auto sm:w-full sm:max-w-sm">
		<h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
			Accedi al tuo account
		</h2>
	</div>

	<div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
		<form class="space-y-6" on:submit|preventDefault={handleLogin}>
			<div>
				<label for="email" class="block text-sm font-medium leading-6 text-gray-900">Email</label>
				<input bind:value={email} id="email" name="email" type="email" required class="mt-2 block w-full rounded-md border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300"/>
			</div>

			<div>
				<label for="password" class="block text-sm font-medium leading-6 text-gray-900">Password</label>
				<input bind:value={password} id="password" name="password" type="password" required class="mt-2 block w-full rounded-md border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300"/>
			</div>
			
			{#if error}
				<p class="text-sm text-red-600">{error}</p>
			{/if}

			<div>
				<button type="submit" disabled={isLoading} class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 disabled:opacity-50">
					{isLoading ? 'Accesso in corso...' : 'Accedi'}
				</button>
			</div>
		</form>

		<p class="mt-10 text-center text-sm text-gray-500">
			Non sei un membro?
			<a href="/registrazione?redirectTo={$page.url.searchParams.get('redirectTo') || '/'}" class="font-semibold text-indigo-600 hover:text-indigo-500">Registrati ora</a>
		</p>
	</div>
</main>