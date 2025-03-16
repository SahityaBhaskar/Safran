from ..checker.models import DocumentAnalysis

def format_analysis(analysis: DocumentAnalysis) -> str:
    """
    Format the analysis results into a readable string.
    """
    output = []
    output.append("=== Technical Writing Analysis ===\n")
    
    if analysis.violations:
        output.append("Found Rule Violations:")
        for violation in analysis.violations:
            output.append(f"\n[{violation.rule_type}]")
            output.append(f"Original: {violation.original_text}")
            output.append(f"Issue: {violation.explanation}")
            output.append(f"Suggestion: {violation.suggestion}")
    else:
        output.append("No rule violations found.")
        
    output.append("\n=== Improved Text ===")
    output.append(analysis.improved_text)
    
    return "\n".join(output)

