/**
 * addFilterListener adds required event listener to form
 * elements.
 * 
 * @return void
 */
function addFilterListener() {
	let filterActivity = document.getElementById("filter-activity");
	filterActivity.addEventListener("change", handleFilterActivity); 

	let filterLastEpisode = document.getElementById("filter-last-episode");
	filterLastEpisode.addEventListener("change", handleFilterLastEpisode); 

	let filterReset = document.getElementById("filter-reset");
	filterReset.addEventListener("click", podcastFilterReset); 
}

/**
 * podcastFilterReset resets the filter form.
 * 
 * @return void
 */
function podcastFilterReset() {
	setSelectElementValue("filter-activity", "");
	setSelectElementValue("filter-last-episode", "");
	filter();
}

/**
 * handleFilterActivity handles the change event on
 * the form field "Activity" (active, inactive, ...).
 * 
 * Both filter are exclusive to each other.
 * Only one can be active.
 * 
 * @param event elem 
 * @return void
 */
function handleFilterActivity(elem) {
	setSelectElementValue("filter-last-episode", "");
	filter();
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
	setSelectElementValue("filter-activity", "");
	filter();
}

/**
 * setSelectElementValue sets valueToSelect on elementID.
 * elementID need to be a <select> field.
 *
 * @param string elementID 
 * @param string valueToSelect 
 * @return void
 */
function setSelectElementValue(elementID, valueToSelect) {    
    let elem = document.getElementById(elementID);
    elem.value = valueToSelect;
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

	const activityFilter = getSelectElementValue("filter-activity");
	if (activityFilter != "") {
		currentFilter["publishingEpisodeStatus"] = activityFilter;
	}

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
		// We only have two filters which are exclusive to each other.
		// Filter for "is the podcast considered as active?"
		if ("publishingEpisodeStatus" in currentFilters && currentFilters["publishingEpisodeStatus"] != "") {
			if (elem.dataset["publishingEpisodeStatus"] == currentFilters["publishingEpisodeStatus"]) {
				elem.classList.remove("hidden");
			} else {
				elem.classList.add("hidden");
			}
		}

		// Andere TODOs
		// - Filter einblenden, nur wenn JS verfügbar ist

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
}

/**
 * toggleNoFilterMatchMessage ensures, if no podcast is matching the current
 * filter, that a "sorry, no match" message is shown.
 * 
 * @return void
 */
function toggleNoFilterMatchMessage() {
	const counter = currentPodcastCounter();

	// If there are no podcasts, matching all filter, show a small message
	if (counter == 0) {
		document.getElementById("no-filter-match").classList.remove("hidden");
	} else {
		document.getElementById("no-filter-match").classList.add("hidden");
	}
}

/**
 * currentPodcastCounter returns the number of podcasts visible on the page.
 * Filtered podcasts are not part of this counter, only visible ones.
 * 
 * @return number
 */
function currentPodcastCounter() {
	const elements = document.getElementsByClassName("tech-podcast");
	let counter = elements.length;
	for (let elem of elements) {
		if (elem.classList.contains("hidden")) {
			counter -= 1;
		}
	}

	return counter;
}

// Add event listener on the form filter elements
window.addEventListener('DOMContentLoaded', (event) => {
	// Make filter bar visible (only when javascript is activated)
	document.getElementById("filter").classList.remove("invisible");

	addFilterListener();
});