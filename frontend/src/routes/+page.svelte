<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';
	import { fade, fly } from 'svelte/transition';
	import { cubicOut } from 'svelte/easing';
	import Logo from '$lib/assets/logo.svelte';
	import { base } from '$app/paths';

	// === STATO PER LA NAVBAR ===
	let isMenuOpen = $state(false);
	let isMobileMenuOpen = $state(false);

	// === STATO PER L'HERO A ROTAZIONE ===
	const backgroundImages = [
		'/hero-bg-1.jpg', // L'immagine delle chiavi
		'/hero-bg-2.jpg', // L'immagine della famiglia
		'/hero-bg-3.jpg'  // L'immagine dell'auto
	];
	let currentBgIndex = $state(0);
	let intervalId: ReturnType<typeof setInterval>;
	let isTransitioning = $state(false);

	onMount(() => {
		// Avvia la rotazione delle immagini di sfondo
		intervalId = setInterval(() => {
			isTransitioning = true;
			setTimeout(() => {
				currentBgIndex = (currentBgIndex + 1) % backgroundImages.length;
				isTransitioning = false;
			}, 300); // Breve delay per la transizione
		}, 7000); // Cambia immagine ogni 7 secondi

        // Cleanup: ferma l'intervallo quando il componente viene distrutto
		return () => clearInterval(intervalId);
	});

	// === DATI PER LE CARD ===
	const features = [
		{ title: 'Assicurazione Auto', description: 'Acquista o rinnova la polizza per viaggiare in sicurezza.', link: '/preventivatore/auto', icon: '🚗' },
		{ title: 'Assicurazione Moto', description: 'Scegli una polizza personalizzabile e sospendila gratis quando vuoi.', link: '/preventivatore/moto', icon: '🏍️' },
		{ title: 'Assicurazione Autocarro', description: 'Soluzioni complete per proteggere il tuo veicolo commerciale.', link: '/preventivatore/autocarro', icon: '🚚' },
	];
</script>

<div class="min-h-screen bg-white flex flex-col">
	<!-- ================== NAVBAR CON DROPDOWN ================== -->
	<nav class="bg-white/80 backdrop-blur-md shadow-sm sticky top-0 z-50">
		<div class="container mx-auto px-6 py-3 flex justify-between items-center">
			<a href={base+"/"} class="flex items-center space-x-2" title="Home AlCoperto">
				<Logo class="h-8 w-8 text-blue-600" />
				<span class="text-2xl font-bold text-gray-800">AlCoperto</span>
			</a>
			
			<!-- Desktop Menu -->
			<div class="hidden md:flex items-center space-x-6">
				<div class="relative">
					<button onclick={() => isMenuOpen = !isMenuOpen} class="flex items-center text-gray-700 hover:text-blue-600">
						Assicurazioni
						<svg class="h-5 w-5 ml-1 transition-transform {isMenuOpen ? 'rotate-180' : ''}" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
					</button>
					{#if isMenuOpen}
						<div class="absolute mt-2 w-48 bg-white rounded-md shadow-xl py-1 z-20">
							<a href={base+"/preventivatore/auto"} class="block px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600">Assicurazione Auto</a>
							<a href={base+"/preventivatore/moto"} class="block px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600">Assicurazione Moto</a>
							<a href={base+"/preventivatore/autocarro"} class="block px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600">Assicurazione Autocarro</a>
						</div>
					{/if}
				</div>
				<a href={base+"/login"} class="px-4 py-2 text-gray-800 font-semibold rounded-lg hover:bg-gray-100">Area Personale</a>
				<button onclick={() => goto(base+'/preventivatore/auto')} class="px-5 py-2 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 transition-colors">Fai un preventivo</button>
			</div>
			
			<!-- Mobile Menu Button -->
			<button 
				onclick={() => isMobileMenuOpen = !isMobileMenuOpen}
				class="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
				aria-label="Toggle mobile menu"
			>
				<svg class="h-6 w-6 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					{#if isMobileMenuOpen}
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
					{:else}
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
					{/if}
				</svg>
			</button>
		</div>
		
		<!-- Mobile Menu -->
		{#if isMobileMenuOpen}
			<div class="md:hidden bg-white border-t border-gray-200 py-4">
				<div class="container mx-auto px-6 space-y-3">
					<!-- Mobile Insurance Submenu -->
					<div class="space-y-2">
						<div class="text-sm font-semibold text-gray-500 uppercase tracking-wide">Assicurazioni</div>
						<a href={base+"/preventivatore/auto"} onclick={() => isMobileMenuOpen = false} class="block px-3 py-2 text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-lg">🚗 Assicurazione Auto</a>
						<a href={base+"/preventivatore/moto"} onclick={() => isMobileMenuOpen = false} class="block px-3 py-2 text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-lg">🏍️ Assicurazione Moto</a>
						<a href={base+"/preventivatore/autocarro"} onclick={() => isMobileMenuOpen = false} class="block px-3 py-2 text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-lg">🚚 Assicurazione Autocarro</a>
					</div>
					
					<!-- Divider -->
					<div class="border-t border-gray-200 my-4"></div>
					
					<!-- Other Menu Items -->
					<a href={base+"/login"} onclick={() => isMobileMenuOpen = false} class="block px-3 py-2 text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-lg">Area Personale</a>
					
					<!-- CTA Button -->
					<button 
						onclick={() => { goto(base+'/preventivatore/auto'); isMobileMenuOpen = false; }}
						class="w-full mt-4 px-5 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 transition-colors"
					>
						Fai un preventivo
					</button>
				</div>
			</div>
		{/if}
	</nav>

	<!-- ================== HERO SECTION A ROTAZIONE ================== -->
	<header class="flex-grow flex items-center justify-center relative overflow-hidden text-white">
		<!-- Background Images with Animations -->
		{#each backgroundImages as bgImage, index (index)}
			{#if index === currentBgIndex}
				<div 
					class="absolute inset-0 bg-cover bg-center"
					style="background-image: url({bgImage})"
					in:fade={{ duration: 800, easing: cubicOut }}
					out:fade={{ duration: 600, easing: cubicOut }}
				></div>
			{/if}
		{/each}
		
		<!-- Dark Overlay -->
		<div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/70 to-transparent"></div>
		
		<!-- Static Content -->
		<div class="container mx-auto px-6 py-24 text-center relative z-10">
			<h1 class="text-4xl md:text-6xl font-black leading-tight tracking-tight text-shadow-lg">
				L'assicurazione online completa e innovativa
			</h1>
			<p class="mt-4 text-lg md:text-xl max-w-3xl mx-auto text-shadow">
				Crea una polizza su misura e facile da gestire, con tutte le garanzie adatte alle tue esigenze.
			</p>
			<div class="mt-10">
				<button 
					onclick={() => goto(base+'/preventivatore/auto')} 
					class="px-10 py-4 bg-blue-600 text-white font-bold rounded-full text-xl hover:bg-blue-700 transition-transform transform hover:scale-105 shadow-2xl"
				>
					Calcola Preventivo
				</button>
			</div>
		</div>
		
		<!-- Background Navigation Dots -->
		<div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex space-x-2 z-10">
			{#each backgroundImages as _, index}
				<button
					onclick={() => {
						if (index !== currentBgIndex) {
							currentBgIndex = index;
							// Reset interval
							clearInterval(intervalId);
							intervalId = setInterval(() => {
								isTransitioning = true;
								setTimeout(() => {
									currentBgIndex = (currentBgIndex + 1) % backgroundImages.length;
									isTransitioning = false;
								}, 300);
							}, 7000);
						}
					}}
					class="w-3 h-3 rounded-full transition-all duration-300 {index === currentBgIndex ? 'bg-white scale-125' : 'bg-white/50 hover:bg-white/70'}"
					aria-label="Vai all'immagine {index + 1}"
				></button>
			{/each}
		</div>
	</header>
</div>

<!-- ================== SEZIONE FEATURE CARDS ================== -->
<section class="bg-gray-50 py-20">
	<div class="container mx-auto px-6">
		<div class="text-center mb-12">
			<h2 class="text-4xl font-bold text-gray-800">Proteggersi è semplice</h2>
			<p class="text-gray-600 mt-2">Scegli la copertura che ti serve e scopri tutte le opzioni.</p>
		</div>
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 justify-center">
			{#each features as feature}
				<a href={feature.link} class="block bg-white p-8 rounded-2xl shadow-md hover:shadow-2xl hover:-translate-y-2 transition-all duration-300 text-center">
					<span class="text-4xl block mb-4">{feature.icon}</span>
					<h3 class="text-xl font-bold mb-2">{feature.title}</h3>
					<p class="text-gray-600 mb-4">{feature.description}</p>
                    <span class="inline-block font-semibold text-blue-600">Scopri di più →</span>
				</a>
			{/each}
		</div>
	</div>
</section>

<section class="py-20">
	<div class="container mx-auto px-6 grid md:grid-cols-2 gap-12 items-center">
		<div>
			<img src={base+"/app-screen.jpg"} alt="Schermata dell'app AlCoperto" class="rounded-xl shadow-2xl">
		</div>
		<div>
			<h2 class="text-4xl font-bold text-gray-800">Risparmia fino a €200 sul rinnovo di polizza</h2>
			<p class="text-lg text-gray-600 mt-4">Approfitta dei vantaggi: assicura veicoli o porta altre persone in AlCoperto e ottieni uno sconto sul rinnovo della polizza (forse)</p>
			<a href="#" class="inline-block mt-6 text-blue-600 font-bold hover:underline">Comincia a risparmiare →</a>
		</div>
	</div>
</section>

<!-- ================== FOOTER ================== -->
<footer class="bg-gray-800 text-gray-300">
	<div class="container mx-auto px-6 py-8 text-center">
		<p>© 2025 AlCoperto. Tutti i diritti riservati.</p>
        <p class="text-xs text-gray-500 mt-2">Progetto a scopo didattico per tesi di laurea. Le immagini sono tratte da Unsplash.</p>
	</div>
</footer>

<style lang="postcss">
	.text-shadow {
		text-shadow: 0 2px 4px rgba(0,0,0,0.5);
	}
	.text-shadow-lg {
		text-shadow: 0 4px 8px rgba(0,0,0,0.4);
	}

	/* Selezioniamo tutti gli elementi <button> in questo componente */
	button {
		/* Usiamo @apply per "iniettare" le utility class di Tailwind */
		@apply cursor-pointer;
	}
</style>