"""
04_react_expense_assistant.py
Stage 4 – Tool‑Using Agent (ReAct)

An expense assistant that can fetch exchange rates, calculate amounts, and validate expense policies.

Learning Objectives:
- Understand dspy.ReAct for building tool-using agents
- Learn safe tool design and error handling
- Practice multi-turn conversations with memory
- See real-world agent patterns for business automation

DOCS: https://github.com/stanfordnlp/dspy?tab=readme-ov-file#react
"""

import os, dspy, logging, json, re, ast, operator
from typing import Dict, List, Any, Optional
from decimal import Decimal, InvalidOperation
from datetime import datetime, date
from dotenv import load_dotenv
from dataclasses import dataclass, asdict

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

dspy.settings.configure(
    lm=dspy.OpenAI(model="gpt-4o-mini"),
    cache="sqlite",
    temperature=0.3,  # Balanced for reasoning but consistent tool usage
)

# ---- Enhanced Expense Management Tools ------------------------------------

@dataclass
class ExpensePolicy:
    """Company expense policy structure."""
    meal_receipt_threshold: float = 75.0
    alcohol_reimbursable: bool = False
    max_daily_meal_allowance: float = 150.0
    per_person_meal_limit: float = 100.0
    uber_receipt_threshold: float = 25.0
    conference_limit_per_year: int = 1
    learning_budget_per_year: float = 2000.0

@dataclass
class ExpenseItem:
    """Structure for individual expense items."""
    amount: float
    currency: str
    category: str
    description: str
    date: str = None
    requires_receipt: bool = False
    policy_compliant: bool = True
    notes: str = ""

# Company expense policy (loaded from configuration)
COMPANY_POLICY = ExpensePolicy()

# Updated exchange rates (in practice, these would come from an API)
EXCHANGE_RATES = {
    "USD": 1.0,
    "EUR": 1.07,
    "GBP": 1.26,
    "CAD": 0.74,
    "JPY": 0.0067,
    "AUD": 0.66,
    "CHF": 1.09
}

class SafeCalculator:
    """Safe mathematical expression evaluator."""
    
    ALLOWED_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    
    @classmethod
    def evaluate(cls, expression: str) -> float:
        """Safely evaluate a mathematical expression."""
        try:
            # Remove whitespace and validate characters
            expression = expression.strip()
            if not re.match(r'^[0-9+\-*/(). ]+$', expression):
                raise ValueError("Expression contains invalid characters")
            
            # Parse and evaluate
            tree = ast.parse(expression, mode='eval')
            result = cls._eval_node(tree.body)
            
            # Ensure result is reasonable for expense calculations
            if not isinstance(result, (int, float)):
                raise ValueError("Result is not a number")
            
            if abs(result) > 1_000_000:  # Sanity check
                raise ValueError("Result too large")
                
            return float(result)
            
        except Exception as e:
            raise ValueError(f"Calculation error: {str(e)}")
    
    @classmethod
    def _eval_node(cls, node):
        """Recursively evaluate AST nodes."""
        if isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.Num):  # Python < 3.8
            return node.n
        elif isinstance(node, ast.BinOp):
            left = cls._eval_node(node.left)
            right = cls._eval_node(node.right)
            operator_func = cls.ALLOWED_OPERATORS.get(type(node.op))
            if operator_func is None:
                raise ValueError(f"Unsupported operator: {type(node.op)}")
            return operator_func(left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = cls._eval_node(node.operand)
            operator_func = cls.ALLOWED_OPERATORS.get(type(node.op))
            if operator_func is None:
                raise ValueError(f"Unsupported unary operator: {type(node.op)}")
            return operator_func(operand)
        else:
            raise ValueError(f"Unsupported node type: {type(node)}")

# ---- Tool Functions -------------------------------------------------------

def get_exchange_rate(from_currency: str, to_currency: str = "USD") -> str:
    """Get exchange rate between two currencies."""
    try:
        from_currency = from_currency.upper().strip()
        to_currency = to_currency.upper().strip()
        
        if from_currency not in EXCHANGE_RATES:
            return f"Error: Currency {from_currency} not supported. Available: {', '.join(EXCHANGE_RATES.keys())}"
        
        if to_currency not in EXCHANGE_RATES:
            return f"Error: Currency {to_currency} not supported. Available: {', '.join(EXCHANGE_RATES.keys())}"
        
        if from_currency == to_currency:
            return f"1.0 (same currency)"
        
        # Convert via USD
        from_rate = EXCHANGE_RATES[from_currency]
        to_rate = EXCHANGE_RATES[to_currency]
        rate = to_rate / from_rate
        
        return f"{rate:.4f} ({from_currency} to {to_currency})"
        
    except Exception as e:
        return f"Error getting exchange rate: {str(e)}"

def calculate_amount(expression: str) -> str:
    """Safely calculate a mathematical expression."""
    try:
        result = SafeCalculator.evaluate(expression)
        return f"{result:.2f}"
    except Exception as e:
        return f"Calculation error: {str(e)}"

def convert_currency(amount: float, from_currency: str, to_currency: str = "USD") -> str:
    """Convert an amount from one currency to another."""
    try:
        amount = float(amount)
        rate_response = get_exchange_rate(from_currency, to_currency)
        
        if "Error" in rate_response:
            return rate_response
        
        # Extract rate from response
        rate = float(rate_response.split()[0])
        converted = amount * rate
        
        return f"{converted:.2f} {to_currency.upper()}"
        
    except Exception as e:
        return f"Currency conversion error: {str(e)}"

def check_expense_policy(category: str, amount: float, currency: str = "USD", 
                        attendees: int = 1, description: str = "") -> str:
    """Check if an expense complies with company policy."""
    try:
        # Convert to USD if needed
        if currency.upper() != "USD":
            usd_amount_str = convert_currency(amount, currency, "USD")
            if "error" in usd_amount_str.lower():
                return usd_amount_str
            usd_amount = float(usd_amount_str.split()[0])
        else:
            usd_amount = amount
        
        policy = COMPANY_POLICY
        category = category.lower()
        description = description.lower()
        
        compliance_issues = []
        requirements = []
        
        # Check meal expenses
        if "meal" in category or "food" in category or "restaurant" in category:
            per_person = usd_amount / attendees if attendees > 0 else usd_amount
            
            if usd_amount >= policy.meal_receipt_threshold:
                requirements.append(f"Receipt required (expense ${usd_amount:.2f} >= ${policy.meal_receipt_threshold})")
            
            if per_person > policy.per_person_meal_limit:
                compliance_issues.append(f"Per-person amount ${per_person:.2f} exceeds limit ${policy.per_person_meal_limit}")
            
            if "alcohol" in description and not policy.alcohol_reimbursable:
                compliance_issues.append("Alcohol not reimbursable under company policy")
        
        # Check travel expenses
        elif "travel" in category or "uber" in category or "taxi" in category:
            if usd_amount >= policy.uber_receipt_threshold:
                requirements.append(f"Receipt required (ride ${usd_amount:.2f} >= ${policy.uber_receipt_threshold})")
        
        # Check training/conference expenses
        elif "training" in category or "conference" in category or "learning" in category:
            if usd_amount > policy.learning_budget_per_year:
                compliance_issues.append(f"Amount ${usd_amount:.2f} exceeds annual budget ${policy.learning_budget_per_year}")
            if usd_amount > 500:
                requirements.append("Manager approval required for training over $500")
        
        # Build response
        result = {
            "compliant": len(compliance_issues) == 0,
            "usd_amount": usd_amount,
            "issues": compliance_issues,
            "requirements": requirements
        }
        
        if result["compliant"]:
            response = f"✅ Expense compliant (${usd_amount:.2f} USD)"
        else:
            response = f"❌ Policy violations found"
        
        if requirements:
            response += f"\nRequirements: {'; '.join(requirements)}"
        
        if compliance_issues:
            response += f"\nIssues: {'; '.join(compliance_issues)}"
        
        return response
        
    except Exception as e:
        return f"Policy check error: {str(e)}"

def get_expense_summary(expenses_json: str) -> str:
    """Analyze a list of expenses and provide summary statistics."""
    try:
        expenses = json.loads(expenses_json)
        if not isinstance(expenses, list):
            return "Error: Expected a JSON list of expenses"
        
        total_usd = 0.0
        by_category = {}
        policy_violations = 0
        receipt_required = 0
        
        for expense in expenses:
            # Convert to USD
            amount = expense.get("amount", 0)
            currency = expense.get("currency", "USD")
            category = expense.get("category", "other")
            
            if currency != "USD":
                usd_str = convert_currency(amount, currency, "USD")
                if "error" in usd_str.lower():
                    continue
                usd_amount = float(usd_str.split()[0])
            else:
                usd_amount = amount
            
            total_usd += usd_amount
            by_category[category] = by_category.get(category, 0) + usd_amount
            
            # Check policy compliance
            policy_result = check_expense_policy(category, amount, currency, 
                                               expense.get("attendees", 1),
                                               expense.get("description", ""))
            
            if "❌" in policy_result:
                policy_violations += 1
            if "Receipt required" in policy_result:
                receipt_required += 1
        
        summary = f"💰 Total: ${total_usd:.2f} USD\n"
        summary += f"📋 Categories: {len(by_category)}\n"
        
        for cat, amount in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
            summary += f"  • {cat}: ${amount:.2f}\n"
        
        summary += f"⚠️  Policy violations: {policy_violations}\n"
        summary += f"🧾 Receipts required: {receipt_required}"
        
        return summary
        
    except json.JSONDecodeError:
        return "Error: Invalid JSON format"
    except Exception as e:
        return f"Summary error: {str(e)}"

# ---- Create DSPy Tools ----------------------------------------------------
# Modern DSPy tools are created using dspy.Tool wrapper
exchange_tool = dspy.Tool(get_exchange_rate, name="ExchangeRate", 
                         desc="Get exchange rate between currencies")
calc_tool = dspy.Tool(calculate_amount, name="Calculator", 
                     desc="Safely calculate mathematical expressions")
convert_tool = dspy.Tool(convert_currency, name="CurrencyConverter", 
                        desc="Convert amount between currencies")
policy_tool = dspy.Tool(check_expense_policy, name="PolicyChecker", 
                       desc="Check expense against company policy")
summary_tool = dspy.Tool(get_expense_summary, name="ExpenseSummary", 
                        desc="Analyze and summarize multiple expenses")

# ---- Enhanced ReAct Agent ------------------------------------------------
class ExpenseAssistant(dspy.Module):
    """Advanced expense assistant with memory and context awareness."""
    
    def __init__(self):
        super().__init__()
        
        # Enhanced signature for business context
        signature = """
        question, conversation_history -> answer
        
        You are a helpful expense management assistant. You can:
        - Calculate currency conversions and mathematical expressions
        - Check expense policy compliance
        - Provide expense summaries and analysis
        - Answer questions about company policies
        
        Always be clear about policy requirements and potential issues.
        Use tools when needed for calculations and policy checks.
        """
        
        self.react = dspy.ReAct(
            signature,
            tools=[exchange_tool, calc_tool, convert_tool, policy_tool, summary_tool],
            max_turns=10  # Allow for complex multi-step reasoning
        )
        
        # Conversation memory
        self.conversation_history = []
    
    def forward(self, question: str) -> dspy.Prediction:
        # Format conversation history
        history_text = ""
        if self.conversation_history:
            recent_history = self.conversation_history[-3:]  # Keep last 3 exchanges
            history_text = "\n".join([f"Q: {h['question']}\nA: {h['answer']}" 
                                    for h in recent_history])
        
        # Get response
        response = self.react(question=question, conversation_history=history_text)
        
        # Store in memory
        self.conversation_history.append({
            "question": question,
            "answer": response.answer,
            "timestamp": datetime.now().isoformat()
        })
        
        return response
    
    def reset_conversation(self):
        """Reset conversation memory."""
        self.conversation_history = []

# ---- Demo Scenarios -------------------------------------------------------
demo_scenarios = [
    {
        "title": "Currency Conversion with Policy Check",
        "question": "I spent 120 EUR on a client dinner for 3 people. What is that in USD and is it compliant with our meal policy?",
        "expected_tools": ["CurrencyConverter", "PolicyChecker"]
    },
    {
        "title": "Multi-step Expense Calculation",
        "question": "I need to split a 250 USD restaurant bill between 4 people. What's each person's share, and do we need receipts?",
        "expected_tools": ["Calculator", "PolicyChecker"]
    },
    {
        "title": "Complex Expense Analysis",
        "question": "Can you check this expense report: [{'amount': 45, 'currency': 'USD', 'category': 'meal', 'attendees': 2}, {'amount': 80, 'currency': 'EUR', 'category': 'training', 'description': 'online course'}]",
        "expected_tools": ["ExpenseSummary"]
    },
    {
        "title": "Policy Guidance",
        "question": "What are the rules for alcohol reimbursement and meal receipt requirements?",
        "expected_tools": []  # No tools needed, general policy question
    },
    {
        "title": "Multi-turn Conversation",
        "questions": [
            "I went to a conference that cost 850 USD. Is this within policy?",
            "What if I had manager approval beforehand?",
            "How much of my annual learning budget would this use up?"
        ]
    }
]

def run_demo_scenario(assistant: ExpenseAssistant, scenario: Dict) -> None:
    """Run a single demo scenario."""
    print(f"\n--- {scenario['title']} ---")
    
    if 'questions' in scenario:  # Multi-turn scenario
        for i, question in enumerate(scenario['questions'], 1):
            print(f"\nTurn {i}: {question}")
            response = assistant(question=question)
            print(f"Assistant: {response.answer}")
    else:  # Single question scenario
        question = scenario['question']
        print(f"Question: {question}")
        
        response = assistant(question=question)
        print(f"Assistant: {response.answer}")
        
        # Verify expected tools were used (if specified)
        if 'expected_tools' in scenario and hasattr(response, 'tool_calls'):
            tools_used = [call.get('tool_name', '') for call in response.tool_calls]
            expected = scenario['expected_tools']
            if expected:
                tools_found = any(tool in str(tools_used) for tool in expected)
                print(f"Tools verification: {'✓' if tools_found else '✗'} "
                      f"(Expected: {expected})")

def demonstrate_error_handling(assistant: ExpenseAssistant) -> None:
    """Demonstrate error handling and edge cases."""
    print("\n=== Error Handling Demonstration ===")
    
    error_cases = [
        "Calculate 100 / 0",  # Division by zero
        "Convert 50 INVALID_CURRENCY to USD",  # Invalid currency
        "What's the policy for FAKE_CATEGORY expenses?",  # Invalid category
        "Calculate 2 ** 100",  # Very large number
    ]
    
    for case in error_cases:
        print(f"\nError Test: {case}")
        try:
            response = assistant(question=case)
            print(f"Response: {response.answer}")
        except Exception as e:
            print(f"Exception caught: {e}")

def main():
    """Main function demonstrating the enhanced expense assistant."""
    print("=== DSPy ReAct Expense Assistant (Enhanced) ===\n")
    print("This demo shows an improved ReAct agent with:")
    print("- Safe mathematical expression parser (no eval())")
    print("- Comprehensive expense policy engine")
    print("- Multi-turn conversation memory")
    print("- Robust error handling and validation")
    print("- Real-world business tools and scenarios")
    print("- Tool usage verification and monitoring")
    print()
    
    # Initialize assistant
    assistant = ExpenseAssistant()
    
    # Run demo scenarios
    for scenario in demo_scenarios:
        run_demo_scenario(assistant, scenario)
        
        # Reset conversation for next scenario (except multi-turn)
        if 'questions' not in scenario:
            assistant.reset_conversation()
    
    # Demonstrate error handling
    demonstrate_error_handling(assistant)
    
    # Show conversation memory
    print("\n=== Conversation Memory Example ===")
    assistant.reset_conversation()
    
    # Build up context
    assistant(question="I had a business meal that cost 95 USD for 2 people")
    assistant(question="Do I need a receipt for that?")
    response = assistant(question="What was the per-person cost again?")
    
    print(f"Final response with context: {response.answer}")
    print(f"Conversation history length: {len(assistant.conversation_history)}")
    
    print("\n--- Key Improvements Made ---")
    print("1. ✅ Safe mathematical expression parser (no eval())")
    print("2. ✅ Comprehensive expense policy engine")
    print("3. ✅ Multi-turn conversation memory")
    print("4. ✅ Robust error handling and validation")
    print("5. ✅ Real-world business tools and scenarios")
    print("6. ✅ Tool usage verification and monitoring")
    
    print("\n--- Production Considerations ---")
    print("• Exchange rates should come from live API (e.g., fixer.io)")
    print("• Expense policies should be loaded from company database")
    print("• Add authentication and audit logging")
    print("• Implement rate limiting and cost controls")
    print("• Add integration with expense management systems")

if __name__ == "__main__":
    main()
