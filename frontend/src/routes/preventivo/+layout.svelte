<script lang="ts">
    import Logo from '$lib/assets/logo.svelte';
    import { goto } from '$app/navigation';
    let { children } = $props();
</script>

<div class="min-h-screen bg-gray-100 flex flex-col">
    <!-- Header Minimale -->
    <header class="bg-white border-b">
        <div onclick={() => goto('/')} class="container mx-auto px-6 py-4 flex items-center">
            <Logo class="h-8 w-8 text-blue-600" />
            <span class="ml-2 text-xl font-semibold text-gray-700">AlCoperto / Preventivo</span>
        </div>
    </header>

    <!-- Contenuto della pagina (il nostro form) -->
    <main class="flex-grow">
        {@render children()}
    </main>

    <!-- Footer Minimale -->
    <footer class="bg-gray-200 text-center py-4">
        <p class="text-sm text-gray-600">© 2025 AlCoperto - Tutti i diritti riservati.</p>
    </footer>
</div>