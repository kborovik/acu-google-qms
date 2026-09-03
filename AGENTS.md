# AGENTS.md

## Repository Guide for AI Coding Agents & Automated Systems

This document provides operational instructions, development workflows, master data references, and **CLI usage examples** for AI agents and developers working within the **GCP Acumatica CoA Ingestion Platform**.

---

## 1. System Architecture Overview

The repository is structured into five distinct operational domains:

* **`agent/`**: Cloud-native Reasoning Engine built on the Google Agent Development Kit (ADK) for Python 3.14.
* **`acumatica/`**: ERP integration specifications, REST API schemas, and master data catalogs (`vendors.json`, `products.json`, `test_labs.json`, `qms_inspection_plans.json`).
* **`domain/`**: Business domain documentation, regulatory specifications (**Health Canada GMP GUI-0001/0158**, **CFIA SFCR**, **USP/Ph. Eur.**), company profiles, and synthetic samples.
* **`docgen/`**: Dedicated vector-grade PDF generator CLI built with `click` and `reportlab` to synthesize the 3 mandatory dock shipping documents (CoA, Packing Slip, BOL).
* **`terraform/`**: Infrastructure as Code (IaC) provisioning GCP Vertex AI Reasoning Engine, Memory Bank, IAM, and Secret Manager across dev and prod environments.

---

## 2. Environment & Tooling Standards

* **Language Runtime:** Python `>=3.14`
* **Package Manager:** `uv` (`pyproject.toml` and `uv.lock` are source of truth; do **not** generate `requirements.txt`).
* **Linting & Formatting:** `ruff`
* **Static Type Checking:** `basedpyright` in strict mode (`typeCheckingMode = "strict"`).
* **Infrastructure:** `terraform` (Google & Google-Beta providers).

### Core Verification Commands
```bash
# Run code linting and formatting checks
uv run ruff check
uv run ruff format --check

# Run strict type checking (must maintain 0 errors/warnings)
uv run basedpyright

# Format and validate Terraform configurations
terraform fmt -recursive terraform
terraform -chdir=terraform validate
```

---

## 3. CLI Usage Examples & Tooling Instructions

### 3.1 Inbound Shipping Document PDF Generator (`docgen`)

The `docgen` CLI generates pixel-perfect PDF shipping suites matching Health Canada GMP, CFIA, and Acumatica ERP dock receiving requirements.

#### Command Reference & Syntax

```bash
# Display help and available subcommands
uv run python -m docgen --help
# Or using the console script entry point:
uv run docgen --help
```

#### 1. Inspect Master Data
View registered qualified vendors, accredited testing laboratories, and raw material catalog items:
```bash
uv run python -m docgen list-master-data
```

#### 2. Generate Complete 3-Document Receiving Suite
Generates a synchronized **Certificate of Analysis (CoA)**, **Supplier Packing Slip**, **Bill of Lading (BOL)**, and **Manifest JSON** for a given inventory item:
```bash
# Generate in-spec (PASS) receiving suite
uv run python -m docgen generate-suite \
  --inventory-id RAW-ECH-EXT4 \
  --outdir ./output/shipping_docs

# Generate out-of-spec (FAIL) receiving suite for quarantine & NCR testing
uv run python -m docgen generate-suite \
  --inventory-id RAW-ASH-EXT5 \
  --status fail \
  --outdir ./output/shipping_docs_failed

# Generate suite directly from an Acumatica Purchase Order JSON payload
uv run python -m docgen from-po \
  --po-json ./path/to/po_order.json \
  --status pass \
  --outdir ./output/po_shipping_docs

# Or via generate-suite with optional --po-json:
uv run python -m docgen generate-suite \
  --po-json ./path/to/po_order.json \
  --status pass \
  --outdir ./output/po_shipping_docs
```

#### 3. Generate Standalone Documents
Generate individual PDF documents for targeted testing:
```bash
# Generate standalone Certificate of Analysis (CoA)
uv run python -m docgen generate-coa \
  --inventory-id RAW-CURC-95 \
  --status pass \
  --outdir ./output/coa

# Generate standalone Supplier Packing Slip
uv run python -m docgen generate-packing-slip \
  --inventory-id RAW-OMEGA3-70 \
  --outdir ./output/packing_slips

# Generate standalone Carrier Bill of Lading (BOL)
uv run python -m docgen generate-bol \
  --inventory-id RAW-THEA-98 \
  --outdir ./output/bol
```

#### 4. Generate Multi-Vendor Batch
Synthesize a batch of document suites spanning the 5 vendor and laboratory standards:
```bash
# Generate 5 suites with alternating pass/fail outcomes
uv run python -m docgen batch \
  --count 5 \
  --include-failures \
  --outdir ./output/batch_shipping_docs

# Generate 10 all-passing suites
uv run python -m docgen batch \
  --count 10 \
  --all-pass \
  --outdir ./output/batch_all_pass
```

---

### 3.2 Synthetic Data & Demo Generators (`domain/samples/`)

```bash
# Generate synthetic JSON CoA payloads across 5 vendor/lab configurations
uv run python domain/samples/generate_demo_documents.py \
  --count 5 \
  --include-failures \
  --outdir domain/samples/generated_test_batch

# Generate standalone reference PDF sample
uv run python domain/samples/generate_pdf_sample.py
```

---

### 3.3 Terraform Infrastructure Deployment

```bash
# Initialize Terraform
terraform -chdir=terraform init

# Plan / Apply against Development environment
terraform -chdir=terraform plan -var-file=lab5-acucoa-dev1.tfvars
terraform -chdir=terraform apply -var-file=lab5-acucoa-dev1.tfvars

# Plan / Apply against Production environment
terraform -chdir=terraform plan -var-file=lab5-acucoa-prd1.tfvars
terraform -chdir=terraform apply -var-file=lab5-acucoa-prd1.tfvars
```

---

## 4. Key Master Data & Specifications Reference

| Resource | Path | Description |
| :--- | :--- | :--- |
| **Vendors Master Data** | `acumatica/master_data/vendors.json` | 5 qualified global raw material suppliers. |
| **Products Master Data** | `acumatica/master_data/products.json` | 10 botanical, probiotic, API, and marine lipid raw materials. |
| **Testing Labs Master Data** | `acumatica/master_data/test_labs.json` | 5 accredited testing laboratories with document standards & SI conversion maps. |
| **QMS Inspection Plans** | `acumatica/master_data/qms_inspection_plans.json` | Acumatica quality plans, test limits, methods, and criticality levels. |
| **Shipping Documents Spec** | `domain/MANDATORY_SHIPPING_DOCUMENTS_SPEC.md` | Inbound dock compliance, 3-way reconciliation (CoA, Packing Slip, BOL). |
| **CoA Ingestion Spec** | `domain/COA_INGESTION_SPEC.md` | Multimodal AI parsing, unit conversions, and ERP release workflows. |
| **Acumatica Matrix** | `acumatica/acumatica_integration_matrix.md` | REST API endpoints, entity mapping, and state machine transitions. |
| **DocGen Specification** | `docgen/SPEC.md` | SDD specification for the CLI document generator. |

---

## 5. Development Conventions for Agents

1. **Strict Type Safety:** Always write full type annotations in Python code. Run `uv run basedpyright` to guarantee 0 errors.
2. **Deterministic Master Data:** Never hardcode vendor or product IDs; resolve identifiers against `acumatica/master_data/`.
3. **Audit Trail Provenance:** Keep the 3-way link (`POReceipt.ReceiptNbr` $\leftrightarrow$ `POReceiptLineSplit.LotSerialNbr` $\leftrightarrow$ `QMSInspectionOrder`) consistent across generated payloads and PDFs.
4. **SDD Specification Fidelity:** When adding new capabilities or modifying schemas, ensure corresponding `SPEC.md` documents are kept up to date.
