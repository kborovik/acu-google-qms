.PHONY: sync format lint typecheck test check clean \
	tf-init tf-fmt tf-validate tf-plan tf-apply tf-destroy terraform \
	release major minor patch help

UV ?= uv
TF_DIR ?= terraform
TF_ENV ?= dev

# `make release <part>` passes the part as an extra goal; pick it out and
# give the part words no-op recipes so make does not try to build them.
part := $(word 1,$(filter major minor patch,$(MAKECMDGOALS)))

help:
	@grep -E '^[a-zA-Z_.-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-14s %s\n", $$1, $$2}'

.venv:
	$(UV) venv

sync: .venv ## Install deps
	$(UV) sync --all-groups

format: .venv ## Format Python sources
	$(UV) run ruff format

lint: .venv ## Lint Python sources
	$(UV) run ruff check
	$(UV) run ruff format --check

typecheck: .venv ## Typecheck Python sources
	$(UV) run basedpyright

test: .venv ## Run pytest
	$(UV) run pytest

check: lint typecheck test ## Run typecheck + lint + test

clean: ## Clean caches/build
	rm -rf dist build .ruff_cache .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

###############################################################################
# Terraform
###############################################################################

tf-fmt: ## Format Terraform files recursively
	terraform fmt -recursive $(TF_DIR)

tf-init: ## Initialize Terraform
	terraform -chdir=$(TF_DIR) init -upgrade

tf-validate: ## Validate Terraform configs
	terraform -chdir=$(TF_DIR) validate

# -var-file is relative to -chdir; omit it until terraform/$(TF_ENV).tfvars exists.
TF_VAR_FILE_FLAG := $(if $(wildcard $(TF_DIR)/$(TF_ENV).tfvars),-var-file=$(TF_ENV).tfvars)

tf-plan: ## Generate Terraform plan (TF_ENV=dev|prd)
	terraform -chdir=$(TF_DIR) plan $(TF_VAR_FILE_FLAG) -out=$(TF_ENV).tfplan

tf-apply: ## Apply Terraform changes (TF_ENV=dev|prd)
	terraform -chdir=$(TF_DIR) apply $(if $(wildcard $(TF_DIR)/$(TF_ENV).tfplan),$(TF_ENV).tfplan,$(TF_VAR_FILE_FLAG))

tf-destroy: ## Destroy Terraform resources (TF_ENV=dev|prd)
	terraform -chdir=$(TF_DIR) destroy $(TF_VAR_FILE_FLAG)

terraform: tf-init tf-fmt tf-validate tf-plan ## Format, validate, plan; prompt to apply
	@printf 'Apply this plan? [y/N] ' >/dev/tty; \
	read ans </dev/tty; \
	case "$$ans" in \
	  [yY]|[yY][eE][sS]) terraform -chdir=$(TF_DIR) apply $(TF_ENV).tfplan ;; \
	  *) echo 'Skipped apply.' ;; \
	esac

###############################################################################
# Release
###############################################################################

release: check ## Bump version, promote CHANGELOG, commit, tag, push, create GitHub release
	@test -n "$(part)" || { echo "usage: make release major|minor|patch"; exit 1; }
	@git diff --quiet && git diff --cached --quiet \
		|| { echo "working tree not clean — commit or stash first"; exit 1; }
	@command -v gh >/dev/null \
		|| { echo "gh CLI required — https://cli.github.com/"; exit 1; }
	@gh auth status >/dev/null 2>&1 \
		|| { echo "gh not authenticated — run: gh auth login"; exit 1; }
	@set -euo pipefail; \
	echo "==> Checking CHANGELOG Unreleased has shippable bullets <=="; \
	./scripts/changelog check; \
	echo "==> Bumping $(part) version <=="; \
	$(UV) version --bump $(part); \
	version=$$($(UV) version --short); \
	echo "==> Promoting CHANGELOG Unreleased → v$$version <=="; \
	./scripts/changelog promote "$$version"; \
	git add pyproject.toml uv.lock CHANGELOG.md; \
	git commit -m "chore: release v$$version"; \
	git tag "v$$version"; \
	echo "==> Pushing v$$version <=="; \
	git push && git push --tags; \
	echo "==> Creating GitHub release v$$version <=="; \
	./scripts/changelog notes "$$version" | gh release create "v$$version" \
		--title "v$$version" \
		--notes-file - \
		--verify-tag; \
	echo "Released v$$version"

major minor patch:
	@:
