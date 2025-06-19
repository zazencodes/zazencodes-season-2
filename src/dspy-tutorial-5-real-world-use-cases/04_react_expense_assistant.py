"""
04_react_expense_assistant.py
Stage 4 – Tool‑Using Agent (ReAct)

An expense assistant that can fetch exchange rates and run a calculator.
"""

import os, dspy, math, re
from dotenv import load_dotenv
load_dotenv()

dspy.settings.configure(
    lm=dspy.OpenAI(model="gpt-4o-mini"),
    cache="sqlite",
    temperature=0.2,
)

# ---- Tools ---------------------------------------------------------------
FX = {"USD": 1.0, "EUR": 1.07, "GBP": 1.26}

def get_exchange_rate(currency_code: str) -> float:
    """Return USD conversion rate."""
    return FX.get(currency_code.upper(), 0.0)

def calculate(expression: str) -> float:
    """Eval a safe math expression like '123*0.5'."""
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
        raise ValueError("Unsafe expression")
    return eval(expression)

exchange_tool = dspy.Tool(get_exchange_rate, name="FX")
calc_tool = dspy.Tool(calculate, name="Calc")

# DOCS: https://github.com/stanfordnlp/dspy?tab=readme-ov-file#react
expense_agent = dspy.ReAct(
    "question -> answer",
    tools=[exchange_tool, calc_tool],
    max_turns=8,
)

def main():
    q = "I spent 120 EUR on a client dinner. What is that in USD and is it under the $75 per‑person limit?"
    pred = expense_agent(question=q)
    print("Q:", q)
    print("\nA:", pred.answer)

if __name__ == "__main__":
    main()
