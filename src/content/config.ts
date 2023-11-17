import { z, defineCollection } from 'astro:content';

// Schema for Podcast Episodes
const podcastEpisodeCollection = defineCollection({
	type: 'content',
	schema: ({ image }) => z.object({
		amazon_music: z.string(),
		apple_podcasts: z.string(),
		audio: z.string(),
		chapter: z.array(
			z.object({
				start: z.string(),
				title: z.string(),
			})
		),
		deezer: z.string(),
		description: z.string(),
		google_podcasts: z.string(),
		headlines: z.string(),
		image: image(),
		length_second: z.number(),
		pubDate: z.date(),
		rtlplus: z.string(),
		speaker: z.array(
			z.object({
				name: z.string(),
				transcriptLetter: z.string(),
				website: z.string(),
			})
		),
		spotify: z.string(),
		tags: z.array(z.string()),
		title: z.string(),
		youtube: z.string(),
	}),
});

// Schema for Blog Entries
const blogEntryCollection = defineCollection({
	type: 'content',
	schema: z.object({
		title: z.string(),
		subtitle: z.string(),
		description: z.string(),
		tags: z.array(z.string()),
		pubDate: z.date(),
		thumbnail: z.string(),
		headerimage: z.string(),
	}),
});

// Export a single `collections` object to register your collection(s)
export const collections = {
	podcast: podcastEpisodeCollection,
	blog: blogEntryCollection,
};
