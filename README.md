# NL-to-Task-Trace

A Python library for converting natural language task descriptions into structured, executable task traces. This tool parses natural language instructions and transforms them into standardized step-by-step execution sequences that can be used for automation, testing, or documentation.

## Features

- **Natural Language Processing**: Parse task descriptions written in plain English
- **Structured Output**: Generate standardized task traces with typed actions and metadata  
- **Multiple Output Formats**: JSON serialization and human-readable formats
- **Contextual Enhancement**: Analyze step dependencies and add contextual information
- **Command Line Interface**: Easy-to-use CLI for batch processing
- **Extensible Architecture**: Modular design for easy customization and extension

## Installation

```bash
# Clone the repository
git clone https://github.com/Tingli98/NL-to-Task-Trace.git
cd NL-to-Task-Trace

# Install dependencies (optional - basic functionality works without external deps)
pip install -r requirements.txt
```

## Quick Start

### Python API

```python
from nl_to_task_trace import TraceConverter

# Create converter instance
converter = TraceConverter()

# Convert natural language to structured trace
description = "Navigate to login page. Enter username and password. Click submit button."
trace = converter.convert_description_to_trace(description)

# Output as JSON
print(trace.to_json())

# Enhance with contextual information
enhanced_trace = converter.enhance_trace_with_context(trace)
```

### Command Line Interface

```bash
# Convert text directly
python cli.py "Click the login button and enter credentials"

# Process from file
python cli.py --file examples/login_task.txt --enhance

# Save to file with JSON format
python cli.py --file examples/shopping_task.txt --format json --output result.json
```

## Task Trace Structure

Each task trace consists of:

- **Task Description**: Extracted title/summary of the task
- **Steps**: Ordered sequence of actions with:
  - **Action Type**: Standardized action (CLICK, TYPE, NAVIGATE, etc.)
  - **Target**: Element or location the action applies to
  - **Value**: Input value (for TYPE actions)
  - **Description**: Original natural language description
  - **Metadata**: Confidence scores, parsing info, context
- **Trace ID**: Unique identifier
- **Metadata**: Overall trace information and statistics

## Supported Action Types

- `NAVIGATE`: Go to pages, URLs, or locations
- `CLICK`: Click buttons, links, or interactive elements  
- `TYPE`: Enter text into input fields
- `SELECT`: Choose options from dropdowns or lists
- `VERIFY`: Check conditions or validate results
- `WAIT`: Pause or wait for conditions
- `SCROLL`: Scroll through content
- `SUBMIT`: Submit forms or data
- `OPEN`: Launch applications or files
- `CLOSE`: Close windows or applications

## Examples

### Login Task
**Input**: "Go to the login page. Click on the username field and type 'john.doe@example.com'. Click on the password field and enter 'mypassword123'. Click the login button. Verify that the dashboard page loads successfully."

**Output**:
```
Task: Go to the login page
Trace ID: aa65c5ff
--------------------------------------------------
1. NAVIGATE
   Target: login page
   Description: Go to the login page

2. CLICK  
   Target: username field
   Description: Click on the username field and type 'john.doe@example.com'

3. CLICK
   Target: password field  
   Value: mypassword123
   Description: Click on the password field and enter 'mypassword123'

4. CLICK
   Target: login button
   Description: Click the login button

5. VERIFY
   Target: dashboard page
   Description: Verify that the dashboard page loads successfully
```

### E-commerce Task
**Input**: "Navigate to the shopping website. Search for 'wireless headphones'. Click on the first product. Add to cart and checkout."

**Output**: Structured trace with NAVIGATE → TYPE → CLICK → CLICK → CLICK actions

## API Reference

### TraceConverter

Main class for converting natural language to task traces.

#### Methods

- `convert_description_to_trace(description: str, trace_id: Optional[str] = None) -> TaskTrace`
  - Convert natural language description to structured trace
  
- `enhance_trace_with_context(trace: TaskTrace) -> TaskTrace`  
  - Add contextual analysis and validation to existing trace

### TaskTrace

Represents a complete task execution sequence.

#### Properties
- `task_description: str` - Task title/summary
- `steps: List[TaskStep]` - Ordered execution steps  
- `trace_id: Optional[str]` - Unique identifier
- `metadata: Dict[str, Any]` - Additional information

#### Methods
- `to_json(indent: int = 2) -> str` - Serialize to JSON
- `to_dict() -> Dict[str, Any]` - Convert to dictionary
- `from_json(json_str: str) -> TaskTrace` - Deserialize from JSON

### TaskStep

Represents a single action in the task sequence.

#### Properties
- `action: ActionType` - Type of action to perform
- `target: str` - Element or location for the action
- `value: Optional[str]` - Input value (for TYPE actions)
- `description: str` - Original natural language description
- `step_number: int` - Position in sequence
- `metadata: Dict[str, Any]` - Additional step information

## Testing

Run the test suite:

```bash
python -m unittest tests.test_nl_to_task_trace -v
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality  
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.