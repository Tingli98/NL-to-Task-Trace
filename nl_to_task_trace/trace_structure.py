"""
Data structures for representing task traces and execution steps.
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import json


class ActionType(Enum):
    """Enumeration of different action types in task execution."""
    NAVIGATE = "navigate"
    CLICK = "click"
    TYPE = "type"
    WAIT = "wait"
    VERIFY = "verify"
    SELECT = "select"
    SCROLL = "scroll"
    SUBMIT = "submit"
    OPEN = "open"
    CLOSE = "close"


@dataclass
class TaskStep:
    """Represents a single step in a task execution trace."""
    action: ActionType
    target: str
    value: Optional[str] = None
    description: str = ""
    step_number: int = 0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the task step to a dictionary representation."""
        return {
            "action": self.action.value,
            "target": self.target,
            "value": self.value,
            "description": self.description,
            "step_number": self.step_number,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskStep':
        """Create a TaskStep from a dictionary representation."""
        return cls(
            action=ActionType(data["action"]),
            target=data["target"],
            value=data.get("value"),
            description=data.get("description", ""),
            step_number=data.get("step_number", 0),
            metadata=data.get("metadata", {})
        )


@dataclass
class TaskTrace:
    """Represents a complete task execution trace."""
    task_description: str
    steps: List[TaskStep]
    trace_id: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        # Auto-number steps if not already numbered
        for i, step in enumerate(self.steps, 1):
            if step.step_number == 0:
                step.step_number = i
    
    def add_step(self, step: TaskStep) -> None:
        """Add a new step to the task trace."""
        step.step_number = len(self.steps) + 1
        self.steps.append(step)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the task trace to a dictionary representation."""
        return {
            "task_description": self.task_description,
            "steps": [step.to_dict() for step in self.steps],
            "trace_id": self.trace_id,
            "metadata": self.metadata
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert the task trace to a JSON string."""
        return json.dumps(self.to_dict(), indent=indent)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskTrace':
        """Create a TaskTrace from a dictionary representation."""
        steps = [TaskStep.from_dict(step_data) for step_data in data["steps"]]
        return cls(
            task_description=data["task_description"],
            steps=steps,
            trace_id=data.get("trace_id"),
            metadata=data.get("metadata", {})
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'TaskTrace':
        """Create a TaskTrace from a JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)