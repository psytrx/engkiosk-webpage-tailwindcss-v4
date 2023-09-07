export function formatDate(date, locale = "de-DE") {
	const options = {
		weekday: 'long',
		year: 'numeric',
		month: 'long',
		day: 'numeric',
	};
	return new Date(date).toLocaleDateString(locale, options);
}

export function formatUnixTimestampToDate(timestamp, locale = "de-DE") {
	const options = {
		weekday: 'long',
		year: 'numeric',
		month: 'long',
		day: 'numeric',
	};
	return new Date(timestamp * 1000).toLocaleDateString(locale, options);
}

export function formatDateWithoutWeekday(date, locale = "de-DE") {
	const options = {
		year: 'numeric',
		month: 'long',
		day: 'numeric',
	};
	return new Date(date).toLocaleDateString(locale, options);
}

export function formatTime(date, locale = "de-DE") {
	const options = {
		hour: 'numeric',
		minute: 'numeric'
	}
	return new Date(date).toLocaleTimeString(locale, options);
}
