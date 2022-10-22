/**
 * addFilterListener adds required event listener to form
 * elements.
 * 
 * @return void
 */
function addFilterListener() {
	let filterLastEpisode = document.getElementById("filter-last-episode");
	filterLastEpisode.addEventListener("change", handleFilterLastEpisode); 
}

/**
 * handleFilterLastEpisode handles the change event on
 * the form field "Last episode" (1 week, 2 weeks, ...).
 * 
 * Both filter are exclusive to each other.
 * Only one can be active.
 * 
 * @param event elem 
 * @return void
 */
function handleFilterLastEpisode(elem) {
	filter();
}

/**
 * getSelectElementValue retrieves the selected value from
 * elementID. elementID need to be a <select> field.
 * 
 * @param string elementID 
 * @returns string
 */
function getSelectElementValue(elementID) {    
    const elem = document.getElementById(elementID);
    return elem.value;
}

/**
 * getFilterAttributes returns the current active filter.
 * 
 * @returns object
 */
function getFilterAttributes() {
	let currentFilter = {};

	const lastEpisodeFilter = getSelectElementValue("filter-last-episode");
	if (lastEpisodeFilter != "") {
		currentFilter["lastEpisode"] = lastEpisodeFilter;
	}

	return currentFilter
}

/**
 * makeEveryPodcastVisible ensures that every tech podcast
 * is visible on the page again. Independent from various filters.
 * 
 * @return void
 */
function makeEveryPodcastVisible() {
	const elements = document.getElementsByClassName("tech-podcast");
	for (let elem of elements) {
		elem.classList.remove("hidden");
	}
}

/**
 * filter takes care of the main logic, the filtering.
 * It gets the current active filter and hides or shows 
 * particular podcasts based on the selected filters.
 * 
 * The current filter are exclusive to each other.
 * Only one can be active.
 * 
 * @returns void
 */
function filter() {
	currentFilters = getFilterAttributes();
	if (Object.keys(currentFilters).length == 0) {
		makeEveryPodcastVisible();
		toggleNoFilterMatchMessage();
		return;
	}

	const elements = document.getElementsByClassName("tech-podcast");
	for (let elem of elements) {
		// Filter for "last episode published within the last X days"
		if ("lastEpisode" in currentFilters &&  currentFilters["lastEpisode"] != "") {
			if (parseInt(elem.dataset["daysSinceLastEpisode"]) <= parseInt(currentFilters["lastEpisode"])) {
				elem.classList.remove("hidden");
			} else {
				elem.classList.add("hidden");
			}
		}
	}

	toggleNoFilterMatchMessage();
	updateFilterCounter();
}

/**
 * updateFilterCounter updates particular HTML tags on the page that
 * indicates how many podcasts are available and how many are visible.
 *
 * @return void
 */
function updateFilterCounter() {
	const totalPodcasts = getTotalPodcastCounter();
	const visiblePodcasts = currentVisiblePodcastCounter();
	document.getElementById("filter-count-match").innerText = visiblePodcasts;
	document.getElementById("filter-count-total").innerText = totalPodcasts;
}

/**
 * toggleNoFilterMatchMessage ensures, if no podcast is matching the current
 * filter, that a "sorry, no match" message is shown.
 * 
 * @return void
 */
function toggleNoFilterMatchMessage() {
	const counter = currentVisiblePodcastCounter();

	// If there are no podcasts, matching all filter, show a small message
	if (counter == 0) {
		document.getElementById("no-filter-match").classList.remove("hidden");
	} else {
		document.getElementById("no-filter-match").classList.add("hidden");
	}
}

/**
 * currentVisiblePodcastCounter returns the number of podcasts visible on the page.
 * Filtered podcasts are not part of this counter, only visible ones.
 * 
 * @return number
 */
function currentVisiblePodcastCounter() {
	const elements = document.getElementsByClassName("tech-podcast");
	let counter =  elements.length;
	for (let elem of elements) {
		if (elem.classList.contains("hidden")) {
			counter -= 1;
		}
	}

	return counter;
}

/**
 * getTotalPodcastCounter returns the number of podcasts available in the listing.
 * Independent if visible or not.
 *
 * @return number
 */
function getTotalPodcastCounter() {
	const elements = document.getElementsByClassName("tech-podcast");
	return elements.length;
}

// Add event listener on the form filter elements
window.addEventListener('DOMContentLoaded', (event) => {
	// Make filter bar visible (only when javascript is activated)
	document.getElementById("filter").classList.remove("invisible");
	document.getElementById("filter-count").classList.remove("invisible");

	addFilterListener();

	updateFilterCounter();
});