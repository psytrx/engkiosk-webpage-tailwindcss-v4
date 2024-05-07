const fs = require('fs')
const matter = require('gray-matter');

transcriptPath = './src/data/transcripts/'
metadataPath = './src/content/podcast/'

// examples: -1-transcript-slim.json, 2-transcript-slim.json. 03-longtitel67-blabla.md
const getEpisodeNumber = (str) => {
	// if first char is "-" include it as it is a negative number
	const negative = str[0] === '-'
	const number = str.match(/\d+/)[0]
	return negative ? -number : +number
}

const exportIntroText = () => {

	const files = fs.readdirSync(transcriptPath).filter(file => file.endsWith('.json'))

	const introTexts = files.map(file => {
		const episodeNumber = getEpisodeNumber(file)
		const data = JSON.parse(fs.readFileSync(transcriptPath + file))
		const firstUtterance = data.utterances[0]

		const episode = {
			episodeNumber,
			intro: undefined
		}

		// not all episodes starts with an intro text. sometimes there are quotes of the episode
		// criteria: longer than 30secs or contains the words "willkommen" or "los" (geht's)
		if (firstUtterance.end - firstUtterance.start > 30000 || firstUtterance.text.toLowerCase().includes('willkommen') || firstUtterance.text.toLowerCase().includes('los')) {
			episode.intro = firstUtterance.text
		}
		return episode

	})

	return introTexts

}

const fetchEpisodeMetadata = () => {

	const files = fs.readdirSync(metadataPath).filter(file => file.endsWith('.md'))

	const episodeMetadata = files.map(file => {
		const episodeNumber = getEpisodeNumber(file)
		const data = fs.readFileSync(metadataPath + file, 'utf8')
		// parse matter
		const { data: metadata } = matter(data)

		const chapters = metadata.chapter.map(chapter => {
			return `(${chapter.start}) ${chapter.title}`
		})

		return {
			episodeNumber,
			title: metadata.title,
			chapters
		}

	})
	return episodeMetadata
}

const introTexts = exportIntroText()
const metadata = fetchEpisodeMetadata()

const episodes = metadata.map(episode => {
	const intro = introTexts.find(intro => intro.episodeNumber === episode.episodeNumber)
	return {
		...episode,
		...intro
	}
})

console.log(JSON.stringify(episodes, null, 2))
