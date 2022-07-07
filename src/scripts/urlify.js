export function URLify(element) {
    // Replace whitespace with -
    let e = element.trim().replace(/\s/g, '-');

    return {
		"name": element,
		"url": e.toLowerCase()
	}
}