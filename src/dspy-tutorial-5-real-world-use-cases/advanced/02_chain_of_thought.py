"""
02_chain_of_thought.py
Stage 2 – Chain‑of‑Thought Reasoning

A financial‑risk checker that explains *why* it approved or rejected an application.

Learning Objectives:
- Understand how dspy.ChainOfThought enables step-by-step reasoning
- Learn to compare Predict vs ChainOfThought for complex tasks
- Practice evaluation and optimization with financial domain constraints
- See how reasoning transparency improves trust in AI decisions

DOCS: https://github.com/stanfordnlp/dspy?tab=readme-ov-file#chainofthought
"""

import os, dspy, logging, statistics
from typing import List, Dict, Tuple
from dotenv import load_dotenv
from dataclasses import dataclass

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

dspy.settings.configure(
    lm=dspy.OpenAI(model="gpt-4o-mini"),
    cache="sqlite",
    temperature=0.2,  # Balanced for consistent yet nuanced reasoning
)

# ---- Domain Context: Financial Risk Assessment ----------------------------
@dataclass
class LoanApplication:
    """Structure for loan application data."""
    name: str
    credit_score: int
    annual_income: int
    existing_debt: int
    requested_amount: int
    loan_purpose: str
    employment_years: float
    debt_to_income_ratio: float = None
    
    def __post_init__(self):
        if self.debt_to_income_ratio is None:
            self.debt_to_income_ratio = round(self.existing_debt / self.annual_income, 3)

# ---- Signature with enhanced reasoning ------------------------------------
class LoanRisk(dspy.Signature):
    """Assess loan default risk with detailed step-by-step reasoning."""
    
    applicant_profile: str = dspy.InputField(desc="Complete applicant financial profile")
    decision: str = dspy.OutputField(desc="approve, reject, or conditional - final recommendation")
    rationale: str = dspy.OutputField(desc="detailed step‑by‑step risk assessment reasoning")
    confidence: float = dspy.OutputField(desc="confidence in decision (0.0-1.0)")
    risk_factors: str = dspy.OutputField(desc="specific risk factors identified")

# ---- Module comparison: Predict vs ChainOfThought ------------------------
basic_risk_checker = dspy.Predict(LoanRisk)
reasoning_risk_checker = dspy.ChainOfThought(LoanRisk)

# ---- Evaluation and validation functions ----------------------------------
def evaluate_decision_quality(application: LoanApplication, prediction) -> Dict:
    """Evaluate the quality of a loan decision using financial domain rules."""
    evaluation = {
        "decision_appropriate": False,
        "reasoning_quality": 0.0,
        "regulatory_compliant": True,
        "issues": []
    }
    
    # Domain-specific validation rules
    dti_ratio = application.debt_to_income_ratio
    
    # High-risk indicators that should lead to rejection
    high_risk_conditions = [
        application.credit_score < 580,
        dti_ratio > 0.5,  # Debt-to-income > 50%
        application.employment_years < 1.0,
        application.requested_amount > application.annual_income * 5
    ]
    
    # Low-risk indicators that should lead to approval
    low_risk_conditions = [
        application.credit_score > 750,
        dti_ratio < 0.3,
        application.employment_years > 3.0,
        application.requested_amount < application.annual_income * 2
    ]
    
    # Evaluate decision appropriateness
    num_high_risk = sum(high_risk_conditions)
    num_low_risk = sum(low_risk_conditions)
    
    if prediction.decision == "reject" and num_high_risk >= 2:
        evaluation["decision_appropriate"] = True
    elif prediction.decision == "approve" and num_low_risk >= 3:
        evaluation["decision_appropriate"] = True
    elif prediction.decision == "conditional" and 1 <= num_high_risk <= 1:
        evaluation["decision_appropriate"] = True
    else:
        evaluation["issues"].append(f"Decision inconsistent with risk profile")
    
    # Evaluate reasoning quality
    reasoning_text = prediction.rationale.lower()
    quality_indicators = [
        "credit score" in reasoning_text,
        "debt" in reasoning_text or "income" in reasoning_text,
        "employment" in reasoning_text,
        "risk" in reasoning_text,
        len(prediction.rationale.split()) > 30  # Sufficient detail
    ]
    evaluation["reasoning_quality"] = sum(quality_indicators) / len(quality_indicators)
    
    # Check for regulatory compliance (simplified)
    protected_terms = ["race", "gender", "religion", "nationality"]
    if any(term in reasoning_text for term in protected_terms):
        evaluation["regulatory_compliant"] = False
        evaluation["issues"].append("Potential discriminatory reasoning")
    
    return evaluation

def create_applicant_profile(app: LoanApplication) -> str:
    """Format application data for the model."""
    return f"""Name: {app.name}
Credit score: {app.credit_score}
Annual income: ${app.annual_income:,}
Existing debt: ${app.existing_debt:,}
Requested amount: ${app.requested_amount:,}
Loan purpose: {app.loan_purpose}
Employment history: {app.employment_years} years
Debt-to-income ratio: {app.debt_to_income_ratio:.1%}"""

# ---- Sample loan applications with diverse risk profiles ------------------
sample_applications = [
    # Original example (medium risk)
    LoanApplication(
        name="Jane Diaz",
        credit_score=612,
        annual_income=84000,
        existing_debt=55000,
        requested_amount=25000,
        loan_purpose="consolidate credit cards",
        employment_years=2.5
    ),
    
    # High-risk applicant
    LoanApplication(
        name="Mike Johnson",
        credit_score=545,
        annual_income=35000,
        existing_debt=28000,
        requested_amount=45000,
        loan_purpose="business investment",
        employment_years=0.8
    ),
    
    # Low-risk applicant
    LoanApplication(
        name="Sarah Chen",
        credit_score=785,
        annual_income=120000,
        existing_debt=25000,
        requested_amount=30000,
        loan_purpose="home improvement",
        employment_years=5.2
    ),
    
    # Edge case: high income but poor credit
    LoanApplication(
        name="Robert Wilson",
        credit_score=520,
        annual_income=150000,
        existing_debt=95000,
        requested_amount=20000,
        loan_purpose="debt consolidation",
        employment_years=8.0
    ),
    
    # Edge case: excellent credit but high debt
    LoanApplication(
        name="Lisa Garcia",
        credit_score=820,
        annual_income=75000,
        existing_debt=65000,
        requested_amount=15000,
        loan_purpose="medical expenses",
        employment_years=3.5
    )
]

def compare_approaches(applications: List[LoanApplication]) -> Dict:
    """Compare basic prediction vs chain-of-thought reasoning."""
    results = {
        "basic": {"decisions": [], "evaluations": [], "total_time": 0},
        "reasoning": {"decisions": [], "evaluations": [], "total_time": 0}
    }
    
    print("\n=== Comparing Basic Prediction vs Chain-of-Thought ===\n")
    
    for i, app in enumerate(applications):
        profile = create_applicant_profile(app)
        print(f"--- Application {i+1}: {app.name} ---")
        print(f"Risk Profile: Credit {app.credit_score}, DTI {app.debt_to_income_ratio:.1%}")
        
        # Basic prediction
        try:
            basic_pred = basic_risk_checker(applicant_profile=profile)
            basic_eval = evaluate_decision_quality(app, basic_pred)
            
            results["basic"]["decisions"].append(basic_pred.decision)
            results["basic"]["evaluations"].append(basic_eval)
            
            print(f"Basic Decision: {basic_pred.decision}")
            print(f"Basic Reasoning: {basic_pred.rationale[:100]}...")
            
        except Exception as e:
            logger.error(f"Basic prediction failed: {e}")
        
        # Chain-of-thought prediction
        try:
            reasoning_pred = reasoning_risk_checker(applicant_profile=profile)
            reasoning_eval = evaluate_decision_quality(app, reasoning_pred)
            
            results["reasoning"]["decisions"].append(reasoning_pred.decision)
            results["reasoning"]["evaluations"].append(reasoning_eval)
            
            print(f"CoT Decision: {reasoning_pred.decision}")
            print(f"CoT Reasoning Quality: {reasoning_eval['reasoning_quality']:.2f}")
            print(f"Decision Appropriate: {'✓' if reasoning_eval['decision_appropriate'] else '✗'}")
            
            if reasoning_eval["issues"]:
                print(f"Issues: {', '.join(reasoning_eval['issues'])}")
                
        except Exception as e:
            logger.error(f"Chain-of-thought prediction failed: {e}")
        
        print()
    
    return results

def analyze_results(results: Dict) -> None:
    """Analyze and compare the performance of both approaches."""
    print("\n=== Performance Analysis ===")
    
    # Calculate metrics for both approaches
    for approach_name, data in results.items():
        if not data["evaluations"]:
            continue
            
        appropriate_decisions = sum(1 for eval in data["evaluations"] if eval["decision_appropriate"])
        avg_reasoning_quality = statistics.mean(eval["reasoning_quality"] for eval in data["evaluations"])
        compliance_rate = sum(1 for eval in data["evaluations"] if eval["regulatory_compliant"]) / len(data["evaluations"])
        
        print(f"\n{approach_name.title()} Approach:")
        print(f"  Appropriate Decisions: {appropriate_decisions}/{len(data['evaluations'])} ({appropriate_decisions/len(data['evaluations']):.1%})")
        print(f"  Avg Reasoning Quality: {avg_reasoning_quality:.2f}")
        print(f"  Regulatory Compliance: {compliance_rate:.1%}")
        print(f"  Decision Distribution: {dict(zip(*map(list, zip(*[(d, data['decisions'].count(d)) for d in set(data['decisions'])]))))}")

def demonstrate_optimization() -> None:
    """Demonstrate how to optimize the chain-of-thought reasoning."""
    print("\n=== Optimization Demo ===")
    print("Note: In production, you would use dspy.BootstrapFewShot or dspy.MIPROv2")
    print("with labeled training data to automatically improve reasoning quality.")
    
    # Create training examples (in practice, these would be expert-labeled)
    training_examples = [
        {
            "input": create_applicant_profile(sample_applications[0]),
            "expected_decision": "conditional",
            "reasoning_requirements": ["credit score analysis", "debt-to-income calculation", "employment stability"]
        }
    ]
    
    print(f"Training examples available: {len(training_examples)}")
    print("Optimization would improve:")
    print("- Consistency of reasoning steps")
    print("- Domain-specific terminology usage")
    print("- Decision accuracy")
    print("- Regulatory compliance")

def main():
    """Main function demonstrating chain-of-thought reasoning."""
    print("=== DSPy Chain-of-Thought Demo: Loan Risk Assessment ===\n")
    print("This demo shows how Chain-of-Thought reasoning improves decision transparency")
    print("and quality in financial risk assessment scenarios.\n")
    
    # Show detailed reasoning for one example
    app = sample_applications[0]  # Jane Diaz - medium risk case
    profile = create_applicant_profile(app)
    
    print("--- Detailed Chain-of-Thought Example ---")
    print(f"Applicant: {app.name}")
    print(f"Profile:\n{profile}\n")
    
    pred = reasoning_risk_checker(applicant_profile=profile)
    evaluation = evaluate_decision_quality(app, pred)
    
    print(f"Decision: {pred.decision}")
    print(f"Confidence: {pred.confidence}")
    print(f"\nDetailed Reasoning:")
    print(pred.rationale)
    print(f"\nRisk Factors Identified:")
    print(pred.risk_factors)
    
    print(f"\n--- Evaluation ---")
    print(f"Decision Appropriate: {'✓' if evaluation['decision_appropriate'] else '✗'}")
    print(f"Reasoning Quality: {evaluation['reasoning_quality']:.2f}/1.0")
    print(f"Regulatory Compliant: {'✓' if evaluation['regulatory_compliant'] else '✗'}")
    
    if evaluation["issues"]:
        print(f"Issues Found: {', '.join(evaluation['issues'])}")
    
    # Compare approaches across multiple applications
    results = compare_approaches(sample_applications)
    analyze_results(results)
    
    # Show optimization potential
    demonstrate_optimization()
    
    print("\n--- Key Takeaways ---")
    print("1. Chain-of-Thought provides transparent, step-by-step reasoning")
    print("2. Reasoning quality can be measured and optimized")
    print("3. Domain expertise can be incorporated into evaluation")
    print("4. DSPy optimizers can automatically improve reasoning consistency")

if __name__ == "__main__":
    main()
