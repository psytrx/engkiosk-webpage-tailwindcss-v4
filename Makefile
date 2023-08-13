.DEFAULT_GOAL := help

.PHONY: help
help: ## Outputs the help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: ## Compiles the application into static content
	npm run build

.PHONY: run
run: ## Starts the development server
	npm run dev

.PHONY: clean
clean: ## Deletes the generated content and node_modules
	rm -rf ./dist
	rm -rf ./node_modules

.PHONY: update-content
update-content: ## Pulls the latest Podcast RSS feed and updates the content
	python ./scripts/podcast_feed_to_content.py sync

.PHONY: update-redirects
update-redirects: ## Writes all short url redirects for Podcast episodes to netlify.toml
	python ./scripts/podcast_feed_to_content.py redirect

.PHONY: episode-check
episode-check: ## Checks all Podcast Episodes if all player links (Spotify, etc.) are set
	python ./scripts/empty_player_urls.py

.PHONY: find_tags_that_need_descriptions-content-files
find_tags_that_need_descriptions-content-files: ## Checks all used tags in content files (blog posts and podcasts) that need SEO descriptions and output them on stdout
	python ./scripts/find_tags_that_need_descriptions.py website-content

.PHONY: find_tags_that_need_descriptions-german-tech-podcast-file
find_tags_that_need_descriptions-german-tech-podcast-file: ## Checks all used tags in the german tech podcasts that need SEO descriptions and output them on stdout
	python ./scripts/find_tags_that_need_descriptions.py german-tech-podcasts

.PHONY: find_tags_that_need_descriptions-content-files-dump
find_tags_that_need_descriptions-content-files-dump: ## Find all used tags in content files (blog posts and podcasts) that need SEO descriptions and dump it down to disk into tag-file
	python ./scripts/find_tags_that_need_descriptions.py -write-file website-content

.PHONY: find_tags_that_need_descriptions-german-tech-podcast-file-dump
find_tags_that_need_descriptions-german-tech-podcast-file-dump: ## Find all used tags in the german tech podcasts that need SEO descriptions and dump it down to disk into tag-file
	python ./scripts/find_tags_that_need_descriptions.py -write-file german-tech-podcasts

.PHONY: sync_german_tech_podcasts
sync_german_tech_podcasts: ## Syncs German Tech Podcasts data from https://github.com/EngineeringKiosk/GermanTechPodcasts
	python ./scripts/sync_german_tech_podcasts.py

.PHONY: init
init: ## Installs dependencies
	npm install

.PHONY: eslint
eslint: ## Statically analyzes of basic JavaScript scripts
	node_modules/.bin/eslint --config .eslintrc src/scripts

.PHONY: prettier
prettier: ## Run prettier (file formatting)
	node_modules/.bin/prettier -w .
