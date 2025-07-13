<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { Chart, registerables } from 'chart.js';

    // Registriamo tutti gli elementi di Chart.js per assicurarci
    // che il grafico a torta (pie) funzioni correttamente.
    Chart.register(...registerables);

    // Il componente si aspetta un array di dati con questa forma.
    let { data } = $props<{ data: { quote__vehicle_type: string, count: number }[] }>();
    
    let canvas: HTMLCanvasElement;
    let chart: Chart;

    onMount(() => {
        if (!canvas) return;

        // Trasformiamo i dati ricevuti nel formato che Chart.js capisce.
        const labels = data.map(d => {
            // Rendiamo le etichette più leggibili
            const label = d.quote__vehicle_type;
            return label.charAt(0).toUpperCase() + label.slice(1);
        });
        const counts = data.map(d => d.count);
        
        chart = new Chart(canvas, {
            type: 'pie', // Tipo di grafico
            data: {
                labels: labels,
                datasets: [{
                    label: 'Polizze per Tipo',
                    data: counts,
                    backgroundColor: [
                        'rgba(59, 130, 246, 0.8)',  // Blu
                        'rgba(239, 68, 68, 0.8)',   // Rosso
                        'rgba(245, 158, 11, 0.8)',  // Ambra
                    ],
                    borderColor: '#ffffff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        text: 'Le tue polizze attive'
                    }
                }
            }
        });
    });

    // È FONDAMENTALE distruggere il grafico quando il componente viene rimosso
    // per evitare problemi di memoria.
    onDestroy(() => {
        if (chart) {
            chart.destroy();
        }
    });
</script>

<div class="bg-white p-6 rounded-lg shadow h-96">
    <canvas bind:this={canvas}></canvas>
</div>