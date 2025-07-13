<!-- frontend/src/routes/(preventivo)/+page.svelte -->

<script lang="ts">
	import { goto } from '$app/navigation';
	import { base } from '$app/paths';

	const tipiPreventivo = [
		{
			tipo: 'auto',
			titolo: 'Assicurazione Auto',
			descrizione: 'Calcola un preventivo su misura per la tua automobile in pochi minuti.',
			icon: '🚗' // Esempio con emoji, potremmo usare SVG
		},
		{
			tipo: 'moto',
			titolo: 'Assicurazione Moto',
			descrizione: 'Proteggi la tua due ruote con le nostre garanzie complete e flessibili.',
			icon: '🏍️'
		},
		{
            tipo: 'autocarro',
            titolo: 'Assicurazione Autocarro',
            descrizione: 'Soluzioni personalizzate per proteggere il tuo veicolo commerciale.',
            icon: '🚚'
        }
	];
</script>

<div class="container mx-auto max-w-4xl py-16 px-4">
	<div class="text-center">
		<h1 class="text-4xl font-extrabold text-gray-900">Scegli la tua protezione</h1>
		<p class="mt-4 text-lg text-gray-600">
			Seleziona il tipo di assicurazione che ti interessa per iniziare a calcolare il tuo preventivo personalizzato.
		</p>
	</div>

	<div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-8 ">
		{#each tipiPreventivo as item}
			<button
				onclick={() => goto(base+`/preventivatore/${item.tipo}`)}
				class="cursor-pointer group block text-left p-6 bg-white rounded-xl shadow-lg hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 border border-gray-200"
			>
				<div class="text-4xl mb-4">{item.icon}</div>
				<h2 class="text-xl font-bold text-gray-800 group-hover:text-blue-600 transition-colors">
					{item.titolo}
				</h2>
				<p class="mt-2 text-gray-600">{item.descrizione}</p>
				<div class="mt-6 text-blue-600 font-semibold opacity-0 group-hover:opacity-100 transition-opacity">
					Inizia ora →
				</div>
			</button>
		{/each}
	</div>
</div>