<!-- src/lib/components/preventivo/Step2DatiAnagrafici.svelte -->

<script lang="ts">
	// Definiamo la forma dei dati di questo step
	type FormData = {
		first_name: string;
		last_name: string;
		birth_date: string; // Formato YYYY-MM-DD
		license_year: number | string;
	};
	
    // Definiamo tutte le props che questo componente riceve
	type Props = {
		formData: FormData;
		user: any | null;
	};

	// Unica chiamata a $props()
	let { formData = $bindable(), user }: Props = $props();

</script>

<div class="space-y-6">
	<h2 class="text-xl font-semibold text-gray-800">2. Dati del Proprietario</h2>

	<div>
		<label for="first_name" class="block text-sm font-medium text-gray-700 mb-1">Nome</label>
		<input
			type="text"
			id="first_name"
			bind:value={formData.first_name}
			class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm disabled:bg-gray-100"
			disabled={!!user}
			required
		/>
	</div>

	<div>
		<label for="last_name" class="block text-sm font-medium text-gray-700 mb-1">Cognome</label>
		<input
			type="text"
			id="last_name"
			bind:value={formData.last_name}
			class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm disabled:bg-gray-100"
			disabled={!!user}
			required
		/>
	</div>

	<div>
		<label for="birth_date" class="block text-sm font-medium text-gray-700 mb-1">Data di Nascita</label>
		<input
			type="date"
			id="birth_date"
			bind:value={formData.birth_date}
			class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm"
			required
		/>
	</div>
	
	<div>
		<label for="license_year" class="block text-sm font-medium text-gray-700 mb-1">Anno Conseguimento Patente</label>
		<input
			type="number"
			id="license_year"
			bind:value={formData.license_year}
			placeholder="Es. 2010"
			min="1950"
			max={new Date().getFullYear()}
			class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm"
			required
		/>
	</div>
</div>