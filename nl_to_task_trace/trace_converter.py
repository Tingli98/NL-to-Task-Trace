"""
Converter for transforming parsed natural language into structured task traces.
"""

from typing import List, Dict, Optional
import uuid

from .trace_structure import TaskTrace, TaskStep, ActionType
from .nl_parser import NLParser, ParsedAction


class TraceConverter:
    """Converts parsed natural language actions into structured task traces."""
    
    def __init__(self):
        self.parser = NLParser()
        
        # Mapping from parsed action verbs to ActionType enums
        self.action_mapping = {
            'navigate': ActionType.NAVIGATE,
            'click': ActionType.CLICK,
            'type': ActionType.TYPE,
            'wait': ActionType.WAIT,
            'verify': ActionType.VERIFY,
            'select': ActionType.SELECT,
            'scroll': ActionType.SCROLL,
            'submit': ActionType.SUBMIT,
            'open': ActionType.OPEN,
            'close': ActionType.CLOSE
        }
    
    def convert_description_to_trace(self, description: str, trace_id: Optional[str] = None) -> TaskTrace:
        """
        Convert a natural language description into a structured task trace.
        
        Args:
            description: Natural language task description
            trace_id: Optional trace identifier
            
        Returns:
            TaskTrace object representing the parsed task
        """
        # Parse the natural language description
        parsed_actions = self.parser.parse_task_description(description)
        
        # Convert parsed actions to task steps
        steps = []
        for i, parsed_action in enumerate(parsed_actions, 1):
            step = self._convert_parsed_action_to_step(parsed_action, i)
            if step:
                steps.append(step)
        
        # Generate trace ID if not provided
        if trace_id is None:
            trace_id = str(uuid.uuid4())[:8]
        
        # Extract task title
        task_title = self.parser.extract_task_title(description)
        
        # Create metadata
        metadata = {
            'original_description': description,
            'parsed_actions_count': len(parsed_actions),
            'successful_conversions': len(steps)
        }
        
        return TaskTrace(
            task_description=task_title,
            steps=steps,
            trace_id=trace_id,
            metadata=metadata
        )
    
    def _convert_parsed_action_to_step(self, parsed_action: ParsedAction, step_number: int) -> Optional[TaskStep]:
        """Convert a ParsedAction into a TaskStep."""
        # Map verb to ActionType
        action_type = self.action_mapping.get(parsed_action.verb)
        if not action_type:
            return None
        
        # Determine target - use parsed target or infer from context
        target = parsed_action.target or self._infer_target(parsed_action)
        
        # Use parsed value or None
        value = parsed_action.value
        
        # Create description from original text
        description = parsed_action.original_text
        
        # Build metadata from modifiers and other info
        metadata = {
            'modifiers': parsed_action.modifiers,
            'original_verb': parsed_action.verb,
            'parsing_confidence': self._calculate_confidence(parsed_action)
        }
        
        return TaskStep(
            action=action_type,
            target=target,
            value=value,
            description=description,
            step_number=step_number,
            metadata=metadata
        )
    
    def _infer_target(self, parsed_action: ParsedAction) -> str:
        """Infer target when not explicitly found."""
        verb = parsed_action.verb
        
        # Default targets based on action type
        default_targets = {
            'navigate': 'website',
            'click': 'element',
            'type': 'input field',
            'wait': 'page',
            'verify': 'element',
            'select': 'option',
            'scroll': 'page',
            'submit': 'form',
            'open': 'application',
            'close': 'window'
        }
        
        return default_targets.get(verb, 'element')
    
    def _calculate_confidence(self, parsed_action: ParsedAction) -> float:
        """Calculate confidence score for the parsed action."""
        confidence = 0.5  # Base confidence
        
        # Boost confidence if we found a clear target
        if parsed_action.target:
            confidence += 0.3
        
        # Boost confidence if we found a specific value
        if parsed_action.value:
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    def enhance_trace_with_context(self, trace: TaskTrace) -> TaskTrace:
        """Enhance a task trace with contextual information and validation."""
        enhanced_steps = []
        
        for i, step in enumerate(trace.steps):
            # Add contextual information
            step.metadata['context'] = self._analyze_step_context(step, i, trace.steps)
            
            # Validate step completeness
            step.metadata['validation'] = self._validate_step(step)
            
            enhanced_steps.append(step)
        
        # Update trace metadata
        trace.metadata['enhanced'] = True
        trace.metadata['total_confidence'] = self._calculate_trace_confidence(enhanced_steps)
        
        return TaskTrace(
            task_description=trace.task_description,
            steps=enhanced_steps,
            trace_id=trace.trace_id,
            metadata=trace.metadata
        )
    
    def _analyze_step_context(self, step: TaskStep, index: int, all_steps: List[TaskStep]) -> Dict:
        """Analyze the context of a step within the overall trace."""
        context = {
            'position': 'start' if index == 0 else 'end' if index == len(all_steps) - 1 else 'middle',
            'prerequisites': [],
            'consequences': []
        }
        
        # Analyze dependencies
        if step.action == ActionType.TYPE and index > 0:
            prev_step = all_steps[index - 1]
            if prev_step.action == ActionType.CLICK:
                context['prerequisites'].append('field_focused')
        
        if step.action == ActionType.SUBMIT and index < len(all_steps) - 1:
            context['consequences'].append('form_submitted')
        
        return context
    
    def _validate_step(self, step: TaskStep) -> Dict:
        """Validate the completeness and correctness of a step."""
        validation = {
            'complete': True,
            'issues': []
        }
        
        # Check for required fields based on action type
        if step.action == ActionType.TYPE and not step.value:
            validation['complete'] = False
            validation['issues'].append('missing_value_for_type_action')
        
        if step.action == ActionType.NAVIGATE and not step.target:
            validation['complete'] = False
            validation['issues'].append('missing_target_for_navigate_action')
        
        return validation
    
    def _calculate_trace_confidence(self, steps: List[TaskStep]) -> float:
        """Calculate overall confidence for the entire trace."""
        if not steps:
            return 0.0
        
        total_confidence = sum(
            step.metadata.get('parsing_confidence', 0.5) 
            for step in steps
        )
        
        return total_confidence / len(steps)