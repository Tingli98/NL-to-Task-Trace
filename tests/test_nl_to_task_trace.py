"""
Unit tests for the NL-to-Task-Trace system.
"""

import unittest
import json
from nl_to_task_trace import TraceConverter, TaskTrace, TaskStep, ActionType


class TestNLParser(unittest.TestCase):
    """Test cases for the NL parser functionality."""
    
    def setUp(self):
        self.converter = TraceConverter()
    
    def test_basic_conversion(self):
        """Test basic natural language to trace conversion."""
        description = "Click the login button"
        trace = self.converter.convert_description_to_trace(description)
        
        self.assertEqual(len(trace.steps), 1)
        self.assertEqual(trace.steps[0].action, ActionType.CLICK)
        self.assertEqual(trace.steps[0].target, "login button")
    
    def test_multi_step_task(self):
        """Test conversion of multi-step tasks."""
        description = "Navigate to homepage. Click login button. Type username."
        trace = self.converter.convert_description_to_trace(description)
        
        self.assertEqual(len(trace.steps), 3)
        self.assertEqual(trace.steps[0].action, ActionType.NAVIGATE)
        self.assertEqual(trace.steps[1].action, ActionType.CLICK)
        self.assertEqual(trace.steps[2].action, ActionType.TYPE)
    
    def test_value_extraction(self):
        """Test extraction of quoted values."""
        description = 'Type "username" in the field'
        trace = self.converter.convert_description_to_trace(description)
        
        self.assertEqual(len(trace.steps), 1)
        self.assertEqual(trace.steps[0].action, ActionType.TYPE)
        self.assertEqual(trace.steps[0].value, "username")
    
    def test_trace_serialization(self):
        """Test JSON serialization of traces."""
        description = "Click button"
        trace = self.converter.convert_description_to_trace(description)
        
        # Test to_dict
        trace_dict = trace.to_dict()
        self.assertIsInstance(trace_dict, dict)
        self.assertIn('task_description', trace_dict)
        self.assertIn('steps', trace_dict)
        
        # Test to_json
        json_str = trace.to_json()
        self.assertIsInstance(json_str, str)
        
        # Test round-trip
        parsed_data = json.loads(json_str)
        reconstructed_trace = TaskTrace.from_dict(parsed_data)
        self.assertEqual(len(reconstructed_trace.steps), len(trace.steps))


class TestTraceStructure(unittest.TestCase):
    """Test cases for trace data structures."""
    
    def test_task_step_creation(self):
        """Test TaskStep creation and serialization."""
        step = TaskStep(
            action=ActionType.CLICK,
            target="button",
            value="test",
            description="Click the test button"
        )
        
        self.assertEqual(step.action, ActionType.CLICK)
        self.assertEqual(step.target, "button")
        self.assertEqual(step.value, "test")
    
    def test_task_trace_creation(self):
        """Test TaskTrace creation with steps."""
        steps = [
            TaskStep(ActionType.NAVIGATE, "homepage"),
            TaskStep(ActionType.CLICK, "login button")
        ]
        
        trace = TaskTrace("Test task", steps)
        
        self.assertEqual(len(trace.steps), 2)
        self.assertEqual(trace.steps[0].step_number, 1)
        self.assertEqual(trace.steps[1].step_number, 2)


class TestTraceConverter(unittest.TestCase):
    """Test cases for the trace converter."""
    
    def setUp(self):
        self.converter = TraceConverter()
    
    def test_enhancement(self):
        """Test trace enhancement functionality."""
        description = "Click field. Type username."
        trace = self.converter.convert_description_to_trace(description)
        enhanced_trace = self.converter.enhance_trace_with_context(trace)
        
        self.assertTrue(enhanced_trace.metadata.get('enhanced'))
        self.assertIn('total_confidence', enhanced_trace.metadata)
    
    def test_action_mapping(self):
        """Test proper mapping of action verbs to ActionType enums."""
        test_cases = [
            ("navigate to page", ActionType.NAVIGATE),
            ("click button", ActionType.CLICK),
            ("type text", ActionType.TYPE),
            ("wait for load", ActionType.WAIT),
            ("verify result", ActionType.VERIFY),
        ]
        
        for description, expected_action in test_cases:
            trace = self.converter.convert_description_to_trace(description)
            self.assertEqual(len(trace.steps), 1)
            self.assertEqual(trace.steps[0].action, expected_action)


if __name__ == '__main__':
    # Run tests
    unittest.main()