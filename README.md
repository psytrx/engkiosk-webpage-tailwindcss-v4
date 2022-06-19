# Engineering Kiosk: Web page

Built with [Astro](https://astro.build/). 

Check it out at [engineeringkiosk.dev](https://www.engineeringkiosk.dev/)

## Getting started

```sh
$ make init

$ make run
```

## 🧞 Commands

All commands are run from the root of the project, from a terminal.


Available `Makefile` commands:

```
build                          Compiles the application into static content
clean                          Deletes the generated content
episode-check                  Checks all Podcast Episodes if all player links (Spotify, etc.) are set
help                           Outputs the help
init                           Installs dependencies
run                            Starts the development server
update-content                 Pulls the latest Podcast RSS feed and updates the content
update-redirects               Writes all short url redirects for Podcast episodes to netlify.toml
```

Native npm commands:

| Command           | Action                                       |
|:----------------  |:-------------------------------------------- |
| `npm install`     | Installs dependencies                        |
| `npm run dev`     | Starts local dev server at `localhost:3000`  |
| `npm run build`   | Build your production site to `./dist/`      |
| `npm run preview` | Preview your build locally, before deploying |

Native python script commands:

```
$ python3 scripts/podcast-feed-to-content.py -h
usage: podcast-feed-to-content.py [-h] [mode]

Automate new Podcast Episide parsing

positional arguments:
  mode        Mode to execute. Supported: sync, redirect (default: sync)

options:
  -h, --help  show this help message and exit
```

## Checklist: Releasing a new Podcast episode

1. Run GitHub Actions [Publish Podcast Episodes](https://github.com/EngineeringKiosk/webpage/actions/workflows/publish-podcast-episodes.yml)
2. Copy Episode Single View URL from [Engineering Kiosk at Amazon Music](https://music.amazon.com/podcasts/c35a09fe-4116-4e04-8f68-77d61b112e46/engineering-kiosk)
3. Add the Episode Single View URL into the Frontmatter of the newly released Podcast episode
4. Commit, push and wait until Netlify is building the new website version.

## Netlify

This page is hosted on Netlify.

Docs for the file based configuration of Netlify are available at https://docs.netlify.com/configure-builds/file-based-configuration/