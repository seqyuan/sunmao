.PHONY: help install install-dev test lint format docs clean build publish

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package
	poetry install --no-dev

install-dev: ## Install the package in development mode
	poetry install

test: ## Run tests
	poetry run pytest tests/ -v

lint: ## Run linting
	poetry run flake8 sunmao/
	poetry run black --check sunmao/
	poetry run mypy sunmao/

format: ## Format code
	poetry run black sunmao/
	poetry run isort sunmao/

docs: ## Build documentation
	cd docs && make html

docs-serve: ## Serve documentation locally
	cd docs/_build/html && python -m http.server 8000

clean: ## Clean build artifacts
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	rm -rf docs/_build/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: ## Build the package
	poetry build

publish: ## Publish to PyPI
	poetry publish

release: ## Create a new release
	python scripts/release.py

setup-git: ## Setup git repository
	git init
	git add .
	git commit -m "Initial commit"

setup-github: ## Setup GitHub repository (requires GitHub CLI)
	gh repo create seqyuan/sunmao --public --description "A flexible subplot layout library for matplotlib"
	git remote add origin https://github.com/seqyuan/sunmao.git
	git push -u origin main

setup-readthedocs: ## Setup ReadTheDocs project
	@echo "Please visit https://readthedocs.org/dashboard/ and:"
	@echo "1. Import project from GitHub"
	@echo "2. Set repository: https://github.com/seqyuan/sunmao"
	@echo "3. Set configuration file: readthedocs.yaml"
	@echo "4. Enable automatic builds"

check: lint test ## Run all checks

all: clean install-dev test lint build ## Run all checks and build
