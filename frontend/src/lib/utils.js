/**
 * @param {string} name 
 * @returns {string} slug
 */
export function createSlug(name) { //Crea lo slug per i prodotti (URL)
	if (!name) return '';
	return name
		.toLowerCase()
		.replace(/\s+/g, '-')
		.replace(/[()]/g, '')
		.replace(/[^\w-]+/g, '');
}