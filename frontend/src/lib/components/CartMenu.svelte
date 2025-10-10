<script>
	import { cart } from '../stores.js';
	import { createSlug } from '$lib/utils.js';

	let subtotal = 0;
	$: subtotal = $cart.reduce((sum, item) => sum + item.prezzo_lordo * item.quantita, 0);
</script>

<div
	class="absolute right-0 z-50 mt-2 w-80 overflow-hidden rounded-lg bg-white text-black shadow-xl
           max-md:fixed max-md:inset-x-0 max-md:bottom-0 max-md:w-full max-md:rounded-b-none max-md:rounded-t-lg"
	role="dialog"
	aria-modal="true"
>
	<div class="p-4">
		<h3 class="text-lg font-semibold text-gray-900">Riepilogo Carrello</h3>

		<div class="mt-4 max-h-64 overflow-y-auto pr-2 max-md:h-40">
			{#if $cart.length > 0}
				<ul class="space-y-4">
					{#each $cart as item}
						<li class="flex items-center space-x-3">
							<a href="/prodotto/{createSlug(item.nome)}">
								<img
									src={item.immagine_url}
									alt={item.nome}
									class="h-16 w-16 flex-shrink-0 rounded-md object-cover"
								/>
							</a>
							<div class="min-w-0 flex-1">
								<a href="/prodotto/{createSlug(item.nome)}" data-sveltekit-reload>
									<p class="truncate text-sm font-semibold hover:underline" title={item.nome}>
										{item.nome}
									</p>
								</a>

								<div class="mt-1 flex items-center text-xs text-gray-600">
									<button
										on:click={() => cart.decrement(item.nome)}
										class="rounded-md border px-2 py-0.5 hover:bg-gray-100">-</button
									>
									<span class="px-3 font-bold">{item.quantita}</span>
									<button
										on:click={() => cart.increment(item.nome)}
										class="rounded-md border px-2 py-0.5 hover:bg-gray-100">+</button
									>
								</div>
							</div>

							<div class="text-right">
								<p class="text-sm font-semibold">
									{(item.prezzo_lordo * item.quantita).toFixed(2)}€
								</p>
								<button
									on:click={() => cart.remove(item.nome)}
									class="text-black-500 mt-1 text-xs hover:underline"
								>
									Rimuovi
								</button>
							</div>
						</li>
					{/each}
				</ul>
			{:else}
				<p class="py-8 text-center text-gray-500">Il tuo carrello è vuoto.</p>
			{/if}
		</div>

		{#if $cart.length > 0}
			<div class="mt-4 border-t border-gray-200 pt-4">
				<div class="flex justify-between font-semibold">
					<span>Subtotale</span>
					<span>{subtotal.toFixed(2)}€</span>
				</div>
				<a
					href="/carrello"
					class="mt-4 block w-full rounded-lg bg-indigo-600 py-2 text-center font-semibold text-white transition hover:bg-indigo-700"
				>
					Vai al Carrello
				</a>
			</div>
		{/if}
	</div>
</div>