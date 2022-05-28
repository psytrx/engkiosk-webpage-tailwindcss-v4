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
clean: ## Deletes the generated content
	rm -rf ./dist

.PHONY: update-content
update-content: ## Pulls the latest Podcas RSS feed and updates the content
	python ./scripts/podcast-feed-to-content.py

.PHONY: init
init: ## Installs dependencies
	npm install