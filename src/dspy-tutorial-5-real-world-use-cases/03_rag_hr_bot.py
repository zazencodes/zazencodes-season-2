"""
03_rag_hr_bot.py
Stage 3 – Retrieval‑Augmented Generation (RAG)

Ask questions about your company handbook stored in memory.
This demo uses a tiny in‑memory knowledge base; swap in your own vector store for production.
"""

import os, dspy, textwrap
from dotenv import load_dotenv
load_dotenv()

dspy.settings.configure(
    lm=dspy.OpenAI(model="gpt-4o-mini"),
    cache="sqlite",
    temperature=0.2,
)

# ---------------------------------------------------------------------------
# Build a *very* small docstore so the example is self‑contained.
docs = {
    "pto": "Employees accrue 1.5 days of paid time off (PTO) per month, for a total of 18 days per year.",
    "laptop": "New hires choose between a MacBook Pro and a Dell XPS. IT covers standard warranty.",
    "expense_policy": "Meals under $75 do not require itemised receipts. Alcohol is not reimbursable.",
}

# Simple retrieval function — replace with dspy.ColBERTv2 for real datasets
def simple_search(query: str, k: int = 2):
    # naïve keyword match
    ranked = sorted(docs.items(), key=lambda kv: -sum(q in kv[1].lower() for q in query.lower().split()))
    return [textwrap.shorten(txt, 120) for _, txt in ranked[:k]]

# Wrap retrieval as a DSPy tool
retrieve = dspy.Tool(simple_search, name="HandbookSearch")

class HRBot(dspy.Module):
    """RAG pipeline: retrieve snippets then answer with reasoning."""

    def __init__(self, k: int = 2):
        super().__init__()
        self.k = k
        self.answer = dspy.ChainOfThought("question, context -> answer")

    def forward(self, question: str):
        context = retrieve(question, k=self.k)
        return self.answer(question=question, context=context)

qa_bot = HRBot()

def main():
    q = "How many PTO days do we get per year?"
    pred = qa_bot(question=q)
    print("Q:", q)
    print("\nA:", pred.answer)
    print("\nReasoning:\n", pred.reasoning)

if __name__ == "__main__":
    main()
