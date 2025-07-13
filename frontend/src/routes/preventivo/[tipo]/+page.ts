// frontend/src/routes/(preventivo)/[tipo]/+page.ts

import { auth, general } from '$lib/api';
import type { PageLoad } from './$types';

export const load: PageLoad = async () => {

    // Funzione per caricare le marche. Già sicura con .catch().
    const fetchBrands = () => general.getCarBrands().catch(() => {
        console.error("Fallimento nel caricamento delle marche di auto.");
        return []; // Restituisce sempre un valore valido (array vuoto).
    });

    // Funzione per caricare l'utente, ORA A PROVA DI BOMBA.
    const fetchUser = async () => {
        try {
            // Proviamo a ottenere l'utente.
            const user = await auth.getUser();
            return { success: true, user: user };
        } catch (error) {
            // Se fallisce (401 o altro), non è un errore per noi, è un'informazione.
            // Restituiamo un oggetto che rappresenta lo stato di "non loggato".
            return { success: false, user: null };
        }
    };

    return {
        // Passiamo sempre le promesse al componente per non bloccare la navigazione
        streamed: {
            carBrands: fetchBrands(),
            userData: fetchUser(), // Ho rinominato la chiave per chiarezza
        }
    };
};