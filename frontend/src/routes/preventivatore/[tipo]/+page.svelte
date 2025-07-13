<!-- /routes/(preventivo)/[tipo]/+page.svelte -->

<script lang="ts">
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { auth, quotes } from '$lib/api';

	import Step1DatiVeicolo from '$lib/components/preventivatore/Step1DatiVeicolo.svelte';
	import Step2DatiAnagrafici from '$lib/components/preventivatore/Step2DatiAnagrafici.svelte';
	import Step3Risultato from '$lib/components/preventivatore/Step3Risultato.svelte';
	import Step4Contatti from '$lib/components/preventivatore/Step4Contatti.svelte';

	let { data } = $props();

	// --- STATO DEL COMPONENTE ---
	let currentStep = $state(1);
	let isLoading = $state(false);
	let errorMessage = $state<string | null>(null);
	let calculatedPrice = $state<number | null>(null);

	let formData = $state({
		car_brand: '',
		car_model: '',
		license_plate: '',
		km_per_year: '10000-15000',
		first_name: '',
		last_name: '',
		birth_date: '',
		license_year: '',
		driving_style: 'esperta',
		email: '',
		password: '',
		password2: ''
	});

	// --- LOGICA DI VALIDAZIONE REATTIVA ---
	let isStep1Valid = $derived(
		formData.car_brand && formData.car_model.trim()
	);
	
	let isStep2Valid = $derived(
		formData.first_name.trim() !== '' && 
		formData.last_name.trim() !== '' && 
		formData.birth_date !== '' && 
		formData.license_year !== '' && 
		parseInt(formData.license_year) > 1000
	);

	let isStep4Valid = $derived(
		formData.email.includes('@') 
	);

	// Effetto per pre-compilare i dati utente
	$effect(() => {
		const prefill = async () => {
			const result = await data.streamed.userData;
			if (result?.success && result.user) {
				formData.first_name = result.user.first_name || '';
				formData.last_name = result.user.last_name || '';
				formData.email = result.user.email || '';
			}
		};
		prefill();
	});

	// --- GESTORI DI EVENTI ---
	async function handleSimulate() {
		isLoading = true;
		errorMessage = null;
		try {
			const result = await quotes.simulate({
				car_brand: formData.car_brand,
				car_model: formData.car_model,
				license_plate: formData.license_plate,
				km_per_year: formData.km_per_year,
				driving_style: formData.driving_style,
				birth_date: formData.birth_date,
				license_year: parseInt(formData.license_year) || 0,
			});
			calculatedPrice = result.premium_price;
			currentStep = 3;
		} catch (error: any) {
			errorMessage = error.message;
		} finally {
			isLoading = false;
		}
	}

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		isLoading = true;
		errorMessage = null;

		try {
			const userDataResult = await data.streamed.userData;
			
			if (!userDataResult.success) {
				// --- CASO UTENTE NON LOGGATO ---
				if (formData.password !== formData.password2) {
					throw new Error('Le password non coincidono.');
				}
				// Prima registriamo
				await auth.register({
					username: formData.email,
					email: formData.email,
					password: formData.password,
					password2: formData.password2,
					first_name: formData.first_name,
					last_name: formData.last_name,
				});
                // Subito dopo il successo, facciamo il login per ottenere il token
                const loginResult = await auth.login({ username: formData.email, password: formData.password });
				localStorage.setItem('authToken', loginResult.key);
			}

			// --- CASO PER TUTTI (LOGGATI O APPENA REGISTRATI) ---
            // Ora che siamo sicuramente autenticati, salviamo il preventivo.
            // Costruiamo l'oggetto `quoteData` prendendo TUTTO da `formData`.
			await quotes.create({
				car_brand: formData.car_brand,
				car_model: formData.car_model,
				license_plate: formData.license_plate,
				km_per_year: formData.km_per_year,
				driving_style: formData.driving_style,
				birth_date: formData.birth_date,
				license_year: parseInt(formData.license_year) || 0,
				first_name: formData.first_name,
				last_name: formData.last_name,
				email: formData.email,
			});
			
			goto('/dashboard');

		} catch (error: any) {
			// Questa parte ora può catturare errori sia dalla registrazione che dalla creazione
			errorMessage = error.message;
		} finally {
			isLoading = false;
		}
	}
</script>

<div class="container mx-auto max-w-2xl py-12 px-4">
	<div class="text-center mb-8">
		<h1 class="text-3xl font-bold text-gray-800">
			Calcola il tuo preventivo per l'assicurazione <span class="text-blue-600">{page.params.tipo}</span>
		</h1>
		<div class="mt-4 w-full bg-gray-200 rounded-full h-2.5">
			<div
				class="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
				style="width: {(currentStep / 4) * 100}%"
			/>
		</div>
	</div>

	{#await Promise.all([data.streamed.userData, data.streamed.carBrands])}
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
				{#if currentStep === 1}
					<Step1DatiVeicolo bind:formData {carBrands} vehicleType={page.params.tipo} />
				{:else if currentStep === 2}
					<Step2DatiAnagrafici bind:formData user={userDataResult.user} />
				{:else if currentStep === 3}
					<Step3Risultato prezzo={calculatedPrice} isUserLoggedIn={!!userDataResult.user} />
				{:else if currentStep === 4}
					<Step4Contatti bind:formData user={userDataResult.user} />
				{/if}

				<div class="mt-8 flex justify-between items-center">
					{#if currentStep > 1 && currentStep !== 3}
						<button type="button" onclick={() => {currentStep--; errorMessage = null}} class="px-4 py-2 text-gray-700 font-semibold rounded-lg hover:bg-gray-200">
							← Indietro
						</button>
					{:else}
						<span></span>
					{/if}

					{#if currentStep === 1}
						<button type="button" onclick={() => currentStep++} disabled={!isStep1Valid} class="px-6 py-2 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed">
							Procedi →
						</button>
					{:else if currentStep === 2}
						<button type="button" onclick={handleSimulate} disabled={!isStep2Valid || isLoading} class="px-6 py-2 bg-green-600 text-white rounded-lg shadow-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed">
							{#if isLoading}Calcolo...{:else}Calcola Preventivo{/if}
						</button>
					{:else if currentStep === 3}
						<button type="button" onclick={() => currentStep++} class="w-full px-6 py-3 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700">
							{#if userDataResult.user}Salva Preventivo{:else}Salva e Registrati{/if} →
						</button>
					{:else if currentStep === 4}
						<button type="submit" disabled={(!userDataResult.user && !isStep4Valid) || isLoading} class="px-6 py-2 bg-green-600 text-white rounded-lg shadow-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed">
							{#if isLoading}Salvataggio...{:else}Conferma e Salva{/if}
						</button>
					{/if}
				</div>

				{#if errorMessage}
					<p class="text-red-500 text-center mt-4 font-semibold">{errorMessage}</p>
				{/if}
			</form>
		</div>
	{:catch error}
        <!-- Gestione Errore Critico -->
	{/await}
</div>

<style lang="postcss">
	/* Selezioniamo tutti gli elementi <button> in questo componente */
	button {
		/* Usiamo @apply per "iniettare" le utility class di Tailwind */
		@apply cursor-pointer;
	}
</style>