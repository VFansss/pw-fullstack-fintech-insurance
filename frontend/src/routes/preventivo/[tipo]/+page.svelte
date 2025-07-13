<script lang="ts">
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { auth, quotes } from '$lib/api';

	// Importa i componenti degli step (come prima)
	import Step1 from '$lib/components/preventivo/Step1DatiVeicolo.svelte';
	import Step2 from '$lib/components/preventivo/Step2DatiAnagrafici.svelte';
	import Step3 from '$lib/components/preventivo/Step3Contatti.svelte';
	
	let { data } = $props();

	// Stato del form (come prima)
	let currentStep = $state(1);
	let isLoading = $state(false);
	let errorMessage = $state<string | null>(null);

	// Questo è il nostro stato. Contiene TUTTI i dati che il form può raccogliere.
	let formData = $state({
		car_brand: '',
		car_model: '',
		license_plate: '',
		first_name: '',
		last_name: '',
		birth_date: '',
		license_year: '',
		email: '',
		password: '',
		password2: '',
	});
	
	// --- Pre-compilazione REATTIVA con $effect ---
	// Questo effetto si attiverà automaticamente ogni volta che `data.streamed.userData` cambia.
	// Poiché cambia solo una volta (da promessa a risultato), verrà eseguito una sola volta.
	$effect(() => {
		// Dobbiamo usare una funzione asincrona interna perché $effect non può essere
		// direttamente async, ma può contenere codice asincrono.
		const prefillData = async () => {
			const result = await data.streamed.userData;
			if (result && result.success) {
				formData.first_name = result.user.first_name || '';
				formData.last_name = result.user.last_name || '';
				formData.email = result.user.email || '';
			}
		};
		
		prefillData();
	});

	// --- FUNZIONE HANDLESUBMIT CORRETTA ---
	// Riceve l'evento, non i dati. Non ha bisogno di essere tipizzata qui
	// perché `onsubmit` lo fa già.
	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault(); // Preveniamo il ricaricamento della pagina

		isLoading = true;
		errorMessage = null;

		try {
			const userDataResult = await data.streamed.userData;
			
			// Se l'utente non è loggato, prima lo registriamo
			if (!userDataResult.success) {
				// Il controllo delle password ora legge direttamente dal nostro stato
				if (formData.password !== formData.password2) {
					throw new Error('Le password non coincidono.');
				}
				
				const registrationResult = await auth.register({
					username: formData.email,
					email: formData.email,
					password: formData.password,
					password2: formData.password2,
				});
				localStorage.setItem('authToken', registrationResult.key);
			}

			// Ora creiamo il preventivo. Prendiamo solo i dati che servono
			// dal nostro grande oggetto formData e li passiamo alla funzione.
			await quotes.create({
				car_brand: formData.car_brand,
				car_model: formData.car_model,
				license_plate: formData.license_plate,
				birth_date: formData.birth_date,
				license_year: parseInt(formData.license_year) || 0,
				first_name: formData.first_name,
				last_name: formData.last_name,
				email: formData.email,
			});
			
			goto('/dashboard');
		} catch (error: any) {
			errorMessage = error.message;
		} finally {
			isLoading = false;
		}
	}
</script>

<div class="container mx-auto max-w-2xl py-12 px-4">
	<!-- Titolo e stato del progresso -->
	<div class="text-center mb-8">
		<h1 class="text-3xl font-bold text-gray-800">
			Calcola il tuo preventivo per l'assicurazione <span class="text-blue-600">{page.params.tipo}</span>
		</h1>
		<div class="mt-4 w-full bg-gray-200 rounded-full h-2.5">
			<div
				class="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
				style="width: {(currentStep / 3) * 100}%"
			/>
		</div>
	</div>

	<!-- Await Block per gestire il caricamento iniziale dei dati (utente e marche) -->
	{#await Promise.all([data.streamed.userData, data.streamed.carBrands])}
		<!-- STATO DI CARICAMENTO INIZIALE (SPINNER) -->
		<div class="flex flex-col items-center justify-center bg-white p-8 rounded-xl shadow-lg min-h-[300px]">
			<svg class="animate-spin h-10 w-10 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
				<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
				<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
			</svg>
			<p class="mt-4 text-gray-600">Stiamo preparando il tuo preventivo...</p>
		</div>
	{:then [userDataResult, carBrands]}
		<div class="bg-white p-8 rounded-xl shadow-lg">
            <form onsubmit={handleSubmit}>
                <!-- Renderizziamo lo step giusto, passando il formData -->
                {#if currentStep === 1}
                    <Step1 bind:formData {carBrands}/>
                {:else if currentStep === 2}
                    <Step2 bind:formData user={userDataResult.user}/>
                {:else if currentStep === 3}
                    <Step3 bind:formData user={userDataResult.user} />
                {/if}

                <!-- I PULSANTI DI NAVIGAZIONE SONO QUI, NEL PADRE! -->
                <div class="mt-8 flex justify-between items-center">
                    {#if currentStep > 1}
                        <button type="button" onclick={() => currentStep--} class="...">
                            ← Indietro
                        </button>
                    {:else}
                        <span></span>
                    {/if}

                    {#if currentStep < 3}
                        <button type="button" onclick={() => currentStep++} class="...">
                            Procedi →
                        </button>
                    {:else}
                        <button type="submit" class="..." disabled={isLoading}>
                            {#if isLoading}Caricamento...{:else}Ottieni Preventivo{/if}
                        </button>
                    {/if}
                </div>

                {#if errorMessage}
                    <p class="text-red-500 ...">{errorMessage}</p>
                {/if}
            </form>
        </div>
	{:catch error}
		<!-- STATO DI ERRORE CRITICO -->
		<div class="bg-white p-8 rounded-xl shadow-lg text-center">
			<h2 class="text-xl font-bold text-red-600">Oops! Qualcosa è andato storto.</h2>
			<p class="text-gray-600 mt-2">{error.message}</p>
			<button onclick={() => window.location.reload()} class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
				Ricarica la pagina
			</button>
		</div>
	{/await}
</div>