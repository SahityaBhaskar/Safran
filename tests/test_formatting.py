import pytest
from src.checker.models import DocumentAnalysis, RuleViolation
from src.utils.formatting import format_analysis

def test_format_analysis():
    analysis = DocumentAnalysis(
        violations=[
            RuleViolation(
                rule_type="Article Usage",
                original_text="Turn shaft assembly",
                suggestion="Turn the shaft assembly",
                explanation="Missing article before noun"
            )
        ],
        improved_text="Turn the shaft assembly."
    )
    
    formatted = format_analysis(analysis)
    assert "Technical Writing Analysis" in formatted
    assert "Article Usage" in formatted

