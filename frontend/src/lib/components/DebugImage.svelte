<script>
	import { onMount } from 'svelte';

	let imageUrl = null;
	let error = null;

	onMount(async () => {
		console.log('DebugImage: Inizio fetch a /api/random-image');
		try {
			const response = await fetch('http://127.0.0.1:5000/api/random-image');
			console.log('DebugImage: Risposta ricevuta', response);

			if (response.ok) {
				const data = await response.json();
				if (data && data.immagine_url) {
					console.log('DebugImage: URL immagine trovato:', data.immagine_url);
					imageUrl = data.immagine_url;
				} else {
					throw new Error('I dati ricevuti non contengono un URL immagine valido.');
				}
			} else {
				throw new Error(`Il server ha risposto con errore: ${response.status} ${response.statusText}`);
			}
		} catch (e) {
			console.error('DebugImage: Errore CATTURATO durante il fetch:', e);
			error = e.message;
		}
	});
</script>

<div class="border-4 border-dashed border-red-500 p-4 my-8">
	<h2 class="text-2xl font-bold text-black mb-4">-- Test di Debug Immagine --</h2>

	{#if imageUrl}
		<h3 class="text-green-700 font-bold">SUCCESSO! Immagine caricata dal backend:</h3>
		<img src={imageUrl} alt="Immagine di test dal backend" class="mt-4 border-2 border-green-500" />
	{:else if error}
		<h3 class="text-red-700 font-bold">ERRORE! Impossibile caricare l'immagine.</h3>
		<p class="text-black mt-2">Dettaglio errore: <span class="font-mono bg-red-100 p-1">{error}</span></p>
		<p class="text-black mt-2">
			Controlla la scheda "Console" e "Network" negli strumenti per sviluppatori (F12) per maggiori
			dettagli.
		</p>
	{:else}
		<p class="text-blue-700 font-bold">Caricamento in corso...</p>
	{/if}
</div>