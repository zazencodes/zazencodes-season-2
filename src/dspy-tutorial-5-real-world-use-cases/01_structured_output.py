"""
Structured Output Extraction

Turn messy support emails into structured JSON tickets.

Run:
    python 01_structured_output.py
"""

from typing import Literal

import dspy
from dotenv import load_dotenv

# Load OPENAI_API_KEY
load_dotenv()

# Configure DSPy
lm = dspy.LM("openai/gpt-5-nano", temperature=1, max_tokens=20000)
dspy.settings.configure(lm=lm)


# ---- Define the task signature -----------------------------------------
class SupportEmail(dspy.Signature):
    email: str = dspy.InputField()
    subject: str = dspy.OutputField(desc="Subject line of the email")
    priority: Literal["low", "medium", "high"] = dspy.OutputField()
    product: str = dspy.OutputField(
        desc="The product(s) referenced. Output an empty string if unknown."
    )
    negative_sentiment: bool = dspy.OutputField(desc="True/False")


# ---- Instantiate a Predict module --------------------------------------
extract_ticket = dspy.Predict(SupportEmail)

# ---- Demo --------------------------------------------------------------
sample_emails = [
    """
    Subject: Screen cracked after one week!

    Hi team,
    I purchased the AlphaTab 11 tablet last Monday and the glass already shattered.
    I’m extremely disappointed and need a replacement ASAP.
    Best,
    Carla
    """,
    """
    Subject: Subscription renewal question

    Hello,
    My CloudSync Pro plan renewed today and I’d like to switch to monthly billing.
    Could you advise?
    Thanks,
    Raj
    """,
    """
    Subject: Your #1 fan

    Loving your alpha tabs. How can I buy more?

    xoxo JEFF
    """,
]


def main() -> None:
    for raw in sample_emails:
        pred = extract_ticket(email=raw.strip())
        print("\n--- Structured Ticket ---")
        print(pred)
    print("\n--- DSPy History ---")
    print(dspy.inspect_history())


if __name__ == "__main__":
    main()
