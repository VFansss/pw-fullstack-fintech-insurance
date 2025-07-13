<!-- src/lib/components/preventivo/Step4Contatti.svelte -->
<script lang="ts">
    // Definiamo la forma dei dati di questo step
    type FormData = {
        email: string;
        password?: string;
        password2?: string;
    };

    // Riceviamo `formData` e `user`
    type Props = {
        formData: FormData;
        user: any | null;
    };
    let { formData = $bindable(), user }: Props = $props();
</script>

<div class="space-y-6">
    <h2 class="text-xl font-semibold text-gray-800">4. Salva e Completa</h2>
    <p class="text-gray-600">
        Manca solo un ultimo passo. Inserisci i tuoi contatti per salvare il preventivo e creare la tua area personale su AlCoperto.
    </p>

    <div>
        <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Indirizzo Email</label>
        <input
            type="email"
            id="email"
            bind:value={formData.email}
            placeholder="tuamail@esempio.com"
            class="w-full px-3 py-2 border rounded-lg shadow-sm disabled:bg-gray-100"
            disabled={!!user}
            required
        />
    </div>

    <!-- Mostriamo i campi password SOLO se l'utente NON è loggato -->
    {#if !user}
        <div class="space-y-4">
            <div>
                <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Crea una Password</label>
                <input
                    type="password"
                    id="password"
                    bind:value={formData.password}
                    class="w-full px-3 py-2 border rounded-lg shadow-sm"
                    required
                />
            </div>
            <div>
                <label for="password2" class="block text-sm font-medium text-gray-700 mb-1">Conferma Password</label>
                <input
                    type="password"
                    id="password2"
                    bind:value={formData.password2}
                    class="w-full px-3 py-2 border rounded-lg shadow-sm"
                    required
                />
            </div>
        </div>
    {/if}
</div>