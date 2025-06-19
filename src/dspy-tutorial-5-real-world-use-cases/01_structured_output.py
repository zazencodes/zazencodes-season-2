"""
01_structured_output.py
Stage 1 – Structured Output Extraction

Turn messy support emails into structured JSON tickets.

Run:
    python 01_structured_output.py
"""

# DOCS: https://github.com/stanfordnlp/dspy?tab=readme-ov-file#signatures
import os, dspy
from dotenv import load_dotenv

load_dotenv()  # loads OPENAI_API_KEY

# Configure DSPy once (you can reuse across scripts)
dspy.settings.configure(
    lm=dspy.OpenAI(model="gpt-4o-mini"),   # DOCS: https://github.com/stanfordnlp/dspy?tab=readme-ov-file#lms
    cache="sqlite",                        # persistent cache so re‑runs are free
    temperature=0.2,
)

# ---- 1. Define the task signature -----------------------------------------
class SupportEmail(dspy.Signature):
    email: str = dspy.InputField()
    priority: str = dspy.OutputField(desc="low, medium, high")
    product: str = dspy.OutputField()
    sentiment: str = dspy.OutputField(desc="positive, neutral, negative")

# ---- 2. Instantiate a Predict module --------------------------------------
extract_ticket = dspy.Predict(SupportEmail)   # DOCS: https://github.com/stanfordnlp/dspy?tab=readme-ov-file#predict

# ---- 3. Demo --------------------------------------------------------------
sample_emails = [
    """
    Subject: Screen cracked after one week!

    Hi team,
    I purchased the **AlphaTab 11** tablet last Monday and the glass already shattered.
    I’m extremely disappointed and need a replacement ASAP.
    Best,
    Carla
    """,
    """
    Subject: Subscription renewal question

    Hello,
    My **CloudSync Pro** plan renewed today and I’d like to switch to monthly billing.
    Could you advise?
    Thanks,
    Raj
    """
]

def main() -> None:
    for raw in sample_emails:
        pred = extract_ticket(email=raw.strip())
        print("\n--- Structured Ticket ---")
        print(pred.to_json(indent=2))

if __name__ == "__main__":
    main()
