.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: venvcheck ## Check if venv is active
venvcheck:
ifeq ("$(VIRTUAL_ENV)","")
	@echo "Venv is not activated!"
	@echo "Activate venv first."
	@echo
	exit 1
endif


.PHONY: install
install: venvcheck  ## Install the dependencies
	@pip install -r requirements.txt


.PHONY: lint
lint: venvcheck		## Run Black and Isort linters
	@black .
	@isort .
	@mypy .


.PHONY: update
update: venvcheck
	@echo "fastapi uvloop konfik uvicorn httpx" | xargs -n 1 -d ' ' -P 5 -I {} sh -c "pip freeze | grep {}"
