<script>
	import Card from './Card.svelte';

	export let title;
	export let products = [];

	let currentIndex = 0;
	let visibleCount = 4;
	let windowWidth = 0;
	let touchStartX = 0;
	let touchEndX = 0;

	function goNext() { //Prodotto successivo
		if (currentIndex < products.length - visibleCount) {
			currentIndex += 1;
		}
	}

	function goPrev() { //Prodotto precedente
		if (currentIndex > 0) {
			currentIndex -= 1;
		}
	}

	$: visibleCount = (() => { //Numero di prodotti in base alla larghezza
		if (windowWidth < 640) return 1;
		if (windowWidth < 768) return 2;
		if (windowWidth < 1024) return 3;
		return 4;
	})();

	$: displayedProducts = products.slice(currentIndex, currentIndex + visibleCount);
	$: canGoPrev = currentIndex > 0;
	$: canGoNext = currentIndex < products.length - visibleCount;
</script>

<svelte:window bind:innerWidth={windowWidth} />

<section class="mb-12">
	<h2 class="text-3xl font-bold text-gray-900 mb-6">{title}</h2>

	<div class="relative">
		{#if products.length > visibleCount}
			<button
				on:click={goPrev}
				disabled={!canGoPrev}
				class="absolute top-1/2 -translate-y-1/2 -left-4 z-10 bg-white rounded-full p-2 shadow-md hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed transition"
				aria-label="Prodotto precedente"
			>
				<svg class="h-6 w-6 text-gray-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
				</svg>
			</button>
		{/if}

		<div
			class="overflow-hidden"
		>
			{#if products.length > 0}
				<div class="flex transition-transform duration-300 ease-in-out -mx-3">
					{#each displayedProducts as prodotto (prodotto.nome)}
						<div class="w-full sm:w-1/2 md:w-1/3 lg:w-1/4 px-3 flex-shrink-0">
							<Card {prodotto} />
						</div>
					{/each}
				</div>
			{:else}
				<p class="text-gray-500">Caricamento prodotti in corso...</p>
			{/if}
		</div>

		{#if products.length > visibleCount}
			<button
				on:click={goNext}
				disabled={!canGoNext}
				class="absolute top-1/2 -translate-y-1/2 -right-4 z-10 bg-white rounded-full p-2 shadow-md hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed transition"
				aria-label="Prodotto successivo"
			>
				<svg class="h-6 w-6 text-gray-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
				</svg>
			</button>
		{/if}
	</div>
</section>