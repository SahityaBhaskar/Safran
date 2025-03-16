import asyncio
import os
from dotenv import load_dotenv
from src.checker.technical_writing_checker import TechnicalWritingChecker

# Load environment variables
load_dotenv()

async def main():
    checker = TechnicalWritingChecker()
    
    # Example texts
    texts = [
        "Turn shaft assembly.",
        "The safety procedures are supplied by the manufacturer.",
        "Set the TEST switch to the middle position and release the SHORT-CIRCUIT TEST switch."
    ]
    
    # Demonstrate both sync and async usage
    print("Synchronous Analysis:")
    for text in texts[:1]:
        analysis = checker.check_text(text)
        print(checker.format_analysis(analysis))
        
    print("\nAsynchronous Analysis:")
    analyses = await checker.process_multiple_texts(texts)
    for analysis in analyses:
        print(checker.format_analysis(analysis))
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    asyncio.run(main())

