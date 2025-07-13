<!-- src/lib/components/preventivo/Step3Contatti.svelte -->

<script lang="ts">
	// Definiamo la forma dei dati di questo step
	type FormData = {
		email: string;
		password?: string; // La password è opzionale
		password2?: string;
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
	<h2 class="text-xl font-semibold text-gray-800">3. Contatti e Account</h2>

	<div>
		<label for="email" class="block text-sm font-medium text-gray-700 mb-1">Indirizzo Email</label>
		<input
			type="email"
			id="email"
			bind:value={formData.email}
			placeholder="tuamail@esempio.com"
			class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm disabled:bg-gray-100"
			disabled={!!user}
			required
		/>
		{#if user}
			<p class="text-sm text-gray-500 mt-1">
				Il preventivo verrà associato al tuo account esistente.
			</p>
		{/if}
	</div>

	<!-- Mostriamo i campi password SOLO se l'utente NON è loggato -->
	{#if !user}
		<div class="border-t pt-6 space-y-4">
			<p class="text-sm text-gray-600">
				Crea una password per salvare il tuo preventivo e accedere alla tua area personale.
				L'email diventerà il tuo username.
			</p>
			<div>
				<label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
				<input
					type="password"
					id="password"
					bind:value={formData.password}
					class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm"
					required
				/>
			</div>
			<div>
				<label for="password2" class="block text-sm font-medium text-gray-700 mb-1">Conferma Password</label>
				<input
					type="password"
					id="password2"
					bind:value={formData.password2}
					class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm"
					required
				/>
			</div>
		</div>
	{/if}
</div>