<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { auth } from '$lib/api';
    import Logo from '$lib/assets/logo.svelte'; // Importiamo il nostro componente Logo

	let username = $state('');
	let password = $state('');
	let errorMessage = $state<string | null>(null);

	onMount(async () => {
		// ... la tua logica onMount rimane identica ...
        const token = localStorage.getItem('authToken');
        if (token) {
            try {
                await auth.getUser();
                goto('/dashboard', { replaceState: true }); 
            } catch (error) {
                localStorage.removeItem('authToken');
                console.log('Token non valido, rimosso.');
            }
        }
	});

	async function handleLogin(event: SubmitEvent) { // Aggiungiamo il tipo all'evento
		event.preventDefault(); // E preveniamo il default
		errorMessage = null;
		try {
			const result = await auth.login({ username, password });
			localStorage.setItem('authToken', result.key);
			goto('/dashboard', { replaceState: true });
		} catch (error: any) {
			errorMessage = error.message || 'Credenziali non valide.';
		}
	}
</script>

<div class="min-h-screen bg-gray-100 flex flex-col justify-center items-center p-4">
	<div class="w-full max-w-sm">
        

		<div class="bg-white p-8 rounded-xl shadow-md">
            <!-- ===== BLOCCO LOGO AGGIUNTO ===== -->
            <div class="flex justify-center mb-6">
                <button onclick={() => goto('/')} class=" cursor-pointer transition-transform transform hover:scale-110">
                    <Logo class="h-16 w-16 text-blue-600" />
                </button>
            </div>
            <!-- ================================ -->
			<h1 class="text-2xl font-bold mb-6 text-center text-gray-800">Accedi ad AlCoperto</h1>

			<form onsubmit={handleLogin}>
				<div class="mb-4">
					<label for="username" class="block text-gray-700 mb-2">Username</label>
					<input
						type="text"
						id="username"
						class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
						bind:value={username}
					/>
				</div>
				<div class="mb-6">
					<label for="password" class="block text-gray-700 mb-2">Password</label>
					<input
						type="password"
						id="password"
						class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
						bind:value={password}
					/>
				</div>

				{#if errorMessage}
					<p class="text-red-500 text-sm mb-4 text-center">{errorMessage}</p>
				{/if}

				<button
					type="submit"
					class="cursor-pointer w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors font-semibold"
				>
					Login
				</button>
			</form>

			<!-- Separator and redirect for non-registered users -->
			<div class="mt-6 pt-6 border-t border-gray-200">
				<p class="text-green-800 text-center mb-4">
					Non sei ancora assicurato da noi? Crea prima un preventivo, per accedere alla tua area personale
				</p>
				<button
					onclick={() => goto('/preventivatore')}
					class="cursor-pointer w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition-colors font-semibold"
				>
					Crea un Preventivo
				</button>
			</div>
		</div>
	</div>
</div>