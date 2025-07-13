<!-- src/lib/components/preventivo/Step1DatiVeicolo.svelte -->

<script lang="ts">
	// Definiamo la "forma" dei dati che questo componente gestisce
	type FormData = {
		car_brand: string;
		car_model: string;
		license_plate: string;
	};

    // Definiamo tutte le props che questo componente riceve
	type Props = {
		formData: FormData;
		carBrands: string[];
	};

	// Unica chiamata a $props()
	let { formData = $bindable(), carBrands }: Props = $props();

</script>

<div class="space-y-6">
	<h2 class="text-xl font-semibold text-gray-800">1. Informazioni sul Veicolo</h2>

	<div>
		<label for="car_brand" class="block text-sm font-medium text-gray-700 mb-1">Marca Veicolo</label>
		<select
			id="car_brand"
			bind:value={formData.car_brand}
			class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
			required
		>
			<option value="" disabled>Seleziona una marca</option>
			{#each carBrands as brand}
				<option value={brand}>{brand}</option>
			{/each}
		</select>
	</div>

	<div>
		<label for="car_model" class="block text-sm font-medium text-gray-700 mb-1">Modello</label>
		<input
			type="text"
			id="car_model"
			bind:value={formData.car_model}
			placeholder="Es. Panda, Golf, Yaris"
			class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
			required
		/>
	</div>

	<div>
		<label for="license_plate" class="block text-sm font-medium text-gray-700 mb-1">Targa</label>
		<input
			type="text"
			id="license_plate"
			bind:value={formData.license_plate}
			placeholder="AA123BB"
			class="w-full uppercase px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
			required
		/>
	</div>
</div>