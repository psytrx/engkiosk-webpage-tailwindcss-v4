.DEFAULT_GOAL := help

VENV_NAME?=venv

.PHONY: help
help: ## Outputs the help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

venv/touchfile: requirements.txt
	test -d $(VENV_NAME) || python3 -m venv $(VENV_NAME)
	. $(VENV_NAME)/bin/activate; pip install -Ur requirements.txt
	touch $(VENV_NAME)/touchfile

venv: venv/touchfile

.PHONY: init
init: venv ## Creates a virtualenv and installs python requirements

.PHONY: episode-check
episode-check: ## Checks all Podcast Episodes if all player links (Spotify, etc.) are set
	. $(VENV_NAME)/bin/activate; python empty_player_urls.py

.PHONY: find_tags_that_need_descriptions-website-content
find_tags_that_need_descriptions-website-content: ## Checks all used tags that need SEO descriptions in Website content like podcasts or blog articles
	. $(VENV_NAME)/bin/activate; python find_tags_that_need_descriptions.py website-content

.PHONY: find_tags_that_need_descriptions-german-tech-podcasts
find_tags_that_need_descriptions-german-tech-podcasts: ## Checks all used tags that need SEO descriptions in external content like the german tech podcasts
	. $(VENV_NAME)/bin/activate; python find_tags_that_need_descriptions.py german-tech-podcasts

.PHONY: summary
summary: ## Creates a Podcast summary with statistics
	. $(VENV_NAME)/bin/activate; python summary.py
