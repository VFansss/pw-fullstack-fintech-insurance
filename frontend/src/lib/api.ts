// frontend/src/lib/api.ts

import { PUBLIC_BACKEND_URL } from '$env/static/public';

/*

    --- 1. CONFIGURAZIONE E HELPER DI BASE ---

*/

// Questa è la nostra funzione "wrapper" per il fetch.
// Prende un percorso (es. '/api/auth/login/') e delle opzioni (metodo, body, etc.)
// e fa la chiamata completa all'URL del backend.
async function apiFetch(path: string, options: RequestInit = {}) {
    const url = `${PUBLIC_BACKEND_URL}${path}`;

    // Controlliamo se abbiamo un token nel localStorage
    const authToken = localStorage.getItem('authToken');

    // Aggiungiamo il Content-Type di default e, se esiste, il token di autenticazione
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (authToken) {
        headers['Authorization'] = `Token ${authToken}`;
    }

    try {
        const response = await fetch(url, {
            ...options,
            headers,
        });

        // Gestione centralizzata degli errori
        if (!response.ok) {
            // Proviamo a leggere l'errore JSON dal backend
            const errorData = await response.json().catch(() => ({}));
            // Creiamo un errore più descrittivo
            throw new Error(errorData.detail || errorData.non_field_errors?.[0] || `HTTP error! status: ${response.status}`);
        }

        // Se la risposta è vuota (es. un 204 No Content), restituiamo null
        if (response.status === 204) {
            return null;
        }
        
        return await response.json();

    } catch (error) {
        console.error('API Fetch Error:', error);
        // Rilanciamo l'errore in modo che il componente che ha chiamato possa gestirlo
        throw error;
    }
}

/*

    --- 2. INTERFACCE (TIPI) ---

*/

interface LoginCredentials {
    username: string;
    password: string;
}

interface RegistrationDetails {
    username: string;
    email: string;
    password: string;
    password2: string;
}

export interface QuoteData {
    car_brand: string;
    car_model: string;
    license_plate: string;
    birth_date: string; // Formato "YYYY-MM-DD"
    license_year: number;
    // Aggiungiamo anche i dati anagrafici, perché nel caso di un utente
    // non loggato, sono obbligatori.
    first_name: string;
    last_name: string;
    email: string;
}

/*

    --- 3. EXPORTS PER DOMINIO ---

*/

export const auth = {

    login: (credentials: LoginCredentials) => 
        apiFetch('/api/auth/login/', {
            method: 'POST',
            body: JSON.stringify(credentials),
        }),
    
    register: (details: RegistrationDetails) => 
        apiFetch('/api/auth/registration/', {
            method: 'POST',
            body: JSON.stringify(details),
        }),

    getUser: () => apiFetch('/api/auth/user/'),

    logout: () => apiFetch('/api/auth/logout/', { method: 'POST' }),
};

export const quotes = {
    /**
     * Crea un nuovo preventivo.
     * La logica del backend associerà il preventivo all'utente se la chiamata è autenticata.
     */
    create: (quoteData: QuoteData) => 
        apiFetch('/api/quotes/', {
            method: 'POST',
            body: JSON.stringify(quoteData),
        }),

    /**
     * Ottiene la lista dei preventivi per l'utente attualmente autenticato.
     * Richiede un token valido.
     */
    getAll: () => apiFetch('/api/quotes/'),

    /**
     * Ottiene i dettagli di un singolo preventivo.
     * Richiede un token valido e che l'utente sia il proprietario del preventivo.
     */
    getById: (id: number) => apiFetch(`/api/quotes/${id}/`),
};

export const general = {
    /**
     * Ottiene la lista di tutte le marche di auto disponibili.
     * È una chiamata pubblica, non richiede autenticazione.
     * @returns {Promise<string[]>} Una promessa che risolve in un array di stringhe.
     */
    getCarBrands: (): Promise<string[]> => apiFetch('/api/car-brands/'),
};

// Esportiamo anche le funzioni per le altre parti dell'API
export const policies = {
    // Esempio:
    // getAll: () => apiFetch('/api/policies/'),
    // getById: (id: number) => apiFetch(`/api/policies/${id}/`),
};