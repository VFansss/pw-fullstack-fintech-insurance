<!-- src/lib/components/preventivo/Step1DatiVeicolo.svelte -->
<script lang="ts">
	type FormData = {
		car_brand: string;
		car_model: string;
		license_plate: string;
		km_per_year: string;
	};

	type Props = {
		formData: FormData;
		carBrands: string[];
		vehicleType: string;
	};

	let { formData = $bindable(), carBrands, vehicleType }: Props = $props();
	

	function getPlaceholderModello(vehicleType: string): string {
		switch (vehicleType) {
			case 'moto': return 'Es. Monster, Scrambler, Panigale';
			case 'autocarro': return 'Es. Daily, Ducato, Sprinter';
			default: return 'Es. Panda, Golf, Yaris';
		}
	}
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
			placeholder={getPlaceholderModello(vehicleType)}
			class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm"
			required
		/>
	</div>

	<div>
		<label for="license_plate" class="block text-sm font-medium text-gray-700 mb-1">Targa</label>
		<input
			type="text"
			id="license_plate"
			bind:value={formData.license_plate}
			maxlength="7"
			class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm"
			required
		/>
	</div>

	<div>
		<label for="km_per_year" class="block text-sm font-medium text-gray-700 mb-1">Km percorsi all'anno</label>
		<select
			id="km_per_year"
			bind:value={formData.km_per_year}
			class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm"
			required
		>
			<option value="0-5000">Meno di 5.000 km</option>
			<option value="5000-10000">5.000 - 10.000 km</option>
			<option value="10000-15000">10.000 - 15.000 km</option>
			<option value="15000-20000">15.000 - 20.000 km</option>
			<option value="20000+">Più di 20.000 km</option>
		</select>
	</div>
</div>