<script lang="ts">
    import MinimalLayout from '$lib/layouts/MinimalLayout.svelte';
    let { children } = $props();
</script>

<MinimalLayout title="AlCoperto / Preventivo">
    {@render children()}
</MinimalLayout>
