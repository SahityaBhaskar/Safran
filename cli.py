#!/usr/bin/env python3
import argparse
import sys
from dotenv import load_dotenv
from src.checker.technical_writing_checker import TechnicalWritingChecker

def main():
    # Load environment variables
    load_dotenv()

    # Set up argument parser
    parser = argparse.ArgumentParser(description='Technical Writing Checker CLI')
    
    # Create mutually exclusive group for input methods
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        'text', 
        nargs='?', 
        help='Text to analyze'
    )
    input_group.add_argument(
        '-f', 
        '--file', 
        help='Read text from file instead of command line'
    )

    args = parser.parse_args()

    try:
        # Initialize checker
        checker = TechnicalWritingChecker()

        # Get text from file or command line
        if args.file:
            try:
                with open(args.file, 'r') as f:
                    text = f.read()
            except FileNotFoundError:
                print(f"Error: File '{args.file}' not found")
                sys.exit(1)
            except Exception as e:
                print(f"Error reading file: {e}")
                sys.exit(1)
        else:
            text = args.text

        # Check if text is empty
        if not text or text.isspace():
            print("Error: No text provided for analysis")
            sys.exit(1)

        # Process the text
        analysis = checker.check_text(text)
        
        # Print the results
        print("\nAnalysis Results:")
        print("=" * 50)
        print(checker.format_analysis(analysis))

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
