# GCP Agent Platform

## §G GOAL
Terraform sole-provisions 1 Gemini Enterprise Agent Platform agent + Memory Bank store; Python/ADK deferred.

## §C CONSTRAINTS
- Python/ADK source, pickle, `requirements.txt` out of this spec §T (later session)
- Provider `hashicorp/google`; resource `google_vertex_ai_reasoning_engine`
- Exactly 1 agent, 1 store
- No console-created Agent Platform resources
- Domain CoA/Acumatica docs stay in `specs/`; not this spec
- Not provision Vector Search ANN serving nodes
- `terraform apply` succeeds w/o agent source artifact
- Local tfstate OK this spec; remote backend later

## §I INTERFACES
- tf: `terraform/` → versions, provider google, vars `project` `region`
- resource: `google_vertex_ai_reasoning_engine` display_name + `spec.context_spec.memory_bank_config`; no `package_spec` this spec
- sa: dedicated engine SA → `roles/aiplatform.user` + `roles/storage.objectViewer`
- gcs: artifact bucket for later package_spec
- api: `aiplatform.googleapis.com` via `google_project_service`
- cmd: `terraform -chdir=terraform init && terraform -chdir=terraform apply` → engine + store
- out: `reasoning_engine_name`, `service_account_email`, `artifact_bucket`

## §V INVARIANTS
V1: terraform-sole-source — Agent Platform resources exist only as Terraform-managed; console create banned
V2: python-deferred — this spec §T not include Python/ADK/pickle/requirements
V3: one-agent-one-store — exactly 1 `google_vertex_ai_reasoning_engine`; Memory Bank via `spec.context_spec.memory_bank_config` on that engine
V4: engine-identity — engine runs as dedicated SA w/ `roles/aiplatform.user` + `roles/storage.objectViewer`; not user ADC
V5: apis-via-tf — `aiplatform.googleapis.com` enabled via `google_project_service` before engine
V6: no-idle-nodes — not provision Vector Search ANN serving or always-on prediction endpoints
V7: apply-without-agent-source — `terraform apply` succeeds w/o `package_spec` / pickle; source attach later spec
V8: outputs-addressable — apply emits reasoning engine resource name, SA email, artifact bucket
V9: state-not-committed — tfstate not committed; `.gitignore` covers `.terraform/` `*.tfstate` `*.tfstate.backup`

## §T TASKS
id|status|task|cites
T1|.|init `terraform/` root: versions, google provider pin, vars `project` `region`|I.tf
T2|.|enable `aiplatform.googleapis.com` via `google_project_service`|V5,I.api
T3|.|add dedicated engine SA + `roles/aiplatform.user` + `roles/storage.objectViewer`|V4,I.sa
T4|.|add GCS artifact bucket for later package_spec|V7,I.gcs
T5|.|add `google_vertex_ai_reasoning_engine` w/ Memory Bank `context_spec`; no `package_spec`|V1,V3,V7,I.resource
T6|.|emit outputs `reasoning_engine_name` `service_account_email` `artifact_bucket`|V8,I.out
T7|.|extend `.gitignore` for `.terraform/` `*.tfstate` `*.tfstate.backup`|V9
T8|.|`terraform fmt` + `terraform validate` pass|T1,T2,T3,T4,T5,T6

## §B BUGS
id|date|cause|fix
