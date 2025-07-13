<script lang="ts">
    import Logo from '$lib/assets/logo.svelte';
    import { goto } from '$app/navigation';
    import type { Snippet } from 'svelte';
    import { base } from '$app/paths';

    // Questo componente accetta "children" come una prop di tipo Snippet
    let { children, title = 'AlCoperto' }: { children: Snippet; title?: string } = $props();
</script>

<div class="min-h-screen bg-gray-100 flex flex-col">
    <!-- Header Minimale -->
    <header class="bg-white border-b">
        <div
            onclick={() => goto(base+'/')}
            class="container mx-auto px-6 py-4 flex items-center cursor-pointer hover:bg-gray-50 transition-colors duration-200"
        >
            <Logo class="h-8 w-8 text-blue-600" />
            <span class="ml-2 text-xl font-semibold text-gray-700">{title}</span>
        </div>
    </header>

    <!-- Contenuto della pagina (lo spazio vuoto) -->
    <main class="flex-grow">
        {@render children()}
    </main>

    <!-- Footer Minimale -->
    <footer class="bg-gray-200 text-center py-4">
        <p class="text-sm text-gray-600">© 2025 AlCoperto - Tutti i diritti riservati.</p>
    </footer>
</div>