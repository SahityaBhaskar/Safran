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
        1. Article Usage: Use articles (the, a, an) or demonstrative adjectives
        2. Active Voice: Use active voice in procedural writing
        3. Single Instructions: One instruction per sentence
        4. Imperative Form: Write instructions in command form
        5. Sentence Length: Maximum 20 words per sentence

        Text to analyze: {text}

        Provide an analysis in the following format:
        {format_instructions}
        """
        
        self.prompt = PromptTemplate(
            template=template,
            input_variables=["text"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )
        
        # Create a runnable sequence instead of LLMChain
        self.chain = self.prompt | self.llm
    
    def check_text(self, text: str) -> DocumentAnalysis:
        """
        Synchronously analyze a piece of technical writing.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            DocumentAnalysis: Analysis results including violations and suggestions
        """
        result = self.chain.invoke({"text": text})
        return self.output_parser.parse(result.content)
    
    async def check_text_async(self, text: str) -> DocumentAnalysis:
        """
        Asynchronously analyze a piece of technical writing.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            DocumentAnalysis: Analysis results including violations and suggestions
        """
        result = await self.chain.ainvoke({"text": text})
        return self.output_parser.parse(result.content)
    
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