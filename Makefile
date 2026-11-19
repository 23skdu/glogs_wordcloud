.DEFAULT_GOAL := help
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c

PYTHON ?= python3.13
UV ?= uv
VENV ?= .venv
TF_DIR ?= infra/terraform
IMAGE ?= glogs-wordcloud:local

.PHONY: help setup lint format test security docker-build tf-fmt tf-validate tf-plan clean all

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  %-18s %s\n", $$1, $$2}'

setup: ## Create venv and install dependencies
	$(UV) venv --python $(PYTHON) $(VENV) 2>/dev/null || true
	$(UV) sync --extra dev
	$(UV) run pre-commit install || true

lint: setup ## Run linters and type checks
	$(UV) run ruff check .
	$(UV) run ruff format --check .
	$(UV) run mypy

format: setup ## Auto-format code
	$(UV) run ruff check --fix .
	$(UV) run ruff format .

test: setup ## Run tests
	$(UV) run pytest

security: setup ## Run security scans
	$(UV) run bandit -r src -c pyproject.toml
	$(UV) run pip-audit
	@if $(UV) run detect-secrets --version >/dev/null 2>&1; then \
	  $(UV) run detect-secrets scan; \
	else \
	  echo "detect-secrets not available, skipping"; \
	fi
	@if command -v gitleaks >/dev/null 2>&1; then \
	  gitleaks detect --source . --no-git; \
	else \
	  echo "gitleaks not available, skipping"; \
	fi
	trivy fs --severity HIGH,CRITICAL --exit-code 1 --skip-dirs .venv --skip-dirs dist --skip-dirs build .
	@if command -v hadolint >/dev/null 2>&1; then \
	  hadolint Dockerfile; \
	else \
	  echo "hadolint not available, skipping"; \
	fi
	checkov -d $(TF_DIR) --framework terraform --quiet

tf-fmt: ## Format Terraform
	terraform -chdir=$(TF_DIR) fmt -recursive

tf-validate: ## Validate Terraform
	terraform -chdir=$(TF_DIR) init -backend=false
	terraform -chdir=$(TF_DIR) validate
	terraform -chdir=$(TF_DIR) fmt -check -recursive

tf-plan: tf-validate ## Plan Terraform changes
	terraform -chdir=$(TF_DIR) plan

docker-build: ## Build container image
	docker build --pull -t $(IMAGE) .

clean: ## Remove build artifacts
	rm -rf $(VENV) .pytest_cache .ruff_cache .mypy_cache .coverage htmlcov dist build
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +

all: setup lint test security tf-validate docker-build ## Run everything