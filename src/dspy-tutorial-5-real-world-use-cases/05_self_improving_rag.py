"""
Self-Improving Pipeline

Optimise a RAG bot with 5 QA examples.

This illustrates DSPy.MIPROv2 and uses a proper embeddings-based retriever
(backed by a free Hugging Face model) to match the earlier RAG demo.
"""

import dspy
from dotenv import load_dotenv

load_dotenv(override=True)

lm = dspy.LM("openai/gpt-4o")
dspy.settings.configure(lm=lm)

corpus: list[str] = [
    "Employee Handbook (excerpt, v1.0). Purpose & scope: This handbook sets expectations for all employees, contractors, and interns. It is guidance, not a contract; where law or a collective bargaining agreement differs, that source controls. Updates may be issued; the latest version lives in the Knowledge Base. Questions? Email HR at hr@company.example. Our values: put customers first, act with integrity, default to transparency, and support one another. By working here you agree to follow the policies summarized below and detailed later.",
    "By working here you agree to follow the policies summarized below and detailed later. Equal Employment Opportunity: We prohibit discrimination and harassment on any protected basis, and we provide reasonable accommodations for disability, pregnancy, religion, and caregiving. Report concerns to your manager, HR, or ethics@company.example; anonymous hotline is available. Retaliation is strictly prohibited. Accessibility: we invest in tools, facilities, and remote workflows to ensure everyone can do their best work. Safer workplace & anti-harassment defined.",
    "Safer workplace & anti-harassment defined. Harassment includes unwelcome conduct (verbal, visual, physical) that creates a hostile environment. Sexual harassment includes quid pro quo and hostile environment conduct. If you experience or witness issues, document facts and report promptly; HR will investigate impartially and maintain confidentiality to the extent possible. Code of Conduct: be respectful, assume positive intent, give and seek feedback, and escalate issues constructively. Employment classifications and timekeeping appear below.",
    "Employment classifications and timekeeping appear below. Status categories: full-time, part-time, temporary, intern, and contractor. Exempt vs. non-exempt status is determined by role and law. Payroll is biweekly on Fridays; timesheets are due Mondays by 10:00 a.m. local. Overtime for non-exempt roles is 1.5x after 40 hours/week (or as local law requires) and must be pre-approved. Breaks: at least a 15-minute rest per 4 hours and a 30-minute meal near the fifth hour, where required. Attendance, punctuality, and timezone norms follow.",
    "Attendance, punctuality, and timezone norms follow. Work hours: standard 9:00–17:30 with a 1-hour meal period; core collaboration hours are 10:00–16:00 local. Flexible schedules require manager approval and must overlap core hours. Remote/hybrid: keep a safe, ergonomic workspace; first-year home-office stipend $500; annual ergonomic assessment recommended. Communication norms: use #announcements-readme for company posts, #help-it for support; respond to direct requests within 1 business day; enable Do Not Disturb outside core hours; meetings ≤50 minutes with notes posted.",
    "Meetings ≤50 minutes with notes posted. Performance & growth: leveling framework L1–L7 with role competencies published internally. Annual review cycle occurs in Q1; midyear check-ins focus on goals and development. Promotions require demonstrated impact, scope, and a calibrated panel review; business need matters. Learning: $1,000/year stipend for courses, books, and certifications; conference travel needs manager approval and budget confirmation. Compliance training is auto-assigned with due dates; complete modules before deadlines to remain in good standing.",
    "Complete modules before deadlines to remain in good standing. Compensation & payroll: salaries align to market bands which are visible internally; equity grants may apply per offer letter and plan documents. Payroll is via direct deposit; bonus plans pay with regular payroll when applicable. Benefits: medical, dental, and vision begin the first of the month following your start date; the company pays 80% of premiums for employees and 60% for dependents. Retirement (401(k)/RRSP): company match up to 4% of eligible pay with immediate vesting and low-fee index options.",
    "Company match up to 4% of eligible pay with immediate vesting and low-fee index options. Time off & leaves: Employees accrue 1.5 days of paid time off (PTO) per month, for a total of 18 days per year. Accrual starts on your hire date; you may carry over up to 5 days into the next year; negative balances need manager approval. Holidays are posted on the company calendar. Sick time is separate per local law. Parental leave provides 16 paid weeks for birth, adoption, or foster placement. Bereavement up to 5 days; jury duty paid; unpaid personal leave by approval.",
    "Unpaid personal leave by approval. Equipment & security: New hires choose between a MacBook Pro and a Dell XPS. IT covers standard warranty and manages provisioning. Devices are company property and must use full-disk encryption, auto-update, and company MDM. Multifactor authentication is required for accounts. Store work only in approved cloud drives; personal cloud sync is not allowed for company files. Report loss or theft within 24 hours to security@company.example. Travel with laptops in privacy-screen mode; software and SaaS purchases go through procurement review.",
    "Software and SaaS purchases go through procurement review. Expense & travel policy: Spend company money as if it were your own. Meals under $75 do not require itemized receipts; alcohol is not reimbursable. Book economy airfare for trips under 6 hours; purchase 14+ days in advance. Hotels: standard room within posted city caps; prefer negotiated rates in the travel portal. Local transport: rideshare or public transit; rent compact cars unless equipment requires larger. Submit expenses within 30 days; reimbursement occurs within 10 business days after approval.",
    "Reimbursement occurs within 10 business days after approval. Information governance: classify data (Public, Internal, Confidential, Restricted); share on a need-to-know basis; never email Restricted data unencrypted. Privacy: handle personal data per policy and law; report incidents immediately. Social media: be kind, be clear, no confidential info, and add “opinions my own.” Conflicts of interest must be disclosed. Disciplinary steps may include coaching, warnings, or termination. Offboarding includes return of assets and deprovisioning. See full handbook for details.",
]

# ---- Generate embeddings with SentenceTransformers --------------------
from sentence_transformers import SentenceTransformer

st_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
embedder = dspy.Embedder(st_model.encode, batch_size=64)  # callable encoder

# Build an embeddings retriever
search = dspy.retrievers.Embeddings(
    corpus=corpus,
    embedder=embedder,
    k=3,  # top-k snippets
)


class HRAnswer(dspy.Signature):
    """Answer HR questions using retrieved context, with step-by-step reasoning."""

    question: str = dspy.InputField()
    context: str = dspy.InputField(desc="relevant handbook snippets")
    answer: str = dspy.OutputField()


class MiniHR(dspy.Module):
    def __init__(self):
        self.answer = dspy.ChainOfThought(HRAnswer)

    def forward(self, question: str):
        ctx_passages = search(question).passages
        context = "\n\n".join(f"- {p}" for p in ctx_passages)
        return self.answer(question=question, context=context)


rag_bot = MiniHR()

# ---------------- Eval set --------------------
raw_eval = [
    ("How many PTO days do we get each year?", "18"),
    ("Do I need an itemised receipt for a $50 team lunch?", "No"),
    ("Is beer reimbursable?", "No"),
    ("What laptop models can new hires choose?", "MacBook Pro and Dell XPS"),
]
devset = [
    dspy.Example(question=q, answer=a).with_inputs("question") for q, a in raw_eval
]


# Metric
def exact_match(example: dspy.Example, pred: dspy.Prediction, trace=None) -> int:
    return int(pred.answer.strip().lower() == example.answer.strip().lower())


# Helper to run & print a small report
def evaluate_bot(
    bot: MiniHR,
    dataset: list[dspy.Example],
    title: str,
) -> tuple[int, list[tuple[str, str, str, int]]]:
    print(f"\n=== {title} ===")
    correct = 0
    rows = []
    for ex in dataset:
        pred = bot(question=ex.question)
        ok = exact_match(ex, pred)
        correct += ok
        rows.append((ex.question, pred.answer, ex.answer, ok))
        print(
            f"- Q: {ex.question}\n  → Pred: {pred.answer} | Gold: {ex.answer} | {'✔️' if ok else '✖️'}"
        )
    print(f"Accuracy: {correct} / {len(dataset)}")
    return correct, rows


# ---- Optimiser -------------------------------------------------------------
optimizer = dspy.MIPROv2(metric=exact_match, auto="light", verbose=True)


def main():
    evaluate_bot(rag_bot, devset, "Baseline")

    print("Compiling optimised bot")
    optimised_bot = optimizer.compile(rag_bot, trainset=devset, valset=devset)

    evaluate_bot(optimised_bot, devset, "Optimized")

    print("\n--- DSPy History ---")
    print(dspy.inspect_history())


if __name__ == "__main__":
    main()
