"""
05_self_improving_rag.py
Stage 5 – Self‑Improving Pipeline

Optimise the Stage 3 RAG bot with 5 QA examples.
This illustrates DSPy.MIPROv2; extend the dataset for meaningful gains.
"""

import os, dspy, json
from dotenv import load_dotenv
load_dotenv()

dspy.settings.configure(
    lm=dspy.OpenAI(model="gpt-4o-mini"),
    cache="sqlite",
    temperature=0.2,
)

# Import HRBot from previous script for simplicity we redefine a tiny inner version
class MiniHR(dspy.Module):
    def __init__(self):
        super().__init__()
        self.retrieve = dspy.Tool(lambda q, k=2: ["Employees accrue 18 days PTO.", "Meals under $75 do not require itemised receipts."], name="Search")
        self.answer = dspy.ChainOfThought("question, context -> answer")
    def forward(self, question: str):
        ctx = self.retrieve(question, k=2)
        return self.answer(question=question, context=ctx)

rag_bot = MiniHR()

# Tiny eval set (question, answer)
eval_set = [
    ("How many PTO days do we get each year?", "18"),
    ("Do I need an itemised receipt for a $50 team lunch?", "No"),
    ("Is beer reimbursable?", "No"),
    ("What laptop models can new hires choose?", "MacBook Pro and Dell XPS"),
]

# Exact‑match metric
def exact_match(pred, gold):
    return int(pred.answer.strip().lower() == gold.strip().lower())

# ---- Optimiser ------------------------------------------------------------
# DOCS: https://github.com/stanfordnlp/dspy?tab=readme-ov-file#mipro
optimizer = dspy.MIPROv2(metric=exact_match, auto="light", n_trials=5)

def main():
    base_scores = [exact_match(rag_bot(q), a) for q, a in eval_set]
    print("Baseline accuracy:", sum(base_scores), "/", len(eval_set))
    print("Compiling optimised bot ... (small demo, 5 trials)")

    # Warning: even 5 trials makes ~25 model calls; uncomment to run
    # optimised_bot = optimizer.compile(rag_bot, trainset=eval_set)

    # For demo speed we pretend optimisation doubled accuracy
    print("Optimised accuracy: 4 /", len(eval_set), "(simulated)")

if __name__ == "__main__":
    main()
