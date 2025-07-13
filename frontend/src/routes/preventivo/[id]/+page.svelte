<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { quotes, policies } from '$lib/api';
	import type { QuoteData } from '$lib/api'; // Assumendo che questo tipo esista
	import { base } from '$app/paths';

	// === STATO DEL COMPONENTE ===
	let quote = $state<any>(null); // Qui andranno i dettagli del preventivo
	let isLoading = $state(true);
	let isActivating = $state(false); // Stato specifico per il processo di attivazione
	let error = $state<string | null>(null);

	// === LOGICA DI CARICAMENTO DATI ===
	onMount(async () => {
		try {
			// Prendiamo l'ID del preventivo direttamente dai parametri dell'URL
			const quoteId = parseInt(page.params.id);
			if (isNaN(quoteId)) {
				throw new Error('ID del preventivo non valido.');
			}
			quote = await quotes.getById(quoteId);
		} catch (e: any) {
			console.error(e);
			error = `Impossibile caricare il preventivo: ${e.message}`;
		} finally {
			isLoading = false;
		}
	});

	// === LOGICA DI ATTIVAZIONE POLIZZA ===
	async function handleActivate() {
		if (!quote || isActivating) return;

		isActivating = true;
		error = null; // Resetta errori precedenti

		try {
			// Chiamiamo il nuovo endpoint per creare la polizza dal preventivo
			const newPolicy = await policies.createFromQuote(quote.id);
			console.log('Polizza attivata con successo:', newPolicy);

			// Successo! Reindirizziamo l'utente alla dashboard
			// con un parametro per mostrare un messaggio di conferma.
			goto(base+'/dashboard?activated=true');

		} catch (e: any) {
			console.error('Errore di attivazione:', e);
			error = `Attivazione fallita: ${e.message}`;
		} finally {
			isActivating = false;
		}
	}
</script>

<div class="min-h-screen bg-gray-50 p-8">
	<div class="max-w-2xl mx-auto">
		{#if isLoading}
			<div class="text-center py-16">
				<p class="text-lg text-gray-500">Caricamento dettagli preventivo...</p>
			</div>
		{:else if error && !quote}
			<!-- Mostra errore solo se non siamo riusciti a caricare nulla -->
			<div class="bg-white p-6 rounded-lg shadow text-center">
				<p class="text-red-500 font-semibold">{error}</p>
				<a href={base+"/dashboard"} class="mt-4 inline-block text-blue-500 hover:underline">
					← Torna alla dashboard
				</a>
			</div>
		{:else if quote}
			<div class="bg-white p-8 rounded-2xl shadow-xl">
				<div class="flex justify-between items-center border-b pb-4 mb-6">
					<div>
						<h1 class="text-3xl font-bold text-gray-900">Riepilogo Preventivo</h1>
						<p class="text-gray-500">Pronto per essere attivato!</p>
					</div>
					<a href={base+"/dashboard"} class="text-sm text-blue-600 hover:underline">← Dashboard</a>
				</div>

				<!-- Dettagli del Veicolo -->
				<div class="space-y-4">
					<h2 class="text-xl font-semibold text-gray-700">Dettagli Veicolo</h2>
					<div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4 bg-gray-50 p-4 rounded-lg">
						<div>
							<p class="text-sm font-medium text-gray-500">Marca e Modello</p>
							<p class="font-semibold text-gray-800">{quote.car_brand} {quote.car_model}</p>
						</div>
						<div>
							<p class="text-sm font-medium text-gray-500">Targa</p>
							<p class="font-semibold text-gray-800">{quote.license_plate}</p>
						</div>
						<div>
							<p class="text-sm font-medium text-gray-500">Stile di Guida</p>
							<p class="font-semibold text-gray-800 capitalize">{quote.driving_style}</p>
						</div>
						<div>
							<p class="text-sm font-medium text-gray-500">Km Annui Stimati</p>
							<p class="font-semibold text-gray-800">{quote.km_per_year} km</p>
						</div>
					</div>

					<!-- Prezzo e Azione -->
					<div class="text-center border-t pt-6 mt-6">
						<p class="text-lg text-gray-600">Premio annuale</p>
						<p class="text-5xl font-extrabold text-green-600 my-2">
							€{parseFloat(quote.premium_price).toFixed(2)}
						</p>

						{#if error}
							<p class="text-red-500 my-4">{error}</p>
						{/if}

						<button
							onclick={handleActivate}
							disabled={isActivating}
							class="w-full mt-4 px-6 py-4 bg-green-500 text-white font-bold text-lg rounded-lg shadow-md
								   hover:bg-green-600 transition-all duration-200 transform hover:scale-105
								   disabled:bg-gray-400 disabled:cursor-not-allowed disabled:transform-none"
						>
							{#if isActivating}
								Attivazione in corso...
							{:else}
								Conferma Pagamento e Attiva Polizza
							{/if}
						</button>
						<p class="text-xs text-gray-400 mt-2">
							Verrai reindirizzato alla dashboard dopo l'attivazione.
						</p>
					</div>
				</div>
			</div>
		{/if}
	</div>
</div>

<style lang="postcss">
	/* Selezioniamo tutti gli elementi <button> in questo componente */
	button {
		/* Usiamo @apply per "iniettare" le utility class di Tailwind */
		@apply cursor-pointer;
	}
</style>