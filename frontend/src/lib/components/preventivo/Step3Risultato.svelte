<!-- src/lib/components/preventivo/Step3Risultato.svelte -->
<script lang="ts">
    // Questo componente riceve solo il prezzo calcolato come prop.
    let { prezzo }: { prezzo: number | null } = $props();
</script>

<div class="text-center">
    <h2 class="text-2xl font-bold text-gray-800">Il Tuo Preventivo Personalizzato è Pronto!</h2>

    {#if prezzo !== null}
        <div class="my-6">
            <p class="text-lg text-gray-600">Premio annuale stimato:</p>
            <p class="text-5xl font-extrabold text-blue-600 tracking-tight mt-2">
                €{prezzo.toFixed(2)}
            </p>
        </div>
        <div class="bg-green-50 border-l-4 border-green-400 p-4 rounded-r-lg">
            <p class="text-green-800">
                Un ottimo prezzo! Salva il tuo preventivo creando un account. Potrai bloccare il prezzo e gestire tutto comodamente dalla tua area personale.
            </p>
        </div>
    {:else}
        <!-- Messaggio mostrato in caso di errore nel calcolo -->
        <div class="my-6">
            <p class="text-xl text-red-600">
                Non è stato possibile calcolare il preventivo.
            </p>
        </div>
    {/if}
</div>