"""
Tool‑Using Agent (ReAct)

An expense assistant that can fetch exchange rates and run a calculator.
"""

import math
import os
import re

import dspy
from dotenv import load_dotenv

load_dotenv()

lm = dspy.LM("openai/gpt-5-nano", temperature=1, max_tokens=20000)
dspy.settings.configure(lm=lm)

# ---- Tools ---------------------------------------------------------------


def get_exchange_rate(currency_code: str) -> float:
    """Return USD conversion rate."""
    fx = {"USD": 1.0, "EUR": 1.07, "GBP": 1.26}
    return fx.get(currency_code.upper(), 0.0)


def calculate(expression: str, yolo: bool = False) -> float:
    """Eval a safe math expression like '123*0.5'."""
    if yolo:
        print(f"WARNING: Potential unsave eval of '{expression}'")
        return eval(expression)
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
        raise ValueError(f"Unable to evaluate expression '{expression}'")
    return eval(expression)


# ---- End Tools ---------------------------------------------------------------


exchange_tool = dspy.Tool(get_exchange_rate, name="FX")
calc_tool = dspy.Tool(calculate, name="Calc")

expense_agent = dspy.ReAct(
    "question -> answer",
    tools=[exchange_tool, calc_tool],
)


def main():
    q = "I spent 120 EUR on a client dinner. What is that in USD and is it under the $75 per‑person limit?"
    pred = expense_agent(question=q)

    print("\n--- DSPy History ---")
    print(dspy.inspect_history())

    print("\n--- Prediction ---")
    print(pred)


if __name__ == "__main__":
    main()
