"""
Chain‑of‑Thought Reasoning

A financial‑risk checker that explains *why* it approved or rejected an application.
"""

from typing import Literal

import dspy
from dotenv import load_dotenv

load_dotenv(override=True)

lm = dspy.LM("openai/gpt-5-mini", temperature=1, max_tokens=20000)
dspy.settings.configure(lm=lm)


class LoanRisk(dspy.Signature):
    applicant_profile: str = dspy.InputField()
    loan_risk: Literal["low", "medium", "high"] = dspy.OutputField()
    approved: bool = dspy.OutputField(desc="approve this person for a loan?")


# risk_checker = dspy.ChainOfThought(
#     "applicant_profile: str, age: int, is_male: bool -> loan_risk"
# )
risk_checker = dspy.ChainOfThought(LoanRisk)

sample_profile = """Name: Jane Diaz
Credit score: 612
Annual income: $84k
Existing debt: $55k
Requested amount: $25k
Loan purpose: consolidate credit cards
"""


def main():
    pred = risk_checker(applicant_profile=sample_profile, age=28, is_male="NO")

    print("\n--- DSPy History ---")
    print(dspy.inspect_history())

    print("\n--- Prediction ---")
    print(pred)


if __name__ == "__main__":
    main()
