# GCP Agent Platform

## §G GOAL
Implement LLM application per `domain/` (CoA ingestion → Acumatica QMS lot-release).

## §C CONSTRAINTS
- Python 3.14
- Google ADK for agent source
- uv owns deps; no `requirements.txt`
- ruff lint + format
- basedpyright strict
- Provider `hashicorp/google`; `hashicorp/google-beta` for `google_vertex_ai_reasoning_engine` (`context_spec` Memory Bank)
- Exactly 1 agent, 1 store
- No console-created Agent Platform resources
- Domain CoA/Acumatica docs stay in `domain/`; not this spec
- Not provision Vector Search ANN serving nodes
- `terraform apply` succeeds w/o agent source artifact
- Local tfstate OK this spec; remote backend later
- Two GCP projects: `lab5-acucoa-dev1`, `lab5-acucoa-prd1`
- Env diffs live in `terraform/<project>.tfvars`; shared `.tf` identical

## §I INTERFACES
- tf: `terraform/` → versions, provider google, vars `project` `region`; tfvars `lab5-acucoa-dev1.tfvars` `lab5-acucoa-prd1.tfvars` named after GCP project
- resource: `google_vertex_ai_reasoning_engine` (google-beta) display_name + `context_spec.memory_bank_config`; no `package_spec` this spec
- sa: dedicated engine SA → `roles/aiplatform.user` + `roles/storage.objectViewer` + `roles/secretmanager.secretAccessor`
- gcs: artifact bucket for later package_spec
- api: `aiplatform.googleapis.com`, `apikeys.googleapis.com`, `secretmanager.googleapis.com` via `google_project_service`
- key: `google_apikeys_key` for Gemini API
- secret: `google_secret_manager_secret` + `google_secret_manager_secret_version` for Gemini API key
- cmd: `terraform -chdir=terraform init && terraform -chdir=terraform apply -var-file=<project>.tfvars` → engine + store
- out: `reasoning_engine_name`, `service_account_email`, `artifact_bucket`, `gemini_api_key_secret_id`
- py: `agent/` Google ADK source; Python 3.14
- pkg: uv `pyproject.toml`; no `requirements.txt`
- adk: Google ADK agent module
- lint: `uv run ruff check && uv run ruff format --check && uv run basedpyright` → pass

## §V INVARIANTS
V1: terraform-sole-source — Agent Platform resources exist only as Terraform-managed; console create banned
V2: python-adk-stack — agent source is Google ADK on Python 3.14; uv owns deps (no `requirements.txt`); ruff + basedpyright strict pass
V3: one-agent-one-store — exactly 1 `google_vertex_ai_reasoning_engine` (google-beta); Memory Bank via `context_spec.memory_bank_config` on that engine
V4: engine-identity — engine runs as dedicated SA w/ `roles/aiplatform.user` + `roles/storage.objectViewer` + `roles/secretmanager.secretAccessor`; not user ADC
V5: apis-via-tf — `aiplatform.googleapis.com`, `apikeys.googleapis.com`, `secretmanager.googleapis.com` enabled via `google_project_service` before engine
V6: no-idle-nodes — not provision Vector Search ANN serving or always-on prediction endpoints
V7: apply-without-agent-source — `terraform apply` succeeds w/o `package_spec` / pickle; source attach later spec
V8: outputs-addressable — apply emits reasoning engine resource name, SA email, artifact bucket, Gemini API key secret ID
V9: state-not-committed — tfstate not committed; `.gitignore` covers `.terraform/` `*.tfstate` `*.tfstate.backup`
V10: tfvars-env-diff — committed `terraform/<project>.tfvars` hold env values for `lab5-acucoa-dev1` and `lab5-acucoa-prd1`; shared `.tf` identical; apply via `-var-file`

## §T TASKS
id|status|task|cites
T1|x|init `terraform/` root: versions, google provider pin, vars `project` `region`|I.tf
T2|x|enable `aiplatform.googleapis.com`, `apikeys.googleapis.com`, `secretmanager.googleapis.com` via `google_project_service`|V5,I.api
T3|x|add dedicated engine SA + `roles/aiplatform.user` + `roles/storage.objectViewer` + `roles/secretmanager.secretAccessor`|V4,I.sa
T4|x|add GCS artifact bucket for later package_spec|V7,I.gcs
T5|x|add `google_vertex_ai_reasoning_engine` (google-beta) w/ Memory Bank `context_spec`; no `package_spec`|V1,V3,V7,I.resource,B1
T6|x|emit outputs `reasoning_engine_name` `service_account_email` `artifact_bucket`|V8,I.out,B2
T7|x|extend `.gitignore` for `.terraform/` `*.tfstate` `*.tfstate.backup`|V9
T8|x|`terraform fmt` + `terraform validate` pass|T1,T2,T3,T4,T5,T6,T13,T14
T9|x|init uv project Python 3.14 `pyproject.toml` + `.python-version`; no `requirements.txt`|V2,I.pkg
T10|x|set ruff + basedpyright strict in `pyproject.toml`|V2,I.pkg
T11|.|add Google ADK dep + minimal agent module in `agent/`|V2,I.adk,I.py
T12|.|`uv run ruff check` + `uv run ruff format --check` + `uv run basedpyright` pass|V2,I.lint
T13|.|add `google_apikeys_key` + `google_secret_manager_secret` for Gemini API key + output `gemini_api_key_secret_id`|V4,V5,V8,I.key,I.secret,I.out,B2
T14|x|add `terraform/lab5-acucoa-dev1.tfvars` + `terraform/lab5-acucoa-prd1.tfvars` w/ `project` + `region`|V10,I.tf
T15|x|set Makefile `TF_ENV` default `lab5-acucoa-dev1`; `-var-file` named after GCP project|V10,I.tf,I.cmd

## §B BUGS
id|date|cause|fix
B1|2026-09-02|GA hashicorp/google 8.1 `google_vertex_ai_reasoning_engine` no `context_spec`; Memory Bank is google-beta, resource-root not `spec.context_spec`|V3
B2|2026-09-02|T6 output `gemini_api_key_secret_id` refs `google_secret_manager_secret` T13 not declared|-
