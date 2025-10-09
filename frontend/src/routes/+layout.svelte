<script>
	import { onMount } from 'svelte';
	import Navbar from '$lib/components/Navbar.svelte';
	import SnakeGame from '$lib/components/SnakeGame.svelte';
	import { utente } from '$lib/stores.js'; // Assicurati di importare lo store utente
	import '../app.css';

	// Importiamo tutti e tre i blob
	import blob from '$lib/assets/blob.svg';
	import blob1 from '$lib/assets/blob (1).svg';
	import blob2 from '$lib/assets/blob (2).svg';

	let showSnake = false;
	const secretCode = ['s', 'n', 'a', 'k', 'e'];
	let keySequence = [];

	function handleSecretCode(e) {
		keySequence.push(e.key.toLowerCase());
		keySequence.splice(-secretCode.length - 1, keySequence.length - secretCode.length);
		if (keySequence.join('') === secretCode.join('')) {
			showSnake = !showSnake;
		}
	}
	onMount(() => {
		utente.checkAuth();
	});
</script>

<svelte:window on:keydown={handleSecretCode} />

{#if showSnake}
	<SnakeGame />
{/if}

<div class="relative min-h-screen">
	<div aria-hidden="true" class="fixed inset-0 -z-10 overflow-hidden">
		<div
			class="absolute inset-0"
			style="background-image: radial-gradient(circle at 1px 1px, rgba(0, 0, 0, 0.25) 1px, transparent 0); background-size: 20px 20px;"
		></div>
		<img
			src={blob1}
			alt=""
			class="animate-blob animation-delay-2000 -right-120 scale-120 absolute -top-80 h-[60rem] w-[80rem] text-indigo-500 opacity-80"
		/>

		<img
			src={blob2}
			alt=""
			class="animate-blob animation-delay-4000 -left-90 -top-50 absolute h-[55rem] w-[55rem] text-teal-400 opacity-80"
		/>

		<img
			src={blob}
			alt=""
			class="animate-blob left-160 absolute -bottom-1/2 h-[60rem] w-[60rem] -translate-x-1/2 text-purple-500 opacity-80"
		/>
	</div>
	
	<div class="isolate flex min-h-screen flex-col">
		<Navbar />
		<main class="flex-grow">
			<slot />
		</main>
	</div>
</div>
