#!/usr/bin/env python3
"""
Command-line interface for SimpleMusic DSL converter.
"""

import argparse
import sys
from pathlib import Path

from .midi_converter import dsl_to_midi
from .examples import EXAMPLE_BASIC, EXAMPLE_COMPLEX, EXAMPLE_ADVANCED

def main():
    parser = argparse.ArgumentParser(
        description="Convert SimpleMusic DSL notation to MIDI files",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('input', nargs='?', help='Input DSL file (or use --example)')
    parser.add_argument('-o', '--output', default='output.mid', 
                       help='Output MIDI file (default: output.mid)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Show detailed parsing information')
    parser.add_argument('--example', choices=['basic', 'complex', 'advanced'],
                       help='Use a built-in example instead of input file')
    
    args = parser.parse_args()
    
    # Get DSL text
    if args.example:
        examples = {
            'basic': EXAMPLE_BASIC,
            'complex': EXAMPLE_COMPLEX, 
            'advanced': EXAMPLE_ADVANCED
        }
        dsl_text = examples[args.example]
        print(f"Using built-in example: {args.example}")
    elif args.input:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                dsl_text = f.read()
        except FileNotFoundError:
            print(f"Error: File '{args.input}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    else:
        print("Error: Either provide an input file or use --example")
        parser.print_help()
        sys.exit(1)
    
    # Convert to MIDI
    result = dsl_to_midi(dsl_text, args.output, verbose=args.verbose)
    
    if result is None:
        sys.exit(1)
    
    print(f"\n✨ Conversion completed! Output: {args.output}")

if __name__ == '__main__':
    main()