<script lang="ts">
	import { goto } from '$app/navigation';
	import Logo from '$lib/assets/logo.svelte'; // Creeremo questo componente tra un attimo
</script>

<div class="min-h-screen bg-gray-50 flex flex-col">
	<!-- Navbar Semplice -->
	<nav class="bg-white shadow-sm">
		<div class="container mx-auto px-6 py-3 flex justify-between items-center">
			<div class="flex items-center space-x-2">
				<Logo class="h-8 w-8 text-blue-600" />
				<span class="text-2xl font-bold text-gray-800">AlCoperto</span>
			</div>
			<div>
				<button
					onclick={() => goto('/dashboard')}
					class="cursor-pointer px-4 py-2 text-gray-800 font-semibold rounded-lg hover:bg-gray-100"
				>
					Area Personale
				</button>
				<button
					onclick={() => goto('/preventivatore')}
					class="cursor-pointer ml-2 px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 transition-colors"
				>
					Fai un preventivo
				</button>
			</div>
		</div>
	</nav>

	<!-- Hero Section -->
	<main class="flex-grow flex items-center">
		<div class="container mx-auto px-6 py-16 text-center">
			<h1 class="text-5xl md:text-6xl font-extrabold text-gray-900 leading-tight">
				La tua protezione, semplice e digitale.
			</h1>
			<p class="mt-4 text-lg text-gray-600 max-w-2xl mx-auto">
				Benvenuto in AlCoperto, la soluzione assicurativa pensata per te. Lorem ipsum dolor sit
				amet, consectetur adipiscing elit. Phasellus imperdiet, nulla et dictum interdum.
			</p>
			<div class="mt-8 flex justify-center space-x-4">
				<button
					onclick={() => goto('/preventivatore')}
					class="px-8 py-3 bg-red-600 text-white font-bold rounded-full text-lg hover:bg-red-700 transition-transform transform hover:scale-105"
				>
					Assicurati con noi!
				</button>
				<button
					onclick={() => goto('/login')}
					class="px-8 py-3 bg-gray-200 text-gray-800 font-bold rounded-full text-lg hover:bg-gray-300"
				>
					Accedi
				</button>
			</div>
		</div>
	</main>

	<!-- Footer Semplice -->
	<footer class="bg-gray-800 text-white">
		<div class="container mx-auto px-6 py-4 text-center">
			<p>© 2025 AlCoperto. Tutti i diritti riservati. Progetto per tesi di laurea.</p>
		</div>
	</footer>
</div>

<style lang="postcss">
	/* Selezioniamo tutti gli elementi <button> in questo componente */
	button {
		/* Usiamo @apply per "iniettare" le utility class di Tailwind */
		@apply cursor-pointer;
	}
</style>