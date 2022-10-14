import rss from '@astrojs/rss';

const rssItems  = import.meta.glob([
    './blog/post/*.mdx',
    './podcast/episode/*.md'
]);

// Docs: https://docs.astro.build/en/guides/rss/
export const get = () => rss({
    title: 'Engineering Kiosk',
    description: 'Der deutschsprachige Software-Engineering-Podcast mit Wolfgang Gassler und Andy Grunwald rund um die Themen Engineering-Kultur, Open Source und Technologie.',
    site: import.meta.env.SITE,
    items: rssItems,
    customData: `<language>de-de</language>`,
});