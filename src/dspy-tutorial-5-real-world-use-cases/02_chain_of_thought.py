"""
02_chain_of_thought.py
Stage 2 – Chain‑of‑Thought Reasoning

A financial‑risk checker that explains *why* it approved or rejected an application.
"""

import os, dspy
from dotenv import load_dotenv
load_dotenv()

dspy.settings.configure(
    lm=dspy.OpenAI(model="gpt-4o-mini"),
    cache="sqlite",
    temperature=0.2,
)

# ---- Signature with rationale field ---------------------------------------
class LoanRisk(dspy.Signature):
    applicant_profile: str = dspy.InputField()
    decision: str = dspy.OutputField(desc="approve or reject")
    rationale: str = dspy.OutputField(desc="step‑by‑step reasoning")

# DOCS: https://github.com/stanfordnlp/dspy?tab=readme-ov-file#chainofthought
risk_checker = dspy.ChainOfThought(LoanRisk)

sample_profile = """Name: Jane Diaz
Credit score: 612
Annual income: $84k
Existing debt: $55k
Requested amount: $25k
Loan purpose: consolidate credit cards
"""

def main():
    pred = risk_checker(applicant_profile=sample_profile)
    print("\nDecision:", pred.decision)
    print("\nRationale:\n", pred.rationale)

if __name__ == "__main__":
    main()
