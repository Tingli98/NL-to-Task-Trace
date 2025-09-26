#!/usr/bin/env python3
"""
Demonstration script showing NL-to-Task-Trace capabilities.
"""

from nl_to_task_trace import TraceConverter
import json


def demo_basic_conversion():
    """Demonstrate basic natural language to trace conversion."""
    print("=" * 60)
    print("DEMO: Basic Natural Language to Task Trace Conversion")
    print("=" * 60)
    
    converter = TraceConverter()
    
    # Simple example
    description = "Click the login button and enter your username"
    print(f"\nInput: {description}")
    print("\nOutput:")
    
    trace = converter.convert_description_to_trace(description)
    
    for step in trace.steps:
        print(f"  {step.step_number}. {step.action.value.upper()}: {step.target}")
        if step.value:
            print(f"     Value: {step.value}")
    
    print(f"\nTrace Confidence: {trace.metadata.get('total_confidence', 'N/A')}")


def demo_complex_task():
    """Demonstrate complex multi-step task conversion."""
    print("\n" + "=" * 60)
    print("DEMO: Complex Multi-Step Task")
    print("=" * 60)
    
    converter = TraceConverter()
    
    description = """
    Navigate to the online banking website. 
    Click on the login link. 
    Enter your username "john.smith" in the username field.
    Type your password "SecurePass123" in the password field.
    Click the "Sign In" button.
    Wait for the dashboard to load.
    Click on "Account Summary" tab.
    Verify that the account balance is displayed.
    """
    
    print(f"Input Task Description:")
    print(description.strip())
    print("\nConverted Trace:")
    
    trace = converter.convert_description_to_trace(description)
    enhanced_trace = converter.enhance_trace_with_context(trace)
    
    for step in enhanced_trace.steps:
        print(f"\n{step.step_number}. {step.action.value.upper()}")
        print(f"   Target: {step.target}")
        if step.value:
            print(f"   Value: {step.value}")
        print(f"   Description: {step.description}")
        
        # Show confidence and validation
        confidence = step.metadata.get('parsing_confidence', 0)
        validation = step.metadata.get('validation', {})
        print(f"   Confidence: {confidence:.2f}")
        if not validation.get('complete', True):
            print(f"   Issues: {', '.join(validation.get('issues', []))}")


def demo_json_output():
    """Demonstrate JSON serialization."""
    print("\n" + "=" * 60)
    print("DEMO: JSON Serialization")
    print("=" * 60)
    
    converter = TraceConverter()
    
    description = "Open calculator app. Type 15. Click plus button. Type 25. Click equals button."
    trace = converter.convert_description_to_trace(description)
    
    print("Task converted to JSON:")
    print(trace.to_json())


def demo_file_processing():
    """Demonstrate processing task files."""
    print("\n" + "=" * 60)
    print("DEMO: File Processing")
    print("=" * 60)
    
    import os
    converter = TraceConverter()
    
    example_files = [
        "examples/login_task.txt",
        "examples/shopping_task.txt", 
        "examples/email_task.txt"
    ]
    
    for filename in example_files:
        if os.path.exists(filename):
            print(f"\nProcessing: {filename}")
            with open(filename, 'r') as f:
                content = f.read().strip()
            
            trace = converter.convert_description_to_trace(content)
            print(f"  Task: {trace.task_description}")
            print(f"  Steps: {len(trace.steps)}")
            print(f"  Confidence: {trace.metadata.get('total_confidence', 0):.2f}")


def main():
    """Run all demonstrations."""
    print("NL-to-Task-Trace Demonstration")
    print("Converting Natural Language to Structured Task Traces")
    
    demo_basic_conversion()
    demo_complex_task() 
    demo_json_output()
    demo_file_processing()
    
    print("\n" + "=" * 60)
    print("Demonstration Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()