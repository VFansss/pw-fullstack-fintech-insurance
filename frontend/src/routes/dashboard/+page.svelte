<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { auth, quotes } from '$lib/api';
    import type { QuoteData } from '$lib/api'; // Importiamo il tipo se lo hai definito

	// === STATO DEL COMPONENTE ===
	let user = $state({ username: '', first_name: '' });
	let userQuotes = $state<any[]>([]); // Usiamo 'any' per semplicità, ma potresti definire un tipo Quote
	let isLoading = $state(true); // Stato di caricamento per un'ottima UX
	let error = $state<string | null>(null);

	// === LOGICA DI CARICAMENTO E PROTEZIONE DELLA PAGINA ===
	onMount(async () => {
		const token = localStorage.getItem('authToken');
		if (!token) {
			goto('/login');
			return;
		}

		try {
			// Carichiamo i dati dell'utente e i preventivi IN PARALLELO
			// Questo è più performante che aspettare prima uno e poi l'altro.
			const [userData, quotesData] = await Promise.all([
				auth.getUser(),
				quotes.getAll()
			]);

			user = userData;
			userQuotes = quotesData;

		} catch (e) {
			// Il token non è valido/scaduto o c'è un altro errore API.
			localStorage.removeItem('authToken');
			error = 'La tua sessione è scaduta o si è verificato un errore. Effettua nuovamente il login.';
			setTimeout(() => goto('/login'), 2500);
		} finally {
			// In ogni caso, il caricamento è terminato.
			isLoading = false;
		}
	});

	// === Logica per il LOGOUT (invariata) ===
	async function handleLogout() {
		try {
			await auth.logout();
		} catch (error) {
			console.error("Errore durante il logout sul server:", error);
		} finally {
			localStorage.removeItem('authToken');
			goto('/login');
		}
	}
</script>

<div class="min-h-screen bg-gray-50 p-8">
	<div class="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow">
		{#if isLoading}
            <!-- 1. STATO DI CARICAMENTO -->
			<div class="text-center py-16">
				<p class="text-lg text-gray-500">Caricamento della tua area personale...</p>
                <!-- Aggiungi uno spinner o un'animazione qui se vuoi -->
			</div>
		{:else if error}
            <!-- 2. STATO DI ERRORE -->
			<p class="text-red-500 text-center py-16">{error}</p>
		{:else}
            <!-- 3. STATO CON DATI CARICATI -->
			<div class="flex justify-between items-start">
				<div>
					<h1 class="text-3xl font-bold text-gray-800">
						Bentornato, <span class="text-blue-600">{user.first_name || user.username}</span>!
					</h1>
					<p class="text-gray-600 mt-2">
						Questa è la tua dashboard di AlCoperto.
					</p>
				</div>
				<button
					onclick={handleLogout}
					class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
				>
					Logout
				</button>
			</div>

			<!-- Sezione Preventivi -->
			<div class="mt-8">
				<h2 class="text-2xl font-semibold text-gray-700 border-b pb-2 mb-4">I Tuoi Preventivi</h2>
				{#if userQuotes.length > 0}
					<ul class="space-y-4">
						{#each userQuotes as quote (quote.id)}
							<li class="border p-4 rounded-lg hover:shadow-md transition-shadow duration-200">
								<div class="flex justify-between items-center">
									<div>
										<p class="font-bold text-lg text-gray-800">{quote.car_brand} {quote.car_model}</p>
										<p class="text-sm text-gray-500">Targa: {quote.license_plate}</p>
										<p class="text-xs text-gray-400 mt-1">Creato il: {new Date(quote.created_at).toLocaleDateString()}</p>
									</div>
									<div class="text-right">
										<p class="text-xl font-light text-green-600">€{quote.premium_price}</p>
										<button 
											onclick={() => goto(`/preventivo/${quote.id}`)}
											class="mt-2 text-sm text-white bg-blue-600 px-3 py-1 rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
											Paga e Attiva
										</button>
									</div>
								</div>
							</li>
						{/each}
					</ul>
				{:else}
					<div class="text-center py-8 px-4 border-2 border-dashed rounded-lg">
						<p class="text-gray-500">Non hai ancora richiesto nessun preventivo.</p>
						<a href="/preventivatore" class="mt-2 inline-block px-4 py-2 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition-colors">
							Fai un preventivo ora
						</a>
					</div>
				{/if}
			</div>
            
            <!-- Aggiungi qui la sezione per le Polizze Attive -->

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