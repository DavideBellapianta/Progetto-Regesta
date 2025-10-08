<script>
	import { onMount } from 'svelte';

	// 1. Il componente ora accetta la categoria del prodotto corrente
	export let category = 'other'; // 'other' come valore di default

	// 2. Una lista di recensioni molto più grande e categorizzata
	const allReviews = [
		// --- Categoria Food ---
		{ category: 'food', author: 'Carla G.', rating: 5, text: 'Gusto eccezionale, si sente la qualità degli ingredienti. Ricomprerò sicuramente.' },
		{ category: 'food', author: 'Davide M.', rating: 4, text: 'Molto buono e fresco. La confezione era pratica e ben sigillata.' },
		{ category: 'food', author: 'Simone F.', rating: 3, text: 'Non male, ma il sapore è un po’ anonimo rispetto ad altre marche.' },
        { category: 'food', author: 'Laura P.', rating: 5, text: 'Il migliore che abbia mai provato! Vale ogni centesimo speso.' },

		// --- Categoria Medical ---
		{ category: 'medical', author: 'Roberto T.', rating: 5, text: 'Prodotto efficace e facile da usare. Ha risolto il mio problema in poco tempo.' },
		{ category: 'medical', author: 'Elena S.', rating: 4, text: 'Fa quello che promette. Ottimo rapporto qualità-prezzo per un prodotto di questo tipo.' },
		{ category: 'medical', author: 'Franco B.', rating: 2, text: 'Purtroppo su di me non ha avuto l\'effetto sperato. Molto deludente.' },
        { category: 'medical', author: 'Marta L.', rating: 5, text: 'Indispensabile da tenere in casa per ogni evenienza. Consigliatissimo.' },

		// --- Categoria Other ---
		{ category: 'other', author: 'Giovanni R.', rating: 5, text: 'Materiali di ottima qualità, robusto e ben costruito. Superiore alle aspettative.' },
		{ category: 'other', author: 'Valentina C.', rating: 3, text: 'Funziona, ma il design potrebbe essere migliorato. Un po’ ingombrante.' },
		{ category: 'other', author: 'Alessandro D.', rating: 4, text: 'Un buon prodotto versatile, utile in molte situazioni. Soddisfatto dell\'acquisto.' },
        { category: 'other', author: 'Chiara Z.', rating: 5, text: 'Esattamente quello che cercavo. Arrivato in un giorno, servizio impeccabile.' }
	];

	let reviewsToShow = [];

	onMount(() => {
		// 3. Filtra le recensioni in base alla categoria ricevuta
		const relevantReviews = allReviews.filter(review => review.category === category);

		// Mescola l'array filtrato
		const shuffled = relevantReviews.sort(() => 0.5 - Math.random());
		
        // Seleziona un massimo di 3 recensioni da mostrare
		reviewsToShow = shuffled.slice(0, 3);
	});
</script>

<div class="mt-10 pt-6 border-t border-gray-200">
	<h2 class="text-2xl font-bold text-gray-900 mb-6">Recensioni dei Clienti</h2>

	<div class="space-y-6">
        {#if reviewsToShow.length > 0}
            {#each reviewsToShow as review}
                <div class="p-4 bg-gray-50 rounded-lg border border-gray-200">
                    <div class="flex items-center mb-2">
                        <div class="flex items-center">
                            {#each { length: 5 } as _, i}
                                <svg
                                    class="h-5 w-5"
                                    class:text-yellow-400={i < review.rating}
                                    class:text-gray-300={i >= review.rating}
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                >
                                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                </svg>
                            {/each}
                        </div>
                        <p class="ml-3 font-semibold text-gray-800">{review.author}</p>
                    </div>
                    <p class="text-gray-600">{review.text}</p>
                </div>
            {/each}
        {:else}
            <p class="text-gray-500">Non ci sono ancora recensioni per questa categoria di prodotti.</p>
        {/if}
	</div>
</div>