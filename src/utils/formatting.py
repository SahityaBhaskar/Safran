from ..checker.models import DocumentAnalysis

def format_analysis(analysis: DocumentAnalysis) -> str:
    """
    Format the analysis results into a readable string.
    
    Args:
        analysis (DocumentAnalysis): The analysis to format
        
    Returns:
        str: Formatted analysis string
    """
    output = []
    output.append("=== Technical Writing Analysis ===\n")
    
    # Add original text using the property
    output.append(f"Original Text:\n{analysis.original_text}\n")
    
    # Add violations if any exist
    if analysis.violations:
        output.append("\nFound Rule Violations:")
        for violation in analysis.violations:
            output.append(f"\n[{violation.rule_type}]")
            output.append(f"Issue: {violation.explanation}")
            output.append(f"Suggestion: {violation.suggestion}")
    else:
        output.append("\nNo rule violations found.")
        
    # Add improved text
    output.append("\n=== Improved Text ===")
    output.append(analysis.improved_text)
    
    return "\n".join(output)