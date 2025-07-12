<script lang="ts">

    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { auth } from '$lib/api';

    let username = $state('');
    let password = $state('');
    let errorMessage = $state<string | null>(null);

    onMount(async () => {
        // Controlla se abbiamo un token
        const token = localStorage.getItem('authToken');
        if (token) {
            try {
                // Prova a ottenere i dati dell'utente. Questa chiamata fallirà se il token non è valido.
                await auth.getUser();
                // Se la chiamata ha successo, il token è valido! Reindirizziamo l'utente alla sua dashboard.
                goto('/dashboard'); 
            } catch (error) {
                // Il token non è valido. Lo rimuoviamo per sicurezza e lasciamo l'utente sulla pagina di login.
                localStorage.removeItem('authToken');
                console.log('Token non valido, rimosso.');
            }
        }
    });

    async function handleLogin() {
        errorMessage = null;
        try {
            const result = await auth.login({ username, password });
            
            console.log('Login riuscito! Token:', result.key);
            localStorage.setItem('authToken', result.key);
            
            goto('/dashboard');
            
        } catch (error: any) {
            errorMessage = error.message || 'Errore sconosciuto.';
        }
    }
</script>

<div class="min-h-screen bg-gray-100 flex flex-col justify-center items-center">
    <div class="bg-white p-8 rounded-lg shadow-md w-96">
        <h1 class="text-2xl font-bold mb-6 text-center">Accedi ad AlCoperto</h1>

        <form onsubmit={handleLogin}>
            <div class="mb-4">
                <label for="username" class="block text-gray-700 mb-2">Username</label>
                <input
                    type="text"
                    id="username"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                    bind:value={username}
                />
            </div>
            <div class="mb-6">
                <label for="password" class="block text-gray-700 mb-2">Password</label>
                <input
                    type="password"
                    id="password"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                    bind:value={password}
                />
            </div>

            {#if errorMessage}
                <p class="text-red-500 text-sm mb-4">{errorMessage}</p>
            {/if}

            <button
                type="submit"
                class="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition-colors"
            >
                Login
            </button>
        </form>
    </div>
</div>