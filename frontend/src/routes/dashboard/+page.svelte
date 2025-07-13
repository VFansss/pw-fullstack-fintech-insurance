<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { auth, quotes, policies, general } from '$lib/api';
    import PolicyChart from '$lib/components/PolicyChart.svelte';
    import { base } from '$app/paths';

	// === STATO DEL COMPONENTE ===
	let user = $state<any>({});
	let userQuotes = $state<any[]>([]);
	let userPolicies = $state<any[]>([]);
	let policyStats = $state<any[]>([]);
    let globalStats = $state({ total_policies: 0 });
	
	let isLoading = $state(true);
	let isClearing = $state(false);
	let error = $state<string | null>(null);

    // Icone per tipo veicolo: semplice, pulito, efficace.
    const ICONS: Record<string, string> = {
        auto: '🚗',
        moto: '🏍️',
        autocarro: '🚚'
    };

	// === LOGICA DI CARICAMENTO ===
	onMount(async () => {
		const token = localStorage.getItem('authToken');
		if (!token) { goto('/login'); return; }

		try {
            // Ora carichiamo tutto quello che ci serve in un colpo solo!
			const [userData, quotesData, policiesData, statsData, globalStatsData] = await Promise.all([
				auth.getUser(),
				quotes.getAll(),
				policies.getAll(),
				policies.getStats(),
                general.getGlobalStats()
			]);
			user = userData;
			userQuotes = quotesData;
			userPolicies = policiesData;
			policyStats = statsData;
            globalStats = globalStatsData;
		} catch (e) {
			localStorage.removeItem('authToken');
			error = 'Sessione scaduta o errore. Effettua nuovamente il login.';
			setTimeout(() => goto('/login'), 2500);
		} finally {
			isLoading = false;
		}
	});

	// === AZIONI UTENTE (logout e clear) ===
	async function handleLogout() {
		try { await auth.logout(); } catch (e) { console.error("Errore logout:", e); }
        finally { localStorage.removeItem('authToken'); goto('/login'); }
	}

    async function handleClearQuotes() {
        if (!confirm('Sei sicuro?')) return;
        isClearing = true;
        try { await quotes.clearAll(); userQuotes = []; }
        catch (e: any) { error = `Errore: ${e.message}`; }
        finally { isClearing = false; }
    }
</script>

<div class="min-h-screen bg-gray-100">
    <header class="bg-white shadow-sm sticky top-0 z-10">
        <div class="container mx-auto p-4 flex justify-between items-center">
            <a href={base+"/"} class="text-2xl font-bold text-blue-600">AlCoperto</a>
            {#if !isLoading && !error}
                <div>
                    <span class="text-gray-700 mr-4">Ciao, {user.first_name || user.username}!</span>
                    <button onclick={handleLogout} class="px-3 py-1 bg-red-500 text-white text-sm rounded hover:bg-red-600">
                        Logout
                    </button>
                </div>
            {/if}
        </div>
    </header>

    {#if !isLoading && !error}
    <section 
        class="bg-cover bg-center py-12 text-white relative"
        style="background-image: url('/mk-banner.jpg');"
    >
        <!-- Overlay per leggibilità -->
        <div class="absolute inset-0 bg-black opacity-50"></div>

        <div class="container mx-auto text-center relative">
            <h2 class="text-4xl font-extrabold tracking-tight">
                Un totale di <span class="text-yellow-300">{globalStats.total_policies}</span> veicoli sono sotto la nostra protezione
            </h2>
            <p class="mt-2 text-lg font-light">Grazie a tutti per la vostra fiducia!</p>
        </div>
    </section>
    {/if}

    <main class="container mx-auto p-4 md:p-8">
        {#if isLoading}
            <div class="text-center py-20"><p class="text-lg text-gray-600 animate-pulse">Caricamento dashboard...</p></div>
        {:else if error}
            <p class="text-red-500 text-center py-20">{error}</p>
        {:else}
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
                
                <!-- Colonna Principale con Polizze e Preventivi -->
                <div class="lg:col-span-2 space-y-8">

                    <!-- SEZIONE POLIZZE ATTIVE -->
                    <div class="bg-white p-6 rounded-xl shadow-lg">
                        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Le tue polizze attive</h2>
                        {#if userPolicies.length > 0}
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {#each userPolicies as policy (policy.id)}
                                    <div class="bg-gray-50 border border-gray-200 rounded-lg p-5 flex flex-col justify-between">
                                        <div>
                                            <div class="flex items-center mb-3">
                                                <!-- ORA POSSIAMO USARE I DATI ANNIDATI! -->
                                                <span class="text-4xl mr-4">{ICONS[policy.quote.vehicle_type] || '📄'}</span>
                                                <div>
                                                    <h3 class="font-bold text-lg text-gray-800">{policy.quote.car_brand} {policy.quote.car_model}</h3>
                                                    <p class="text-sm text-gray-500">Targa: {policy.quote.license_plate}</p>
                                                    <p class="text-sm text-gray-500">Guida: {policy.quote.driving_style}</p> 
                                                </div>
                                            </div>
                                            <ul class="text-sm space-y-2 mt-4">
                                                <li class="flex justify-between"><span>Numero Polizza:</span> <strong class="font-mono">#{policy.id}</strong></li>
                                                <li class="flex justify-between"><span>Inizio Copertura:</span> <strong>{new Date(policy.start_date).toLocaleDateString()}</strong></li>
                                                <li class="flex justify-between"><span>Fine Copertura:</span> <strong>{new Date(policy.end_date).toLocaleDateString()}</strong></li>
                                            </ul>
                                        </div>
                                        <div class="text-center mt-4 pt-4 border-t">
                                             <span class="px-3 py-1 text-xs font-bold uppercase tracking-wider bg-green-200 text-green-800 rounded-full">
                                                PAGATA
                                             </span>
                                        </div>
                                    </div>
                                {/each}
                            </div>
                        {:else}
                            <p class="text-center text-gray-500 py-4">Nessuna polizza attiva.</p>
                        {/if}
                    </div>

                    <!-- Sezione Preventivi (leggermente rivista) -->
                    <div class="bg-white p-6 rounded-xl shadow-lg">

                        <!-- Box dei Preventivi -->
						<div class="bg-gray-50 p-6 rounded-lg">
							<div class="flex justify-between items-center mb-4">
								<h2 class="text-2xl font-semibold text-gray-700">Preventivi in Attesa</h2>
								{#if userQuotes.length > 0}
									<button 
										onclick={handleClearQuotes}
										disabled={isClearing}
										class="text-sm font-medium text-red-500 hover:text-red-700 disabled:text-gray-400 disabled:cursor-wait"
									>
										{isClearing ? 'Cancellando...' : 'Pulisci tutti'}
									</button>
								{/if}
							</div>

							{#if userQuotes.length > 0}
								<ul class="space-y-4">
									{#each userQuotes as quote (quote.id)}
										<li class="border bg-white p-4 rounded-lg hover:shadow-lg hover:border-blue-300 transition-all duration-300">
											<a href={base+"/preventivo/{quote.id}"} class="block">
												<div class="flex justify-between items-center">
													<div>
														<p class="font-bold text-lg text-gray-800">{quote.car_brand} {quote.car_model}</p>
														<p class="text-sm text-gray-500">Targa: {quote.license_plate}</p>
														<p class="text-xs text-gray-400 mt-1">Creato il: {new Date(quote.created_at).toLocaleDateString()}</p>
													</div>
													<div class="text-right">
														<p class="text-xl font-bold text-blue-600">€{quote.premium_price}</p>
														<span class="text-sm text-blue-500 font-semibold">Dettagli →</span>
													</div>
												</div>
											</a>
										</li>
									{/each}
								</ul>
							{:else}
								<div class="text-center py-10 px-4 border-2 border-dashed rounded-lg">
									<p class="text-gray-600">Ottimo! Non hai preventivi in sospeso.</p>
									<a href={base+"/preventivatore"} class="mt-3 inline-block px-5 py-2 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition-colors">
										Crea un nuovo preventivo
									</a>
								</div>
							{/if}
						</div>
                    </div>
                </div>

                <!-- Colonna Laterale per il Grafico -->
                <div class="space-y-8">
                    {#if policyStats.length > 0}
                        <PolicyChart data={policyStats} />
                    {:else}
                        <div class="bg-white p-6 rounded-lg shadow text-center text-gray-500">
                            <p>Attiva la tua prima polizza per vedere le statistiche!</p>
                        </div>
                    {/if}
                    <!-- Qui potresti aggiungere altri widget in futuro -->
                </div>
            </div>
        {/if}
    </main>
</div>

<style lang="postcss">
	/* Selezioniamo tutti gli elementi <button> in questo componente */
	button {
		/* Usiamo @apply per "iniettare" le utility class di Tailwind */
		@apply cursor-pointer;
	}
</style>