<script lang="ts">

	import '../app.css';
	import { page } from '$app/state';

	let { children } = $props();

	export const prerender = true;

	const defaultTitle = 'AlCoperto Assicurazioni';

</script>

<svelte:head>
    <!-- Il titolo sarà quello fornito dai dati della pagina,
         o il titolo di default se non presente. -->
    <title>{page.data.title || defaultTitle}</title>
    
    <!-- Puoi aggiungere qui anche altri meta tag globali -->
    <meta name="description" content="AlCoperto - La tua assicurazione digitale, semplice e veloce." />
</svelte:head>

{@render children()}


