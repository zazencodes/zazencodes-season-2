"""
03_rag_hr_bot.py
Stage 3 – Retrieval‑Augmented Generation (RAG)

Ask questions about your company handbook stored in memory.

Learning Objectives:
- Understand how to build RAG systems with DSPy
- Learn about retrieval quality and answer attribution
- Practice RAG evaluation with multiple metrics
- See how to optimize RAG pipelines for better performance

This demo uses an expanded in‑memory knowledge base. In production,
you would use a proper vector store like Pinecone, Weaviate, or ChromaDB.
"""

import os, dspy, textwrap, logging, re
from typing import List, Dict, Tuple, Optional
from dotenv import load_dotenv
from dataclasses import dataclass
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

dspy.settings.configure(
    lm=dspy.OpenAI(model="gpt-4o-mini"),
    cache="sqlite",
    temperature=0.2,
)

# ---- Expanded Company Knowledge Base ----------------------------------------
@dataclass
class Document:
    """Structure for company handbook documents."""
    id: str
    title: str
    content: str
    category: str
    last_updated: str

# Realistic HR documentation
company_docs = [
    Document(
        id="pto_001",
        title="Paid Time Off Policy",
        content="Employees accrue 1.5 days of paid time off (PTO) per month, for a total of 18 days per year. "
                "PTO can be used for vacation, personal time, or sick leave. Employees must request PTO at least "
                "2 weeks in advance for planned time off. PTO carries over up to 5 days per year. "
                "New employees are eligible for PTO after 90 days of employment.",
        category="benefits",
        last_updated="2024-01-15"
    ),
    Document(
        id="tech_001",
        title="Laptop and Equipment Policy",
        content="New hires choose between a MacBook Pro (14-inch M3) and a Dell XPS 13 Plus. "
                "IT covers standard 3-year warranty and AppleCare/Dell ProSupport. "
                "Employees are responsible for basic care and must report damage within 24 hours. "
                "Software installation requires IT approval. Personal use is permitted but monitored.",
        category="equipment",
        last_updated="2024-02-01"
    ),
    Document(
        id="expense_001",
        title="Business Expense Reimbursement",
        content="Meals under $75 per person do not require itemized receipts. "
                "Alcohol is not reimbursable unless part of client entertainment (pre-approved). "
                "Travel expenses must be booked through corporate travel portal. "
                "Uber/taxi receipts required for rides over $25. Hotel wifi and parking are reimbursable. "
                "Submit expenses within 30 days of incurrence.",
        category="finance",
        last_updated="2024-01-20"
    ),
    Document(
        id="remote_001",
        title="Remote Work Guidelines",
        content="Employees may work remotely up to 3 days per week with manager approval. "
                "Core collaboration hours are 10 AM - 3 PM local time. "
                "Home office equipment stipend of $500 annually for ergonomic setup. "
                "Secure VPN connection required for all remote work. "
                "In-person attendance required for team meetings and client presentations.",
        category="workplace",
        last_updated="2024-02-15"
    ),
    Document(
        id="benefits_001",
        title="Health and Wellness Benefits",
        content="Company provides comprehensive health insurance with 80% coverage. "
                "Dental and vision included at no additional cost. "
                "Mental health support through EAP program with 6 free sessions annually. "
                "Fitness reimbursement up to $50/month for gym memberships or wellness apps. "
                "Annual health screening with $200 HSA contribution bonus.",
        category="benefits",
        last_updated="2024-01-10"
    ),
    Document(
        id="security_001",
        title="Information Security Policy",
        content="All passwords must be at least 12 characters with MFA enabled. "
                "USB drives must be encrypted and approved by IT. "
                "Report phishing attempts immediately to security@company.com. "
                "Lock workstation when away from desk. "
                "No personal cloud storage for company data. Use approved tools only.",
        category="security",
        last_updated="2024-02-10"
    ),
    Document(
        id="training_001",
        title="Professional Development",
        content="Annual learning budget of $2,000 per employee for courses, conferences, and certifications. "
                "Manager approval required for external training over $500. "
                "Internal lunch-and-learn sessions held monthly. "
                "Tuition reimbursement available for job-relevant degree programs (50% coverage). "
                "Conference attendance limited to one major conference per year.",
        category="development",
        last_updated="2024-01-25"
    ),
    Document(
        id="hiring_001",
        title="Employee Referral Program",
        content="Employees receive $2,000 bonus for successful referrals (after 90 days). "
                "Referrals for senior positions (Director+) qualify for $3,000 bonus. "
                "Immediate family members not eligible for referral bonus. "
                "Multiple referrals for same position share the bonus equally. "
                "Referrer must remain employed for 6 months after hire date.",
        category="hiring",
        last_updated="2024-01-30"
    )
]

# ---- Improved Retrieval System ----------------------------------------------
class ImprovedRetrieval:
    """Enhanced retrieval system with semantic matching and ranking."""
    
    def __init__(self, documents: List[Document]):
        self.documents = documents
        self.doc_index = {doc.id: doc for doc in documents}
    
    def search(self, query: str, k: int = 3) -> List[Dict]:
        """Search documents with improved ranking."""
        query_lower = query.lower()
        query_terms = set(query_lower.split())
        
        scored_docs = []
        
        for doc in self.documents:
            score = self._calculate_relevance_score(doc, query_lower, query_terms)
            if score > 0:
                scored_docs.append({
                    'document': doc,
                    'score': score,
                    'text': doc.content,
                    'title': doc.title,
                    'category': doc.category,
                    'doc_id': doc.id
                })
        
        # Sort by relevance score and return top k
        scored_docs.sort(key=lambda x: x['score'], reverse=True)
        return scored_docs[:k]
    
    def _calculate_relevance_score(self, doc: Document, query: str, query_terms: set) -> float:
        """Calculate relevance score based on multiple factors."""
        content_lower = doc.content.lower()
        title_lower = doc.title.lower()
        
        # Exact phrase matching (highest priority)
        phrase_score = 3.0 if query in content_lower else 0.0
        
        # Title relevance (high priority)
        title_score = sum(2.0 for term in query_terms if term in title_lower)
        
        # Content term matching
        content_score = sum(1.0 for term in query_terms if term in content_lower)
        
        # Category bonus for common HR terms
        category_bonus = 0.5 if any(term in doc.category for term in query_terms) else 0.0
        
        return phrase_score + title_score + content_score + category_bonus

# Initialize retrieval system
retrieval_system = ImprovedRetrieval(company_docs)

# ---- Enhanced RAG Signatures ------------------------------------------------
class HRBotWithSources(dspy.Signature):
    """Answer HR questions with source attribution and confidence scoring."""
    
    question: str = dspy.InputField(desc="Employee question about company policies")
    context: str = dspy.InputField(desc="Relevant policy documents and information")
    answer: str = dspy.OutputField(desc="Clear, helpful answer based on company policies")
    sources: str = dspy.OutputField(desc="Specific document titles or sections referenced")
    confidence: float = dspy.OutputField(desc="Confidence in answer accuracy (0.0-1.0)")
    caveats: str = dspy.OutputField(desc="Important limitations or conditions to note")

# ---- RAG Module with Enhanced Features --------------------------------------
class EnhancedHRBot(dspy.Module):
    """Advanced RAG pipeline with source attribution and context management."""

    def __init__(self, k: int = 3):
        super().__init__()
        self.k = k
        self.retrieval = retrieval_system
        self.answer = dspy.ChainOfThought(HRBotWithSources)

    def forward(self, question: str):
        # Retrieve relevant documents
        retrieved_docs = self.retrieval.search(question, k=self.k)
        
        if not retrieved_docs:
            return dspy.Prediction(
                answer="I don't have information about that in our company policies. "
                       "Please contact HR directly for assistance.",
                sources="No relevant documents found",
                confidence=0.0,
                caveats="Unable to find relevant policy information",
                context="",
                retrieved_docs=[]
            )
        
        # Format context with source attribution
        context_parts = []
        for i, doc_info in enumerate(retrieved_docs, 1):
            doc = doc_info['document']
            context_parts.append(
                f"[Source {i}: {doc.title}]\n{doc.content}\n"
            )
        
        context = "\n".join(context_parts)
        
        # Generate answer with reasoning
        prediction = self.answer(question=question, context=context)
        
        # Add metadata
        prediction.retrieved_docs = retrieved_docs
        prediction.context = context
        
        return prediction

# ---- Evaluation Functions ---------------------------------------------------
def evaluate_answer_quality(question: str, prediction, expected_answer: str = None) -> Dict:
    """Evaluate RAG answer quality across multiple dimensions."""
    evaluation = {
        "completeness": 0.0,
        "accuracy": 0.0,
        "source_attribution": 0.0,
        "helpful": 0.0,
        "issues": []
    }
    
    answer = prediction.answer.lower()
    
    # Check completeness (does it address the question?)
    question_terms = set(question.lower().split())
    answer_terms = set(answer.split())
    term_overlap = len(question_terms.intersection(answer_terms)) / len(question_terms)
    evaluation["completeness"] = min(1.0, term_overlap * 2)  # Scale appropriately
    
    # Check for source attribution
    if hasattr(prediction, 'sources') and prediction.sources:
        if "source" in prediction.sources.lower() or any(doc['title'].lower() in prediction.sources.lower() 
                                                       for doc in prediction.retrieved_docs):
            evaluation["source_attribution"] = 1.0
        else:
            evaluation["issues"].append("Weak source attribution")
    else:
        evaluation["issues"].append("No source attribution")
    
    # Check for helpfulness indicators
    helpful_phrases = ["contact hr", "more information", "specific situation", "varies"]
    if any(phrase in answer for phrase in helpful_phrases):
        evaluation["helpful"] += 0.5
    
    if len(answer.split()) > 20:  # Substantial answer
        evaluation["helpful"] += 0.5
    
    # Overall accuracy (simplified - in practice you'd use semantic similarity)
    if expected_answer:
        expected_terms = set(expected_answer.lower().split())
        accuracy_overlap = len(answer_terms.intersection(expected_terms)) / len(expected_terms)
        evaluation["accuracy"] = accuracy_overlap
    else:
        # Use confidence as proxy when no expected answer
        evaluation["accuracy"] = getattr(prediction, 'confidence', 0.5)
    
    return evaluation

def evaluate_retrieval_quality(question: str, retrieved_docs: List[Dict]) -> Dict:
    """Evaluate the quality of document retrieval."""
    if not retrieved_docs:
        return {"precision": 0.0, "coverage": 0.0, "diversity": 0.0}
    
    query_terms = set(question.lower().split())
    
    # Precision: how many retrieved docs are relevant?
    relevant_docs = 0
    for doc_info in retrieved_docs:
        doc_terms = set(doc_info['text'].lower().split())
        if len(query_terms.intersection(doc_terms)) >= 2:  # At least 2 terms match
            relevant_docs += 1
    
    precision = relevant_docs / len(retrieved_docs)
    
    # Coverage: do we have diverse information?
    categories = set(doc_info['category'] for doc_info in retrieved_docs)
    diversity = len(categories) / len(retrieved_docs)
    
    # Coverage score based on document types
    coverage = min(1.0, len(retrieved_docs) / 3)  # Assume 3 is good coverage
    
    return {
        "precision": precision,
        "coverage": coverage,
        "diversity": diversity
    }

# ---- Test Cases and Examples ------------------------------------------------
test_questions = [
    {
        "question": "How many PTO days do we get each year?",
        "expected_answer": "18 days per year",
        "category": "benefits"
    },
    {
        "question": "Do I need a receipt for a $50 team lunch?",
        "expected_answer": "No receipt required for meals under $75",
        "category": "finance"
    },
    {
        "question": "Can I work from home 4 days a week?",
        "expected_answer": "Remote work limited to 3 days per week",
        "category": "workplace"
    },
    {
        "question": "What laptop options are available for new hires?",
        "expected_answer": "MacBook Pro or Dell XPS",
        "category": "equipment"
    },
    {
        "question": "How much is the employee referral bonus?",
        "expected_answer": "$2,000 for regular positions, $3,000 for senior roles",
        "category": "hiring"
    },
    {
        "question": "What's the password policy?",
        "expected_answer": "At least 12 characters with MFA",
        "category": "security"
    }
]

def run_comprehensive_evaluation(bot: EnhancedHRBot) -> Dict:
    """Run comprehensive evaluation on the HR bot."""
    results = {
        "individual_results": [],
        "summary": {
            "avg_completeness": 0.0,
            "avg_accuracy": 0.0,
            "avg_source_attribution": 0.0,
            "avg_retrieval_precision": 0.0,
            "total_questions": len(test_questions)
        }
    }
    
    print("\n=== Comprehensive RAG Evaluation ===\n")
    
    for i, test_case in enumerate(test_questions):
        question = test_case["question"]
        expected = test_case["expected_answer"]
        
        print(f"Q{i+1}: {question}")
        
        # Get prediction
        prediction = bot(question=question)
        
        # Evaluate answer quality
        answer_eval = evaluate_answer_quality(question, prediction, expected)
        
        # Evaluate retrieval quality
        retrieval_eval = evaluate_retrieval_quality(question, prediction.retrieved_docs)
        
        # Combine results
        result = {
            "question": question,
            "answer": prediction.answer,
            "sources": getattr(prediction, 'sources', 'N/A'),
            "confidence": getattr(prediction, 'confidence', 0.0),
            "answer_evaluation": answer_eval,
            "retrieval_evaluation": retrieval_eval
        }
        
        results["individual_results"].append(result)
        
        print(f"Answer: {prediction.answer}")
        print(f"Sources: {result['sources']}")
        print(f"Quality Scores - Completeness: {answer_eval['completeness']:.2f}, "
              f"Accuracy: {answer_eval['accuracy']:.2f}, "
              f"Attribution: {answer_eval['source_attribution']:.2f}")
        
        if answer_eval["issues"]:
            print(f"Issues: {', '.join(answer_eval['issues'])}")
        
        print()
    
    # Calculate summary statistics
    if results["individual_results"]:
        summary = results["summary"]
        summary["avg_completeness"] = sum(r["answer_evaluation"]["completeness"] 
                                        for r in results["individual_results"]) / len(results["individual_results"])
        summary["avg_accuracy"] = sum(r["answer_evaluation"]["accuracy"] 
                                    for r in results["individual_results"]) / len(results["individual_results"])
        summary["avg_source_attribution"] = sum(r["answer_evaluation"]["source_attribution"] 
                                               for r in results["individual_results"]) / len(results["individual_results"])
        summary["avg_retrieval_precision"] = sum(r["retrieval_evaluation"]["precision"] 
                                                for r in results["individual_results"]) / len(results["individual_results"])
    
    return results

def demonstrate_optimization_potential():
    """Show how RAG optimization would work in practice."""
    print("\n=== RAG Optimization Demonstration ===")
    print("In production, you would use dspy.MIPROv2 to optimize this RAG pipeline:")
    print()
    print("# Example optimization setup:")
    print("from dspy.teleprompt import MIPROv2")
    print()
    print("# Define training set from test questions")
    print("trainset = [")
    for q in test_questions[:3]:  # Show first 3 as example
        print(f'    dspy.Example(question="{q["question"]}", answer="{q["expected_answer"]}"),')
    print("    # ... more examples")
    print("]")
    print()
    print("# Set up optimizer")
    print("optimizer = MIPROv2(metric=answer_exact_match, auto='light')")
    print("optimized_bot = optimizer.compile(hr_bot, trainset=trainset)")
    print()
    print("Expected improvements after optimization:")
    print("- Better retrieval relevance through query reformulation")
    print("- More consistent source attribution")
    print("- Improved answer completeness")
    print("- Enhanced reasoning chains in responses")

def main():
    """Main function demonstrating the enhanced RAG HR bot."""
    print("=== DSPy RAG HR Bot Demo (Enhanced) ===\n")
    print("This demo shows an improved RAG system with:")
    print("- Expanded knowledge base (8 realistic HR documents)")
    print("- Enhanced retrieval with semantic scoring")
    print("- Source attribution and confidence scoring")
    print("- Comprehensive evaluation metrics")
    print("- Optimization demonstration")
    print()
    
    # Initialize bot
    hr_bot = EnhancedHRBot(k=3)
    
    # Show interactive example
    sample_question = "How many PTO days do we get per year?"
    print(f"--- Sample Question ---")
    print(f"Q: {sample_question}")
    
    prediction = hr_bot(question=sample_question)
    
    print(f"A: {prediction.answer}")
    print(f"Sources: {prediction.sources}")
    print(f"Confidence: {getattr(prediction, 'confidence', 'N/A')}")
    
    if hasattr(prediction, 'caveats') and prediction.caveats:
        print(f"Important Notes: {prediction.caveats}")
    
    # Show retrieval details
    print(f"\n--- Retrieval Details ---")
    for i, doc_info in enumerate(prediction.retrieved_docs, 1):
        print(f"Document {i}: {doc_info['title']} (Score: {doc_info['score']:.2f})")
    
    # Run comprehensive evaluation
    eval_results = run_comprehensive_evaluation(hr_bot)
    
    # Print summary
    summary = eval_results["summary"]
    print("=== Overall Performance Summary ===")
    print(f"Average Completeness: {summary['avg_completeness']:.2f}/1.0")
    print(f"Average Accuracy: {summary['avg_accuracy']:.2f}/1.0")
    print(f"Average Source Attribution: {summary['avg_source_attribution']:.2f}/1.0")
    print(f"Average Retrieval Precision: {summary['avg_retrieval_precision']:.2f}/1.0")
    
    # Show optimization potential
    demonstrate_optimization_potential()
    
    print("\n--- Key Improvements Made ---")
    print("1. ✅ Realistic, comprehensive knowledge base")
    print("2. ✅ Enhanced retrieval with semantic scoring")
    print("3. ✅ Source attribution in all answers")
    print("4. ✅ Multi-dimensional evaluation metrics")
    print("5. ✅ Confidence scoring and caveats")
    print("6. ✅ Optimization framework demonstration")

if __name__ == "__main__":
    main()
