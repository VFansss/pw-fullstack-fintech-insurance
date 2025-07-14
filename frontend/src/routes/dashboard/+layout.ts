/** @type {import('./$types').LayoutLoad} */
export async function load({ parent }) {
    // `parent()` esegue la funzione `load` del layout superiore.
    const parentData = await parent(); 

    // Restituiamo i dati del genitore (se servono) e SOVRASCRIVIAMO il titolo.
    return {
        ...parentData, // Opzionale, ma buona pratica se il layout padre ha altri dati utili
        title: 'Area Personale - AlCoperto' // Titolo specifico per questa sezione
    };
}