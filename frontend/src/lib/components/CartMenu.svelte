<script>
	import { cart } from '../stores.js';

	let subtotal = 0;
	$: subtotal = $cart.reduce((sum, item) => sum + item.prezzo_lordo * item.quantita, 0);
    
</script>

<div
	class="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-xl z-50 text-black overflow-hidden
           max-md:fixed max-md:inset-x-0 max-md:bottom-0 max-md:w-full max-md:rounded-t-lg max-md:rounded-b-none"
	role="dialog"
	aria-modal="true"
>
	<div class="p-4">
		<h3 class="text-lg font-semibold text-gray-900">Riepilogo Carrello</h3>

		<div class="mt-4 max-h-64 max-md:h-40 overflow-y-auto pr-2">
			{#if $cart.length > 0}
				<ul class="space-y-4">
					{#each $cart as item}
						<li class="flex items-center space-x-3">
							<img
								src={item.immagine_url}
								alt={item.nome}
								class="h-16 w-16 object-cover rounded-md flex-shrink-0"
							/>
							<div class="flex-1 min-w-0">
								<p class="font-semibold text-sm truncate" title={item.nome}>{item.nome}</p>
								
								<div class="flex items-center text-xs text-gray-600 mt-1">
									<button on:click={() => cart.decrement(item.nome)} class="px-2 py-0.5 border rounded-md hover:bg-gray-100">-</button>
									<span class="px-3 font-bold">{item.quantita}</span>
									<button on:click={() => cart.increment(item.nome)} class="px-2 py-0.5 border rounded-md hover:bg-gray-100">+</button>
								</div>
							</div>
							
                            <div class="text-right">
                                <p class="font-semibold text-sm">
                                    {(item.prezzo_lordo * item.quantita).toFixed(2)}€
                                </p>
                                <button on:click={() => cart.remove(item.nome)} class="text-xs text-black-500 hover:underline mt-1">
                                    Rimuovi
                                </button>
                            </div>
						</li>
					{/each}
				</ul>
			{:else}
				<p class="text-center text-gray-500 py-8">Il tuo carrello è vuoto.</p>
			{/if}
		</div>

		{#if $cart.length > 0}
			<div class="border-t border-gray-200 mt-4 pt-4">
				<div class="flex justify-between font-semibold">
					<span>Subtotale</span>
					<span>{subtotal.toFixed(2)}€</span>
				</div>
				<a
					href="/carrello"
					class="block text-center w-full mt-4 bg-indigo-600 text-white py-2 rounded-lg font-semibold transition hover:bg-indigo-700"
				>
					Vai al Carrello
				</a>
			</div>
		{/if}
	</div>
</div>