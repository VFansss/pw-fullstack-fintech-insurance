<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { auth } from '$lib/api';

    let username = $state('...'); // Placeholder
    let error = $state<string | null>(null);

    // === ROUTE GUARD: Proteggiamo la pagina ===
    onMount(async () => {
        const token = localStorage.getItem('authToken');
        if (!token) {
            // Se non c'è il token, non c'è motivo di stare qui. Vai al login.
            goto('/login');
            return;
        }

        try {
            // Proviamo a caricare i dati dell'utente per mostrarli.
            // Questa è anche la nostra validazione del token.
            const user = await auth.getUser();
            username = user.username;
        } catch (e) {
            // Il token non è valido/scaduto. Rimuovilo e torna al login.
            localStorage.removeItem('authToken');
            error = 'La tua sessione è scaduta. Effettua nuovamente il login.';
            // Diamo un secondo per leggere l'errore prima di reindirizzare
            setTimeout(() => goto('/login'), 2000);
        }
    });
    
    // === Logica per il LOGOUT ===
    async function handleLogout() {
        try {
            await auth.logout();
        } catch (error) {
            console.error("Errore durante il logout sul server:", error);
            // Andiamo avanti comunque, l'importante è pulire il frontend.
        } finally {
            // A prescindere dal risultato del server, puliamo il token dal browser
            // e reindirizziamo al login.
            localStorage.removeItem('authToken');
            goto('/login');
        }
    }
</script>

<div class="min-h-screen bg-gray-50 p-8">
    <div class="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow">
        {#if error}
            <p class="text-red-500">{error}</p>
        {:else}
            <h1 class="text-3xl font-bold text-gray-800">
                Benvenuto nella tua Area Riservata, <span class="text-blue-600">{username}</span>!
            </h1>
            <p class="text-gray-600 mt-2">
                Questa è la tua dashboard di AlCoperto.
            </p>

            <div class="mt-8">
                <!-- Qui andranno le tue polizze, preventivi, etc. -->
                <p class="text-center text-gray-500">(Contenuto della dashboard in arrivo...)</p>
            </div>
            
            <div class="mt-8 border-t pt-6">
                <button
                    onclick={handleLogout}
                    class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
                >
                    Logout
                </button>
            </div>
        {/if}
    </div>
</div>