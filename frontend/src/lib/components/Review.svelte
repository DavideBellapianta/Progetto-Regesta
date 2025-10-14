<script>
    import { onMount } from 'svelte';

    export let category = 'other';
    // NUOVO: Riceve l'elenco completo delle recensioni come prop
    export let allReviews = [];

    let reviewsToShow = [];

    onMount(() => {
        // La logica interna rimane la stessa, ma ora usa la prop 'allReviews'
        const relevantReviews = allReviews.filter(review => review.category === category);
        const shuffled = relevantReviews.sort(() => 0.5 - Math.random());
        reviewsToShow = shuffled.slice(0, 3);
    });
</script>

<div class="mt-10 border-t border-gray-200 pt-6">
    <h2 class="mb-6 text-2xl font-bold text-gray-900">Recensioni dei Clienti</h2>

    <div class="space-y-6">
        {#if reviewsToShow.length > 0}
            {#each reviewsToShow as review}
                <div class="rounded-lg border border-gray-200 bg-gray-50 p-4">
                    <div class="mb-2 flex items-center">
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