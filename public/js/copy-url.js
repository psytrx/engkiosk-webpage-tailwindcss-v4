// How this piece of magic works?
// Read https://stackoverflow.com/questions/400212/how-do-i-copy-to-the-clipboard-in-javascript
function fallbackCopyTextToClipboard(text) {
	var textArea = document.createElement('textarea');
	textArea.value = text;

	// Avoid scrolling to bottom
	textArea.style.top = '0';
	textArea.style.left = '0';
	textArea.style.position = 'fixed';

	document.body.appendChild(textArea);
	textArea.focus();
	textArea.select();

	try {
		document.execCommand('copy');
		// We skip any result checking
	} catch (err) {
		// We skip any error checking
	}

	document.body.removeChild(textArea);
}

function copyTextToClipboard(text) {
	if (!navigator.clipboard) {
		fallbackCopyTextToClipboard(text);
		return;
	}
	navigator.clipboard.writeText(text);
	// We skip any promise result here (incl. error)
}

var copyBtn = document.querySelector('#copy-url');
copyBtn.addEventListener('click', function (event) {
	event.preventDefault();
	copyTextToClipboard(this.dataset.href);
});
