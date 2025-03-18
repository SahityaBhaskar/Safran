import os
from typing import List
import asyncio
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from .models import DocumentAnalysis
from ..utils.formatting import format_analysis

class TechnicalWritingChecker:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
            
        if base_url:
            self.llm = ChatOpenAI(
                temperature=0,
                model_name="gpt-4o",
                api_key=api_key,
                base_url=base_url
            )
        else:
            self.llm = ChatOpenAI(
                temperature=0,
                model_name="gpt-4o",
                api_key=api_key,
            )
        
        self.output_parser = PydanticOutputParser(pydantic_object=DocumentAnalysis)
        self._setup_prompt_template()
    
    def _setup_prompt_template(self):
        template = """
        Analyze the following technical writing text and check for these rules:
        1. Article Usage: 
           - Use articles (the, a, an) before nouns when needed
           - Use demonstrative adjectives (this, that, these, those) where appropriate
           - Check for missing articles before singular countable nouns
           - Ensure proper article agreement with plural/singular nouns
           - Flag instances where articles are missing or incorrectly used
        
        2. Active Voice:
           - Use active voice in procedural writing (subject performs the action)
           - Avoid passive constructions like "is done", "was performed", "should be completed"
           - Convert phrases like "it is recommended" to direct commands
           - Identify sentences where the actor/subject is unclear or missing
           - Flag sentences where passive voice makes instructions unclear
        
        3. Single Instructions:
           - One instruction per sentence
           - If a sentence contains multiple instructions, categorize it under this rule type
           - Split compound instructions into separate sentences
           - Each sentence should convey one clear action or concept
        
        4. Imperative Form:
           - Write instructions in command form
           - Start instructions with action verbs
           - Remove phrases like "you should" or "please"
           - Convert indirect suggestions to direct commands
           - If a sentence needs to be rewritten in command form, categorize it under this rule type
        
        5. Sentence Length:
           - Flag ONLY if sentence has MORE THAN 20 words
           - Count words carefully before flagging
           - Only use this rule type when the word count exceeds 20
           - Do not use this category for other types of violations
        
        Important: 
        - Categorize each violation under the most specific applicable rule type
        - Do not use "Sentence Length" for violations that are primarily about other rules
        - For sentences with multiple issues, prioritize the most significant rule violation
        - Provide clear explanations and specific suggestions for improvement
    
        Text to analyze: {text}
    
        Analyze the entire text and provide a complete analysis. Include all violations found throughout the text.
        
        Provide an analysis in the following format:
        {format_instructions}
        """
    
        self.prompt = PromptTemplate(
            template=template,
            input_variables=["text"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )
        
        # Create a runnable sequence
        self.chain = self.prompt | self.llm
    
    
    def check_text(self, text: str) -> DocumentAnalysis:
        """
        Synchronously analyze a piece of technical writing.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            DocumentAnalysis: Analysis results including violations and suggestions
        """
        # Invoke the LLM chain with the input text
        result = self.chain.invoke({"text": text})
        
        # Parse the LLM response into a DocumentAnalysis object
        parsed_result = self.output_parser.parse(result.content)
        
        # Create a new DocumentAnalysis object with the full text included
        complete_analysis = DocumentAnalysis(
            violations=parsed_result.violations,
            improved_text=parsed_result.improved_text,
            full_text=text  # Include the original complete text
        )
        
        return complete_analysis
    
    
    async def check_text_async(self, text: str) -> DocumentAnalysis:
        """
        Asynchronously analyze a piece of technical writing.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            DocumentAnalysis: Analysis results including violations and suggestions
        """
        # Invoke the LLM chain asynchronously
        result = await self.chain.ainvoke({"text": text})
        
        # Parse the LLM response
        parsed_result = self.output_parser.parse(result.content)
        
        # Create a new DocumentAnalysis object with the full text included
        complete_analysis = DocumentAnalysis(
            violations=parsed_result.violations,
            improved_text=parsed_result.improved_text,
            full_text=text  # Include the original complete text
        )
        
        return complete_analysis
    
    
    async def process_multiple_texts(self, texts: List[str]) -> List[DocumentAnalysis]:
        """
        Process multiple texts concurrently.
        
        Args:
            texts (List[str]): List of texts to analyze
            
        Returns:
            List[DocumentAnalysis]: List of analysis results
        """
        tasks = [self.check_text_async(text) for text in texts]
        return await asyncio.gather(*tasks)
    
    def format_analysis(self, analysis: DocumentAnalysis) -> str:
        """
        Format the analysis results in a readable format.
        
        Args:
            analysis (DocumentAnalysis): The analysis to format
            
        Returns:
            str: Formatted analysis
        """
        return format_analysis(analysis)