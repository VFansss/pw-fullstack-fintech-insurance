// Questo file serve a dire al builder quali pagine statiche generare per la rotta [tipo]

/** @type {import('./$types').EntryGenerator} */
export function entries() {
	// Restituiamo un array di oggetti, dove ogni oggetto
	// rappresenta i parametri per una pagina da generare.
	return [
		{ tipo: 'auto' },
		{ tipo: 'moto' },
		{ tipo: 'autocarro' }
	];
}

// Già che ci siamo, confermiamo che queste pagine devono essere prerenderizzate.
export const prerender = true;