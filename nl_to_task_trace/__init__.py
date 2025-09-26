"""
NL-to-Task-Trace: A system for converting natural language descriptions to structured task traces.
"""

__version__ = "0.1.0"
__author__ = "NL-to-Task-Trace Team"

from .trace_structure import TaskTrace, TaskStep, ActionType
from .nl_parser import NLParser
from .trace_converter import TraceConverter

__all__ = [
    "TaskTrace",
    "TaskStep", 
    "ActionType",
    "NLParser",
    "TraceConverter"
]