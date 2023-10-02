// returns the date in the format of Monday, October 12, 2023
export function formatDate(date, locale = 'de-DE') {
	const options = {
		weekday: 'long',
		year: 'numeric',
		month: 'long',
		day: 'numeric',
	};
	return new Date(date).toLocaleDateString(locale, options);
}

export function formatUnixTimestampToDate(timestamp, locale = 'de-DE') {
	const options = {
		weekday: 'long',
		year: 'numeric',
		month: 'long',
		day: 'numeric',
	};
	return new Date(timestamp * 1000).toLocaleDateString(locale, options);
}

// returns the date in the format of October 12, 2023
export function formatDateWithoutWeekday(date, locale = 'de-DE') {
	const options = {
		year: 'numeric',
		month: 'long',
		day: 'numeric',
	};
	return new Date(date).toLocaleDateString(locale, options);
}

// returns the time in the format HH:MM
export function formatTime(date, locale = 'de-DE', timeZone = 'Europe/Berlin') {
	const options = {
		hour: 'numeric',
		minute: 'numeric',
		timeZone,
	};
	return new Date(date).toLocaleTimeString(locale, options);
}
