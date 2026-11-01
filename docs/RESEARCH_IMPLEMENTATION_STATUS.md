# CodeMind: implementation and evidence audit

**Audit date:** 1 November 2026  
**Repository audited:** https://github.com/shashankakgec/CodeMind  
**Upstream research-team repository:** https://github.com/vivek3770/CodeMind  
**Scope:** Source inspection only. This is not a penetration test or complete runtime evaluation.

## Executive summary

The repository contains a full-stack React/Vite/Monaco frontend and FastAPI/Python backend. Source modules exist for AI review, classifier inference, review-history retrieval, embedding-based code indexing, code execution, code tracing, and complexity analysis.

A module's presence does not prove end-to-end operation, local hosting, project isolation, offline operation, or security. The paper also uses a separate, reduced minimal Python API prototype for its four unit tests and API smoke checks. Results from that reduced prototype must not be attributed to this full-stack repository.

## Findings verified by source inspection

| Area | Source evidence | Accurate description |
|---|---|---|
| LLM | backend/services/llm.py calls Gemini 2.5 Flash | Cloud-assisted LLM integration, not local inference. |
| Classifier | backend/services/bug_classifier.py calls Hugging Face Inference API | Remote inference path, not local CodeBERT inference. |
| Classifier metrics | get_metrics() returned hardcoded accuracy 0.7083 and macro-F1 0.4146 | Not calculated by the status endpoint; must not be reported as verified evaluation results. This branch removes these misleading values from runtime status. |
| Review memory | backend/services/rag_pipeline.py retrieves exact code-hash matches and recent same-language reviews | Exact/recent-review context; not project-isolated neural RAG. |
| Semantic index | backend/services/code_indexer.py stores embeddings in a JSON index and may use local SentenceTransformers or remote Hugging Face | Embedding-based search source exists; metadata does not establish project-level access isolation. |
| Docker execution | backend/services/code_executor.py uses a read-only bind mount for /code, network_mode=none, non-root user, CPU/memory limits and timeout | Restricted Docker execution source exists. Container root filesystem is not set read-only; no independent hardening/escape/egress tests were supplied. |
| Cloud execution fallback | Executor calls OnlineCompiler.io when Docker is unavailable | Submitted code may be sent to an external service; this path is not offline. |
| License | No LICENSE file was found in the inspected repository tree | Do not claim MIT licensing until a license file is added and approved by project owners. |

## Critical risks and required fixes

### P0 — Do not claim a security sandbox yet
- Docker invocation does not set a read-only container root filesystem.
- No evidence was supplied for dropped Linux capabilities, no-new-privileges, restrictive seccomp/AppArmor, process-count limits, or packet-capture/egress tests.
- OnlineCompiler.io fallback is a remote execution service from a privacy/offline perspective.
- Until hardening and tests are completed on an isolated disposable host, describe the executor as restricted execution code, not a secure sandbox.

### P0 — Keep cloud and strict-offline modes separate
- Gemini, Hugging Face Inference API, and OnlineCompiler.io are remote services.
- A deployment using any of these services must not be described as strict-offline.
- Strict-offline operation requires explicit provider disabling, local model/embedding endpoints, and network-boundary tests.

### P1 — Project isolation and access control
- Review-history retrieval is based on code hash and language, not a project identifier.
- The JSON vector index stores filename/language metadata without a project membership boundary.
- API review-history endpoints were not found to have an authentication boundary during source inspection.
- Before multi-user/client deployment, implement authenticated project ownership, per-project retrieval filters, authorization checks on every read/write/delete endpoint, and cross-project access tests.

### P1 — Classifier metric reporting
- Runtime status previously returned fixed accuracy and macro-F1 constants.
- This branch changes status metrics to null and explicitly reports that benchmark metrics are unavailable from runtime status.
- Publish metrics only when supported by archived raw predictions, a documented dataset version, split manifest, and reproducible evaluation script.

### P2 — Model and dataset reproducibility
- Verify the hosted model's label mapping, revision, training-data provenance, and evaluation protocol.
- Do not assume labels declared in application code match the model's exported label configuration.
- Group train/validation/test splits by commit/project to reduce leakage; report class balance and duplicate filtering.

## Research-paper evidence boundary

The paper may accurately state:
1. The research team maintains this full-stack repository and identify its major technologies and source modules.
2. A separate minimal API prototype was functionally checked with four automated unit tests and controlled API smoke checks, if the accompanying test logs are retained.
3. Current evidence does not establish Devign benchmark performance, CodeBERT training performance, neural RAG quality, usability, strict-offline operation, or Docker security.

The paper should not:
- attribute minimal-prototype tests to this full-stack repository;
- call the Hugging Face inference path a local CodeBERT model;
- call review-memory retrieval project-scoped neural RAG;
- claim OnlineCompiler fallback is offline;
- claim a secure sandbox based only on Docker resource/network options;
- report hardcoded service-status metrics as experimental results.

## Validation checklist

- [ ] Run backend tests from a clean environment and archive logs.
- [ ] Run frontend build and browser smoke tests.
- [ ] Verify classifier label mapping against the exact hosted model revision.
- [ ] Run Devign/CodeBERT training and held-out evaluation; archive raw predictions and split manifests.
- [ ] Evaluate RAG relevance and cross-project isolation with labelled queries.
- [ ] Implement and test authenticated project-level authorization.
- [ ] Harden Docker execution on an isolated disposable host; capture configuration and packet traces.
- [ ] Add a confirmed license file only after research-team owners approve the license.
- [ ] Keep README and paper wording synchronized with measured evidence.
