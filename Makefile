# Makefile to gather common commands

.PHONY: clean format help lint pipenv-dev-install
.DEFAULT_GOAL := help

# Project variables
SRC:=src/$(MODULE)

help: ## Show this help menu
	$(info Available make commands:)
	@grep -e '^[a-z|_|-]*:.* ##' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS=":.* ## "}; {printf "\t%-23s %s\n", $$1, $$2};'

.print-phony:
	@echo -en "\n.PHONY: "
	@grep -e '^[a-z|_|-]*:.* ##' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS=":.* ## "}; {printf "%s ", $$1};'
	@echo -e "\n"

####### COMMANDS #######################################################################

clean: ## Clean up auxiliary and temporary files from the workspace
	$(info Cleaning auxiliary and temporary files...)
	@find . -maxdepth 1 -type d -name '.mypy_cache' -exec rm -r {} +
	@find . -maxdepth 1 -type d -name '.ruff_cache' -exec rm -r {} +
	@find . -maxdepth 1 -type d -name 'build'       -exec rm -r {} +
	@find . -maxdepth 1 -type d -name 'dist'        -exec rm -r {} +
	@find . -maxdepth 2 -type d -name '*.egg-info'  -exec rm -r {} +
	@echo Done.

format: ## Format the entire codebase
	@if \
	type black >/dev/null 2>&1 ; then \
		echo Formatting source-code... && \
		echo Applying black... && \
		black -q $(SRC) && \
		echo Done. ; \
	else echo SKIPPED. Run 'make pipenv-dev-install' first. >&2 ; fi

lint: ## Perform a static code analysis
	@if \
	type ruff >/dev/null 2>&1 ; then \
		echo Linting source-code... && \
		echo Applying ruff... && \
		ruff check $(SRC) && \
		echo Done. ; \
	else echo SKIPPED. Run 'make pipenv-dev-install' first. >&2 ; fi

pipenv-dev-install: ## Create dev venv
	@pipenv run pip install --upgrade pip
	@pipenv install --dev --ignore-pipfile --deploy

docker-build: ## Build all Dockerfile images for onebrc
	@docker build -f cpython.Dockerfile -t onebrc-cpython .
	@docker build -f cpython_perf.Dockerfile -t onebrc-cpython_perf .

run-cpython-docker-100t: ## Run all modules inside a docker container using 100t.txt
	@python -m onebrc.00_native_DictReader /onebrc/test_data/100t.txt
	@python -m onebrc.01_native_split /onebrc/test_data/100t.txt
	@python -m onebrc.02_native_read_text /onebrc/test_data/100t.txt

run-cpython-docker-100m: ## Run all modules inside a docker container using 100m.txt
	@python -m onebrc.00_native_DictReader /onebrc/test_data/100m.txt
	@python -m onebrc.01_native_split /onebrc/test_data/100m.txt
	@python -m onebrc.02_native_read_text /onebrc/test_data/100m.txt
