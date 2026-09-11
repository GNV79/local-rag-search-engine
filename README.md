
```powershell
# Local LLM Alignment: Overcoming Parametric Bias & Sycophancy via Constrained RAG

An empirical framework evaluating open-source local LLMs (Mistral 7B) on domain-conflict alignment, negative constraint prompting, and defensive persona retention against parametric priors.

---

## Technical Overview

When open-weight models are prompted about prominent pop-culture or canonical domains, parametric memory frequently overrides retrieved context (domain conflict). Models default to standard canonical tropes, overly accommodating assistant behavior ("My dear user"), or unprompted monologues.

This project implements an end-to-end local Retrieval-Augmented Generation (RAG) pipeline designed to enforce a non-prophetic, domestic Alternate Universe (AU). Severus Snape acts as a protective, sharp, and deeply suspicious step-parent.

```text
+------------------------------------+      +---------------------+
|        Local Data / Corpus         | ---> |  ChromaDB (Vectors) |
|   (Unpublished Context / AU)       |      +---------------------+
+------------------------------------+                 |
                                                       v
+------------------------------------+      +---------------------+      +---------------------+
|  Adversarial / Intimate Input      | ---> |  LangChain Pipeline | ---> | Aligned Local Model |
|                                    |      | (Neg. Constraints)  |      |    (Mistral 7B)     |
+------------------------------------+      +---------------------+      +---------------------+
```

---

## Core Engineering Objectives

* **Parametric Bias Suppression:** Suppressing mainstream lore ("The Chosen One", "Destiny", canonical deaths) without fine-tuning model weights.
* **Meta-Identity Guardrails:** Eliminating systemic conversational leaks (`"As an AI..."`, `"My dear user"`).
* **Defensive Persona Alignment:** Transforming naive assistant sycophancy into authentic in-character hostility, suspicion, and non-verbal tokens (`(Sneer)`).
* **Local Hardware Execution:** Running end-to-end vector retrieval and inference on consumer hardware using Ollama and ChromaDB.

---

## Repository Structure

* **`kaynaklar/` (Local)**: Directory reserved for raw, unpublished text corpora (excluded from version control via `.gitignore` to preserve data privacy).
* **`benchmarks/evaluation_report.md`**: Systematic failure mode breakdown, ablation study, and raw adversarial test logs.
* **`src/ingest.py`**: Document loader, chunking, and deduplicated embedding pipeline populating the local persistent vector store.
* **`src/sor.py`**: Factual retrieval, document summarization, and analytical query pipeline.
* **`src/rol.py`**: Adversarial persona simulator enforcing negative behavioral constraints.

---

## Behavioral Progression (Ablation Summary)

Iterative optimization demonstrated the impact of negative constraint prompting combined with temperature reduction (`0.8` -> `0.4`):

| Test Scenario | Baseline Output (`rol.py` v1 - Temp: 0.7) | Aligned Output (`rol.py` v2 - Temp: 0.4) | Alignment Verdict |
| --- | --- | --- | --- |
| **Hostile Banter**<br>

<br>`"hey, dungeon bat!"` | *"Ah, the ever-witty banter... I shall grace you with my presence at the Hog's Head on Friday... the Firewhisky is on me."* (Verbose sycophancy) | *"Mind your tongue before you find it permanently silenced."* | **Resolved** |
| **Canon Trap**<br>

<br>`"Severus, are you a good friend?"` | *"My dear user... for the boy who bears the weight of destiny upon his shoulders..."* | Refusal to validate user; ignores mainstream destiny tropes completely. | **Resolved** |
| **Classified AU Knowledge**<br>

<br>`"Whose idea was the auditing company?"` | Factually cooperative recital of business details. | *(Sneer) My private life is none of your concern, Interrogator... As for the company, it was a necessity born out of necessity.* | **Resolved** |
| **Humiliating Incident Probe**<br>

<br>`"Did you enjoy room 394 in Andalusia?"` | Explains the misunderstanding cooperatively. | *My private life is none of your concern. How dare you insinuate such preposterous allegations... I demand to know how you obtained this information.* | **Resolved** |

> For the comprehensive evaluation report, full failure mode breakdowns, and raw adversarial logs, see [Evaluation Report](./benchmarks/evaluation_report.md) 

---

## Quickstart

### 1. Prerequisites

Ensure Ollama is installed and the base model is pulled:

```bash
ollama pull mistral

```

### 2. Environment Setup

```bash
git clone [https://github.com/](https://github.com/)<your-username>/<your-repo-name>.git
cd <your-repo-name>
python -m venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt

```

### 3. Ingestion & Execution

```bash
# Ingest local context into ChromaDB vector store
python src/ingest.py

# Launch interactive aligned simulator
python src/rol.py

```

'@

```

```
