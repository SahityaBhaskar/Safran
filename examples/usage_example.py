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
        "Set the TEST switch to the middle position and release the SHORT-CIRCUIT TEST switch.",
        "The test can be continued.",
        "Oil and grease are to be removed with a degreasing agent.",
        "1. Codebase: Your submitted code should be well-documented, modular, and feature comments as necessary.Ensure that your code is organized into relevant modules for better readability and maintainability.Documentation:The accompanying documentation should detail the workflow, architectural decisions, and any assumptions made during development.Keep the documentation brief yet comprehensive.Demo Instructions:Include a brief guide on how to run the application, including any necessary setup steps and example queries to demonstrate the application's functionality.Test Cases:Provide a few example to showcase how your application works."
    ]
    
    # Demonstrating both sync and async usage
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

