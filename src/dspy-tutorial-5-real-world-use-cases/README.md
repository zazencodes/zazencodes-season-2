# DSPy Tutorial — Master 5 Real‑World Use Cases

This repository accompanies the blog‑style tutorial **“DSPy Tutorial — Master 5 Real‑World Use Cases”**.
Each Python script here maps to a stage in the learning path; run them in order or open them in a Jupyter notebook.

> **Tip:** Every script is self‑contained and keeps external calls to a minimum, so you can experiment without a large bill.
> For production workloads you’ll likely replace the tiny demo datasets with your own corpora and validation sets.

---

## Quick Start

```bash
# 1. Python ≥ 3.9
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Set your OpenAI key
echo "OPENAI_API_KEY=sk-..." > .env

# 3. Run the first example
python 01_structured_output.py
```

`dspy-ai` will default to the inexpensive **gpt-4o-mini**; change the model in each script if you wish.

---

## Repository Layout

| File | Stage | Real‑World Scenario | Key DSPy Concepts |
|------|-------|--------------------|-------------------|
| `01_structured_output.py` | 1 | Extract fields from customer‑support emails | `dspy.Signature`, `dspy.Predict` |
| `02_chain_of_thought.py` | 2 | Explain risk decisions for loan applications | `dspy.ChainOfThought` |
| `03_rag_hr_bot.py` | 3 | HR & IT handbook Q&A (RAG) | `dspy.Retrieve`, pipeline composition |
| `04_react_expense_assistant.py` | 4 | Expense assistant with tools (ReAct) | `dspy.ReAct`, `dspy.Tool` |
| `05_self_improving_rag.py` | 5 | Optimise the Stage 3 bot | `dspy.MIPROv2` optimiser |

---

## Docs links

We sprinkle inline links like:

```python
# DOCS: https://github.com/stanfordnlp/dspy?tab=readme-ov-file#signatures
```

so you can jump directly from code to the relevant reference.

Have fun — and **happy declarative prompting!**
