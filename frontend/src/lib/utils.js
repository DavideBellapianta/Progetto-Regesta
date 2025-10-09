/**
 * @param {string} name La stringa da convertire.
 * @returns {string} Lo slug generato.
 */
export function createSlug(name) {
	if (!name) return '';
	return name
		.toLowerCase()
		.replace(/\s+/g, '-')
		.replace(/[()]/g, '')
		.replace(/[^\w-]+/g, '');
}