"""
01_structured_output.py
Stage 1 – Structured Output Extraction

Turn messy support emails into structured JSON tickets.

Learning Objectives:
- Understand DSPy Signatures for defining input/output interfaces
- Learn how to use dspy.Predict for basic LLM tasks
- See how to extract structured data from unstructured text
- Practice handling real-world data variations and edge cases

Run:
    python 01_structured_output.py
"""

# DOCS: https://github.com/stanfordnlp/dspy?tab=readme-ov-file#signatures
import os, dspy, json, logging
from typing import Literal, Optional
from dotenv import load_dotenv

# Set up logging for better debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()  # loads OPENAI_API_KEY

# Configure DSPy once (you can reuse across scripts)
dspy.settings.configure(
    lm=dspy.OpenAI(model="gpt-4o-mini"),   # DOCS: https://github.com/stanfordnlp/dspy?tab=readme-ov-file#lms
    cache="sqlite",                        # persistent cache so re‑runs are free
    temperature=0.1,                       # Lower temperature for more consistent structured outputs
)

# ---- 1. Define the task signature with proper validation -----------------
class SupportEmail(dspy.Signature):
    """Extract structured ticket information from customer support emails."""
    
    email: str = dspy.InputField(desc="Raw customer support email text")
    priority: Literal["low", "medium", "high", "urgent"] = dspy.OutputField(
        desc="Ticket priority based on urgency indicators, customer tier, and issue severity"
    )
    product: str = dspy.OutputField(
        desc="Product or service mentioned in the email (e.g., 'AlphaTab 11', 'CloudSync Pro')"
    )
    sentiment: Literal["positive", "neutral", "negative", "frustrated"] = dspy.OutputField(
        desc="Customer sentiment detected from tone and language"
    )
    category: str = dspy.OutputField(
        desc="Issue category (e.g., 'hardware_defect', 'billing_inquiry', 'feature_request')"
    )
    confidence: float = dspy.OutputField(
        desc="Confidence score (0.0-1.0) for the extraction accuracy"
    )

# ---- 2. Instantiate a Predict module --------------------------------------
extract_ticket = dspy.Predict(SupportEmail)   # DOCS: https://github.com/stanfordnlp/dspy?tab=readme-ov-file#predict

# ---- 3. Validation functions ----------------------------------------------
def validate_extraction(prediction) -> bool:
    """Validate the extracted ticket information for consistency."""
    try:
        # Check confidence is in valid range
        if not (0.0 <= prediction.confidence <= 1.0):
            logger.warning(f"Invalid confidence score: {prediction.confidence}")
            return False
        
        # Check for required fields
        if not prediction.product.strip():
            logger.warning("Missing product information")
            return False
            
        # Validate priority-sentiment consistency
        if prediction.priority == "urgent" and prediction.sentiment == "positive":
            logger.warning("Inconsistent priority-sentiment combination")
            return False
            
        return True
    except Exception as e:
        logger.error(f"Validation error: {e}")
        return False

def enhance_with_business_rules(prediction, email_text: str):
    """Apply business rules to enhance the extraction."""
    # Upgrade priority for VIP customers
    if "VIP" in email_text or "premium" in email_text.lower():
        if prediction.priority == "low":
            prediction.priority = "medium"
        elif prediction.priority == "medium":
            prediction.priority = "high"
    
    # Security issues get automatic high priority
    if any(keyword in email_text.lower() for keyword in ["security", "breach", "hack", "fraud"]):
        prediction.priority = "urgent"
        prediction.category = "security_incident"
    
    return prediction

# ---- 4. Expanded demo with realistic examples -----------------------------
sample_emails = [
    # Original examples enhanced
    """
    Subject: Screen cracked after one week! [VIP Customer]

    Hi team,
    I purchased the **AlphaTab 11** tablet last Monday and the glass already shattered.
    I'm extremely disappointed and need a replacement ASAP. I've been a premium customer
    for 3 years and this is unacceptable quality.
    
    Order #: AT-2024-001234
    Customer ID: VIP-789
    
    Best,
    Carla Morrison
    """,
    
    """
    Subject: Subscription renewal question

    Hello,
    My **CloudSync Pro** plan renewed today and I'd like to switch to monthly billing.
    Could you advise on the process? No rush on this.
    
    Thanks,
    Raj Patel
    """,
    
    # New realistic examples
    """
    Subject: URGENT: Cannot access account - possible security breach
    
    I cannot log into my CloudSync account and received suspicious emails about 
    password changes I didn't make. This might be a security issue.
    
    Please help immediately.
    
    Mike Chen
    """,
    
    """
    Subject: Feature request for AlphaTab Pro
    
    Hi there!
    
    Love the new AlphaTab Pro! Would it be possible to add dark mode support?
    Many users in our community have been asking for this.
    
    Keep up the great work!
    Sarah Kim
    """,
    
    """
    Subject: Billing error - charged twice
    
    I was charged twice for my CloudSync subscription this month ($29.99 x 2).
    One charge on the 1st and another on the 15th. Please refund the duplicate charge.
    
    Account: sarah.davis@company.com
    
    Sarah Davis
    """,
    
    # Edge case: unclear email
    """
    Subject: help
    
    thing not working
    """,
]

def process_email_safely(email_text: str, index: int) -> Optional[dict]:
    """Process a single email with error handling."""
    try:
        logger.info(f"Processing email {index + 1}")
        
        # Extract structured information
        pred = extract_ticket(email=email_text.strip())
        
        # Validate the extraction
        if not validate_extraction(pred):
            logger.warning(f"Validation failed for email {index + 1}")
            # Still return the result but flag it
            pred.confidence = max(0.0, pred.confidence - 0.3)  # Reduce confidence
        
        # Apply business rules
        pred = enhance_with_business_rules(pred, email_text)
        
        # Return structured result
        return {
            "email_id": index + 1,
            "original_length": len(email_text),
            "extraction": {
                "priority": pred.priority,
                "product": pred.product,
                "sentiment": pred.sentiment,
                "category": pred.category,
                "confidence": round(pred.confidence, 2)
            },
            "validation_passed": validate_extraction(pred)
        }
        
    except Exception as e:
        logger.error(f"Error processing email {index + 1}: {e}")
        return {
            "email_id": index + 1,
            "error": str(e),
            "extraction": None
        }

def main() -> None:
    """Main function demonstrating structured output extraction."""
    print("=== DSPy Structured Output Extraction Demo ===\n")
    print("This demo shows how to extract structured information from support emails.")
    print("Key concepts: Signatures, InputField/OutputField, validation, business rules\n")
    
    results = []
    
    for i, email in enumerate(sample_emails):
        print(f"\n--- Processing Email {i + 1} ---")
        print(f"Subject: {email.split('Subject:')[1].split('\n')[0].strip() if 'Subject:' in email else 'No subject'}")
        
        result = process_email_safely(email, i)
        results.append(result)
        
        if result and "extraction" in result and result["extraction"]:
            extraction = result["extraction"]
            print(f"Priority: {extraction['priority']}")
            print(f"Product: {extraction['product']}")
            print(f"Sentiment: {extraction['sentiment']}")
            print(f"Category: {extraction['category']}")
            print(f"Confidence: {extraction['confidence']}")
            print(f"Validation: {'✓' if result['validation_passed'] else '✗'}")
        else:
            print(f"❌ Failed to process: {result.get('error', 'Unknown error')}")
    
    # Summary statistics
    print(f"\n--- Summary ---")
    successful = len([r for r in results if r.get("extraction")])
    print(f"Successfully processed: {successful}/{len(sample_emails)} emails")
    
    # Demonstrate downstream processing
    print(f"\n--- Downstream Processing Example ---")
    high_priority = [r for r in results if r.get("extraction") and r["extraction"]["priority"] in ["high", "urgent"]]
    print(f"High/Urgent priority tickets requiring immediate attention: {len(high_priority)}")
    
    negative_sentiment = [r for r in results if r.get("extraction") and r["extraction"]["sentiment"] in ["negative", "frustrated"]]
    print(f"Negative sentiment tickets requiring careful handling: {len(negative_sentiment)}")

if __name__ == "__main__":
    main()
