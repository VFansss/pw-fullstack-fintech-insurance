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
            
            // Gestione migliorata degli errori di validazione
            let errorMessage = '';
            
            if (errorData.detail) {
                errorMessage = errorData.detail;
            } else if (errorData.non_field_errors) {
                errorMessage = errorData.non_field_errors[0];
            } else if (errorData.password1) {
                // Errori specifici del campo password1
                errorMessage = `Password: ${errorData.password1.join(', ')}`;
            } else if (errorData.password2) {
                // Errori specifici del campo password2
                errorMessage = `Conferma Password: ${errorData.password2.join(', ')}`;
            } else if (errorData.email) {
                errorMessage = `Email: ${errorData.email.join(', ')}`;
            } else if (errorData.username) {
                errorMessage = `Username: ${errorData.username.join(', ')}`;
            } else {
                // Fallback per altri errori di campo
                const firstError = Object.keys(errorData)[0];
                if (firstError && errorData[firstError]) {
                    const fieldErrors = Array.isArray(errorData[firstError]) ? errorData[firstError] : [errorData[firstError]];
                    errorMessage = `${firstError}: ${fieldErrors.join(', ')}`;
                } else {
                    errorMessage = `HTTP error! status: ${response.status}`;
                }
            }
            
            throw new Error(errorMessage);
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
    first_name: string;
    last_name: string;
}

export interface QuoteData {
    car_brand: string;
    car_model: string;
    license_plate: string;
    birth_date: string; // Formato "YYYY-MM-DD"
    license_year: number;
    km_per_year: string; 
    driving_style: string;
    vehicle_type: string;
    // Aggiungiamo anche i dati anagrafici, perché nel caso di un utente
    // non loggato, sono obbligatori.
    first_name: string;
    last_name: string;
    email: string;
}

interface SimulateQuoteData {
    car_brand: string;
    car_model: string;
    license_plate: string;
    km_per_year: string;
    driving_style: string;
    birth_date: string;
    license_year: number;
    vehicle_type: string;
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
            body: JSON.stringify({
                username: details.username,
                email: details.email,
                password1: details.password,
                password2: details.password2,
                first_name: details.first_name,
                last_name: details.last_name,
            }),
        }),
    getUser: () => apiFetch('/api/auth/user/'),

    logout: () => apiFetch('/api/auth/logout/', { method: 'POST' }),
};

export const quotes = {
    /**
     * Crea un nuovo preventivo.
     * La logica del backend associerà il preventivo all'utente se la chiamata è autenticata.
     */
    /**
     * Calcola un preventivo senza salvarlo. Endpoint pubblico.
     */
    simulate: (simulationData: SimulateQuoteData) => 
        apiFetch('/api/quotes/simulate/', {
            method: 'POST',
            body: JSON.stringify(simulationData)
        }),

    /**
     * Crea e salva un nuovo preventivo. Richiede autenticazione.
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

    clearAll: () => 
        apiFetch('/api/quotes/clear-all/', {
            method: 'DELETE',
        }),

};

export const general = {
    getVehicleBrands: (vehicleType: string): Promise<string[]> => 
        apiFetch(`/api/vehicle-data/${vehicleType}/brands/`),

    getGlobalStats: () => apiFetch('/api/stats/global/'),
};

export const policies = {
    getAll: () => apiFetch('/api/policies/'),
    getById: (id: number) => apiFetch(`/api/policies/${id}/`),
    getStats: () => apiFetch('/api/policies/stats/'),
    createFromQuote: (quoteId: number) => 
        apiFetch('/api/policies/create-from-quote/', {
            method: 'POST',
            body: JSON.stringify({ quote_id: quoteId }),
        }),
};