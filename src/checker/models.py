from pydantic import BaseModel, Field
from typing import List

class RuleViolation(BaseModel):
    rule_type: str = Field(description="Type of rule that was violated")
    original_text: str = Field(description="The text that contains the violation")
    suggestion: str = Field(description="Suggested correction")
    explanation: str = Field(description="Explanation of why this is a violation")

class DocumentAnalysis(BaseModel):
    violations: List[RuleViolation] = Field(description="List of rule violations found")
    improved_text: str = Field(description="The corrected version of the text")

    @property
    def original_text(self) -> str:
        """
        Get the original text from the first violation or return improved text if no violations.
        """
        if self.violations:
            return self.violations[0].original_text
        return self.improved_text

