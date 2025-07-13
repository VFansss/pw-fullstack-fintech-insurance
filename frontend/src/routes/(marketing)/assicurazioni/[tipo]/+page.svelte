<!-- frontend/src/routes/preventivatore/[tipo]/+page.svelte -->
<script lang="ts">

    import { page } from '$app/state';

    // For sveltekit
    /** @type {import('./$types').EntryGenerator} */
    export function entries() {
        return [
            { tipo: 'auto' },
            { tipo: 'moto' },
        ];
    }

    // Diciamo a SvelteKit che queste pagine possono essere pre-renderizzate
    export const prerender = true;

    // Il parametro 'tipo' è disponibile tramite l'oggetto page
    const tipoAssicurazione = $derived(page.params.tipo);

    // Ora possiamo usare questa variabile per cambiare il contenuto della pagina
    const titolo = $derived(`Preventivo per Assicurazione ${tipoAssicurazione.charAt(0).toUpperCase() + tipoAssicurazione.slice(1)}`);

</script>

<div class="container mx-auto p-8">
    <h1 class="text-4xl font-bold">{titolo}</h1>

    {#if tipoAssicurazione === 'auto'}
        <p>Mostra i campi specifici per l'auto...</p>
        <!-- Form per l'auto qui -->
    {:else if tipoAssicurazione === 'moto'}
        <p>Mostra i campi specifici per la moto...</p>
        <!-- Form per la moto qui -->
    {:else}
        <p>Form generico per il tipo: {tipoAssicurazione}</p>
    {/if}
</div>