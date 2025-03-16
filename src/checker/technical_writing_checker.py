import os
from typing import List
import asyncio
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from .models import DocumentAnalysis
from ..utils.formatting import format_analysis

class TechnicalWritingChecker:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        if not base_url:
            raise ValueError("OPENAI_BASE_URL environment variable is not set")
            
        self.llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-4",
            api_key=api_key,
            base_url=base_url
        )
        
        self.output_parser = PydanticOutputParser(pydantic_object=DocumentAnalysis)
        self._setup_prompt_template()
        
    # [Rest of the TechnicalWritingChecker implementation...]

