export function formatDate(date) {
	const options = {
		weekday: 'long',
		year: 'numeric',
		month: 'long',
		day: 'numeric'
	};
	return new Date(date).toLocaleDateString('de-DE', options);
}

export function formatUnixTimestampToDate(timestamp) {
	const options = {
		weekday: 'long',
		year: 'numeric',
		month: 'long',
		day: 'numeric'
	};
	return new Date(timestamp * 1000).toLocaleDateString('de-DE', options);
}

export function formatDateWithoutWeekday(date) {
	const options = {
		year: 'numeric',
		month: 'long',
		day: 'numeric'
	};
	return new Date(date).toLocaleDateString('de-DE', options);
}