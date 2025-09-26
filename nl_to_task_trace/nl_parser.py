"""
Natural language parser for extracting task information from text descriptions.
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ParsedAction:
    """Represents a parsed action from natural language."""
    verb: str
    target: Optional[str] = None
    value: Optional[str] = None
    modifiers: List[str] = None
    original_text: str = ""
    
    def __post_init__(self):
        if self.modifiers is None:
            self.modifiers = []


class NLParser:
    """Parser for converting natural language task descriptions into structured actions."""
    
    def __init__(self):
        # Action verb patterns mapped to action types
        self.action_patterns = {
            'navigate': [
                r'\b(go to|navigate to|visit|open)\b',
                r'\b(browse to|access)\b'
            ],
            'click': [
                r'\b(click|press|tap|select)\b',
                r'\b(hit|choose)\b'
            ],
            'type': [
                r'\b(type|enter|input|fill)\b',
                r'\b(write|key in)\b'
            ],
            'wait': [
                r'\b(wait|pause|delay)\b',
                r'\b(hold|stay)\b'
            ],
            'verify': [
                r'\b(verify|check|confirm|ensure)\b',
                r'\b(validate|assert)\b'
            ],
            'select': [
                r'\b(select|choose|pick)\b'
            ],
            'scroll': [
                r'\b(scroll|swipe)\b'
            ],
            'submit': [
                r'\b(submit|send|post)\b'
            ],
            'open': [
                r'\b(open|launch|start)\b'
            ],
            'close': [
                r'\b(close|exit|quit)\b'
            ]
        }
        
        # Target identification patterns
        self.target_patterns = [
            r'\b(?:the\s+)?(\w+\s+button)\b',
            r'\b(?:the\s+)?(\w+\s+field)\b',
            r'\b(?:the\s+)?(\w+\s+menu)\b',
            r'\b(?:the\s+)?(\w+\s+link)\b',
            r'\b(?:the\s+)?(\w+\s+tab)\b',
            r'\b(?:the\s+)?(\w+\s+page)\b',
            r'\b(?:the\s+)?(\w+\s+form)\b',
            r'\binput\s+field\b',
            r'\btext\s+box\b',
            r'\bdropdown\b',
            r'\bcheckbox\b',
            r'\bradio\s+button\b',
        ]
        
        # Value extraction patterns
        self.value_patterns = [
            r'"([^"]+)"',  # Quoted values
            r"'([^']+)'",  # Single quoted values
            r'\bwith\s+"([^"]+)"',  # "with" clauses
            r'\bto\s+"([^"]+)"',    # "to" clauses
            r'\bas\s+"([^"]+)"',    # "as" clauses
            r'\btype\s+"([^"]+)"',  # type with quotes
            r'\benter\s+"([^"]+)"', # enter with quotes
            r'\binput\s+"([^"]+)"', # input with quotes
        ]
    
    def parse_task_description(self, description: str) -> List[ParsedAction]:
        """
        Parse a natural language task description into structured actions.
        
        Args:
            description: Natural language description of the task
            
        Returns:
            List of ParsedAction objects representing the parsed actions
        """
        # Split description into sentences/steps
        sentences = self._split_into_sentences(description)
        
        parsed_actions = []
        for sentence in sentences:
            action = self._parse_sentence(sentence)
            if action:
                parsed_actions.append(action)
        
        return parsed_actions
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences, handling common separators."""
        # Split on period, exclamation, question mark, or numbered lists
        sentences = re.split(r'[.!?]|\n\d+\.|\n[-*]', text)
        
        # Clean up and filter empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def _parse_sentence(self, sentence: str) -> Optional[ParsedAction]:
        """Parse a single sentence into a ParsedAction."""
        sentence_lower = sentence.lower()
        
        # Find action verb
        action_type = self._identify_action_type(sentence_lower)
        if not action_type:
            return None
        
        # Extract target
        target = self._extract_target(sentence_lower)
        
        # Extract value
        value = self._extract_value(sentence)
        
        # Extract modifiers
        modifiers = self._extract_modifiers(sentence_lower)
        
        return ParsedAction(
            verb=action_type,
            target=target,
            value=value,
            modifiers=modifiers,
            original_text=sentence.strip()
        )
    
    def _identify_action_type(self, sentence: str) -> Optional[str]:
        """Identify the primary action type in a sentence."""
        for action_type, patterns in self.action_patterns.items():
            for pattern in patterns:
                if re.search(pattern, sentence, re.IGNORECASE):
                    return action_type
        return None
    
    def _extract_target(self, sentence: str) -> Optional[str]:
        """Extract the target element or location from a sentence."""
        for pattern in self.target_patterns:
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                return match.group(1) if match.groups() else match.group(0)
        
        # Fallback: look for common UI element words
        ui_elements = [
            'button', 'link', 'menu', 'field', 'box', 'dropdown',
            'checkbox', 'radio', 'tab', 'page', 'form', 'input'
        ]
        
        for element in ui_elements:
            if element in sentence:
                # Try to find the element with its descriptor
                pattern = r'(\w+\s+)?' + element
                match = re.search(pattern, sentence)
                if match:
                    return match.group(0).strip()
        
        return None
    
    def _extract_value(self, sentence: str) -> Optional[str]:
        """Extract quoted values or specific input values."""
        for pattern in self.value_patterns:
            match = re.search(pattern, sentence)
            if match:
                return match.group(1)
        return None
    
    def _extract_modifiers(self, sentence: str) -> List[str]:
        """Extract modifying words that provide context."""
        modifiers = []
        
        # Location modifiers
        if 'left' in sentence:
            modifiers.append('left')
        if 'right' in sentence:
            modifiers.append('right')
        if 'top' in sentence:
            modifiers.append('top')
        if 'bottom' in sentence:
            modifiers.append('bottom')
        if 'center' in sentence:
            modifiers.append('center')
        
        # Timing modifiers
        if 'slowly' in sentence:
            modifiers.append('slowly')
        if 'quickly' in sentence:
            modifiers.append('quickly')
        if 'carefully' in sentence:
            modifiers.append('carefully')
        
        return modifiers
    
    def extract_task_title(self, description: str) -> str:
        """Extract a concise title from the task description."""
        # Take first sentence and clean it up
        first_sentence = description.split('.')[0].split('\n')[0].strip()
        
        # Remove common prefixes
        first_sentence = re.sub(r'^(task:|goal:|objective:|to\s+)', '', first_sentence, flags=re.IGNORECASE)
        
        # Capitalize and limit length
        title = first_sentence[:80] + "..." if len(first_sentence) > 80 else first_sentence
        return title.strip()