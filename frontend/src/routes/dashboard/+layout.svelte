<script lang="ts">
    import MinimalLayout from '$lib/layouts/MinimalLayout.svelte';
    let { children } = $props();
</script>

<MinimalLayout title="AlCoperto / Area Personale - Dashboard">
    {@render children()}
</MinimalLayout>
