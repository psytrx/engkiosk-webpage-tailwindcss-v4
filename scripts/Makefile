.DEFAULT_GOAL := help

VENV_NAME?=venv
VENV_ACTIVATE=$(VENV_NAME)/bin/activate

.PHONY: help
help: ## Outputs the help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# target is only run if the target or any of the prerequisites have changed (touchfile)
venv/touchfile: requirements.txt
	test -d $(VENV_NAME) || python3 -m venv $(VENV_NAME)
	. $(VENV_ACTIVATE) && pip install --require-virtualenv -Ur requirements.txt
	touch $(VENV_NAME)/touchfile

.PHONY: init
init: venv/touchfile ## Installs python dependencies and creates a virtualenv
