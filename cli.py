#!/usr/bin/env python3
"""
Command-line interface for NL-to-Task-Trace conversion.
"""

import argparse
import sys
import json
from pathlib import Path

from nl_to_task_trace import TraceConverter


def main():
    parser = argparse.ArgumentParser(
        description="Convert natural language task descriptions to structured traces"
    )
    
    parser.add_argument(
        'input',
        help='Input text (either a string or path to a text file)',
        nargs='?'
    )
    
    parser.add_argument(
        '--file', '-f',
        help='Read input from file',
        type=str
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file path (default: stdout)',
        type=str
    )
    
    parser.add_argument(
        '--format',
        help='Output format',
        choices=['json', 'pretty'],
        default='pretty'
    )
    
    parser.add_argument(
        '--enhance',
        help='Apply contextual enhancement to the trace',
        action='store_true'
    )
    
    parser.add_argument(
        '--trace-id',
        help='Custom trace ID',
        type=str
    )
    
    args = parser.parse_args()
    
    # Get input text
    input_text = None
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                input_text = f.read().strip()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            return 1
    elif args.input:
        input_text = args.input
    else:
        print("Error: Please provide input text or use --file option", file=sys.stderr)
        parser.print_help()
        return 1
    
    if not input_text:
        print("Error: Input text is empty", file=sys.stderr)
        return 1
    
    # Convert the text to trace
    converter = TraceConverter()
    
    try:
        trace = converter.convert_description_to_trace(input_text, args.trace_id)
        
        if args.enhance:
            trace = converter.enhance_trace_with_context(trace)
        
        # Format output
        if args.format == 'json':
            output = trace.to_json()
        else:
            output = format_trace_pretty(trace)
        
        # Write output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Trace saved to {args.output}")
        else:
            print(output)
        
        return 0
    
    except Exception as e:
        print(f"Error converting trace: {e}", file=sys.stderr)
        return 1


def format_trace_pretty(trace) -> str:
    """Format a trace in a human-readable way."""
    lines = []
    lines.append(f"Task: {trace.task_description}")
    lines.append(f"Trace ID: {trace.trace_id}")
    lines.append("-" * 50)
    
    for step in trace.steps:
        lines.append(f"{step.step_number}. {step.action.value.upper()}")
        lines.append(f"   Target: {step.target}")
        if step.value:
            lines.append(f"   Value: {step.value}")
        lines.append(f"   Description: {step.description}")
        
        if step.metadata.get('parsing_confidence'):
            confidence = step.metadata['parsing_confidence']
            lines.append(f"   Confidence: {confidence:.2f}")
        
        lines.append("")
    
    # Add metadata
    if trace.metadata:
        lines.append("Metadata:")
        for key, value in trace.metadata.items():
            lines.append(f"  {key}: {value}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())