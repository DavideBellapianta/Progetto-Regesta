<script>
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { utente } from '$lib/stores.js';

	let email = '';
	let password = '';
	let error = null;
	let isLoading = false;
	let isPasswordVisible = false;

	async function handleLogin() {
		isLoading = true;
		error = null;
		try {
			await utente.login(email.toLowerCase(), password);
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
				<input
					bind:value={email}
					on:input={() => (email = email.toLowerCase())}
					id="email"
					name="email"
					type="email"
					required
					class="mt-2 block w-full rounded-md border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300"
				/>
			</div>

			<div>
				<label for="password" class="block text-sm font-medium leading-6 text-gray-900"
					>Password</label
				>
				<div class="relative mt-2">
					<input
						bind:value={password}
						id="password"
						name="password"
						type={isPasswordVisible ? 'text' : 'password'}
						required
						class="block w-full rounded-md border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300"
					/>
					<button
						type="button"
						on:click={() => (isPasswordVisible = !isPasswordVisible)}
						class="absolute inset-y-0 right-0 flex items-center pr-3"
						aria-label={isPasswordVisible ? 'Nascondi password' : 'Mostra password'}
					>
						{#if isPasswordVisible}
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="h-5 w-5 text-gray-500">
								<path fill-rule="evenodd" d="M3.28 2.22a.75.75 0 00-1.06 1.06l14.5 14.5a.75.75 0 101.06-1.06l-1.745-1.745a10.029 10.029 0 003.3-4.38 1.59 1.59 0 000-1.214.75.75 0 00-.033-.114l-.01-.019a10.03 10.03 0 00-3.213-4.415l-1.32-1.32a.75.75 0 00-1.06 1.06l1.099 1.099a8.53 8.53 0 012.33 3.328l-.001.002.002.002a8.53 8.53 0 01-2.33 3.328l-1.099-1.099a.75.75 0 10-1.06-1.06l-1.32-1.32a8.53 8.53 0 01-3.328-2.33l-.002-.002a.75.75 0 00-.005-.008l-.009-.01a8.53 8.53 0 01-3.328-2.33l1.099 1.099a.75.75 0 001.06-1.06l-1.745-1.745z" clip-rule="evenodd" />
								<path d="M11.32 7.68a.75.75 0 00-1.06-1.06l-1.32 1.32a1.5 1.5 0 00-2.12 2.12l1.32-1.32a.75.75 0 001.06 1.06l-1.099-1.099a2.25 2.25 0 113.182-3.182l-1.099 1.099z" />
							</svg>
						{:else}
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="h-5 w-5 text-gray-500">
								<path d="M10 12.5a2.5 2.5 0 100-5 2.5 2.5 0 000 5z" />
								<path fill-rule="evenodd" d="M.664 10.59a1.651 1.651 0 010-1.186A10.004 10.004 0 0110 3c4.257 0 7.893 2.66 9.336 6.41.772 1.928.772 4.09 0 6.018A10.004 10.004 0 0110 17c-4.257 0-7.893-2.66-9.336-6.41a1.651 1.651 0 010-1.186zM10 15a5 5 0 100-10 5 5 0 000 10z" clip-rule="evenodd" />
							</svg>
						{/if}
					</button>
				</div>
			</div>

			{#if error} <p class="text-sm text-red-600">{error}</p> {/if}

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