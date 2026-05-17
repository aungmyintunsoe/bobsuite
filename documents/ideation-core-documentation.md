# Comprehensive Documentation for Ideation Engine Core
**File:** mcp_server/lib/ideation/core.py
**Language:** Python
**Documentation type:** Comprehensive Documentation
**Generated:** 2026-05-17T09:25:42.694345Z

---

## API Documentation

### IdeationEngine Class

Transforms IBM Bob into a proactive Technical Product Manager through AI-driven feature planning.

#### Methods

**`__init__(watsonx_client)`**
- Initialize the Ideation Engine
- Parameters:
  - `watsonx_client`: WatsonxClient instance for AI operations

**`get_framework(include_examples=True) -> Dict[str, Any]`**
- Retrieve the 7-pillar ideation framework
- Parameters:
  - `include_examples`: Include example answers for each pillar (default: True)
- Returns: Dictionary containing framework structure

**`format_framework_for_display() -> str`**
- Format the framework as readable markdown
- Returns: Markdown-formatted framework guide

**`async synthesize_prd(conversation_data, project_name=None, output_path=None) -> Dict[str, Any]`**
- Generate comprehensive PRD from conversation data
- Parameters:
  - `conversation_data`: Structured conversation data or transcript
  - `project_name`: Optional project/feature name
  - `output_path`: Optional custom path to save PRD
- Returns: Dictionary with success status, PRD markdown, metadata, and file path

---

## Quick Start Guide

### Minimal Setup Steps

1. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**
   Set up Watsonx AI access credentials

3. **Create WatsonxClient and initialize engine**
   ```python
   from ibm_watsonx_ai import WatsonxClient
   
   watsonx = WatsonxClient(api_key="YOUR_API_KEY", url="https://api.ibm.com/watsonx/v1")
   ideation = IdeationEngine(watsonx_client=watsonx)
   ```

### Basic Usage Example

```python
# Get framework
framework = ideation.get_framework(include_examples=True)
print(ideation.format_framework_for_display())

# Prepare conversation data
conversation = {
    "pillars": {
        "vision": "Create a mobile app for ordering coffee",
        "user": "Coffee shop customers",
        "problem": "Long lines and lack of customization options",
        "solution": "Mobile ordering with personalized drink recommendations",
        "competition": "Starbucks app, Dunkin' app",
        "metrics": "Order volume, customer satisfaction"
    }
}

# Synthesize PRD
result = await ideation.synthesize_prd(
    conversation_data=conversation,
    project_name="Mobile Coffee Order"
)
print(result["prd_markdown"])
```

### Next Steps

1. Integrate with conversation platform (Slack, Teams, etc.)
2. Implement user authentication and permissions
3. Add CI/CD pipeline for framework updates
4. Explore advanced Watsonx.ai features
5. Set up monitoring and logging for production

### Detailed Documentation Links

- WatsonxClient: https://ibm.github.io/watsonx-python-client/
- Framework definition: framework.py
- Validators: validators.py
- Formatters: formatters.py
- Utilities: lib/utils.py

---

## User Manual

### Overview and Purpose

The Ideation Engine transforms IBM Bob into a proactive Technical Product Manager by orchestrating:
- Framework retrieval (7-pillar ideation framework)
- Input validation
- PRD synthesis via watsonx.ai
- Output formatting
- File saving

### Installation Instructions

1. Ensure Python is installed
2. Clone repository or download code files
3. Install dependencies: `pip install -r requirements.txt`
4. Set up watsonx.ai client with credentials
5. Place Ideation Engine code in project directory

### Configuration Options

**Framework Retrieval:**
- `include_examples`: Include example answers for each pillar (default: True)

**PRD Synthesis:**
- `conversation_data`: Structured conversation data or transcript
- `project_name`: Optional project/feature name
- `output_path`: Optional custom path to save PRD

### Usage Examples

#### Framework Retrieval
```python
from ideation_engine import IdeationEngine

engine = IdeationEngine(watsonx_client)
framework = engine.get_framework(include_examples=True)
print(framework)
```

#### PRD Synthesis
```python
from ideation_engine import IdeationEngine

engine = IdeationEngine(watsonx_client)
conversation_data = {
    "pillars": {
        "Pillar1": "Example data",
        "Pillar2": "Example data"
    }
}
result = await engine.synthesize_prd(
    conversation_data,
    project_name="Sample Project"
)
print(result)
```

### Common Use Cases

- **Automated PRD Creation**: Generate PRDs from structured conversation data
- **Framework Guidance**: Guide product managers through ideation process
- **Input Validation**: Ensure quality and consistency of input data

### Best Practices

- **Structured Data**: Ensure conversation data is structured and consistent
- **Framework Utilization**: Leverage 7-pillar framework for comprehensive coverage
- **Output Management**: Use clear project names and output paths
- **Error Handling**: Implement robust error handling for PRD synthesis

---

## How-To Guide

### Objective
Create a production-ready Ideation Engine that orchestrates framework retrieval, input validation, AI-driven PRD synthesis, and output formatting/file saving.

### Prerequisites
- Python 3.8+ environment
- Installed dependencies
- Configured watsonx.ai client
- Proper logging configuration

### Step-by-Step Instructions

1. **Environment Setup**
   ```bash
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Import and Initialize**
   ```python
   from ideation_engine import IdeationEngine
   watsonx_client = WatsonXClient(...)
   engine = IdeationEngine(watsonx_client)
   ```

3. **Framework Retrieval**
   ```python
   # With examples
   framework = engine.get_framework()
   
   # Without examples
   framework = engine.get_framework(include_examples=False)
   
   # Display as markdown
   markdown_guide = engine.format_framework_for_display()
   print(markdown_guide)
   ```

4. **Prepare Conversation Data**
   ```python
   conversation_data = {
       "pillars": {
           "business_value": {"answers": ["..."]},
           "user_stories": {"answers": ["..."]},
           ...
       },
       "context": {"additional_info": "..." }
   }
   ```

5. **PRD Synthesis**
   ```python
   result = await engine.synthesize_prd(
       conversation_data=conversation_data,
       project_name="My New Feature",
       output_path="output/prd.txt"
   )
   ```

6. **Handling Results**
   ```python
   if result["success"]:
       print("PRD generated!")
       print(result["prd_markdown"])
       print(f"Saved to: {result['file_path']}")
   else:
       print("Error:", result["error"])
       print("Suggestions:", result["suggestions"])
   ```

7. **Customize Output**
   - Specify custom output path in `synthesize_prd`
   - AI will suggest optimal path if none provided

8. **Logging and Debugging**
   - Engine uses logger (`get_logger("ideation-engine")`)
   - Check logs for detailed information
   - Increase log verbosity for debugging

### Expected Outcomes
- Markdown-formatted framework guide
- Comprehensive PRD document from conversation data
- PRD saved to specified or AI-determined file path
- Detailed success or error messages with suggestions

### Tips and Warnings
- Always validate conversation data before synthesis
- Provide meaningful project names
- Use `include_examples` flag strategically
- Leverage logging system to monitor operations
- Implement retry mechanism for transient errors
- Ensure watsonx.ai client is properly authenticated
- Be mindful of rate limits
- Framework examples are for guidance only
- Large conversation data may increase processing time
- Always review generated PRD for accuracy

---

## Tutorial

### Learning Objectives
1. Understand Ideation Engine architecture
2. Learn to retrieve and display 7-pillar framework
3. Master input validation techniques
4. Gain experience synthesizing PRDs with AI
5. Practice output formatting and file saving
6. Explore error handling and logging mechanisms

### Prerequisites
- Basic Python programming
- Familiarity with async programming
- Understanding of JSON data structures
- Knowledge of markdown formatting
- Basic AI concepts and prompt engineering
- Python 3.9+ installed
- Access to Watsonx.ai API
- IDE or text editor
- Git for version control (recommended)

### Step-by-Step Lessons

#### Lesson 1: Setting Up Development Environment
1. Install Python 3.9 or later
2. Create virtual environment
3. Install required packages
4. Set up Watsonx.ai API credentials
5. Clone Ideation Engine repository

#### Lesson 2: Understanding Architecture
1. Open `ideation_engine.py` in IDE
2. Examine class structure and key methods
3. Study initialization process
4. Trace flow from framework retrieval to PRD synthesis
5. Understand separation of concerns

#### Lesson 3: Working with Ideation Framework
1. Explore `get_framework()` method
2. Understand 7-pillar framework structure
3. Practice modifying framework structure
4. Learn to include/exclude examples
5. Study markdown formatting

#### Lesson 4: Validating Conversation Data
1. Analyze `validate_conversation_data()` function
2. Understand validation rules and error handling
3. Practice creating valid/invalid data structures
4. Explore error formatting
5. Learn importance of input validation

#### Lesson 5: Synthesizing PRDs with AI
1. Study `synthesize_prd()` method
2. Understand async workflow
3. Explore conversation data processing
4. Practice with different data types
5. Learn about sample PRDs role
6. Understand project name influence

#### Lesson 6: Output Formatting and File Saving
1. Examine `format_prd_output()` function
2. Understand metadata incorporation
3. Practice specifying custom output paths
4. Learn about AI-driven path determination
5. Study file saving mechanism

#### Lesson 7: Error Handling and Logging
1. Analyze error handling strategy
2. Understand different error types
3. Explore logging system configuration
4. Practice triggering error scenarios
5. Learn importance of detailed error reporting

### Practice Exercises

1. **Framework Customization**
   - Add new pillar to framework
   - Create markdown file with updated framework
   - Toggle example inclusion
   - Challenge: Implement dynamic pillar reordering

2. **Conversation Data Validation**
   - Create JSON with invalid data
   - Write script to load and validate
   - Modify validation logic
   - Create unit tests
   - Challenge: Implement auto-correction feature

3. **PRD Synthesis**
   - Prepare sample conversation transcript
   - Write script to synthesize PRD
   - Experiment with different project names
   - Modify synthesis prompt
   - Challenge: Generate multiple PRD versions

4. **Output Customization**
   - Add table of contents to PRD
   - Create custom markdown template
   - Save PRDs to different formats
   - Implement version control
   - Challenge: Create web interface for preview

5. **Error Handling Improvement**
   - Identify unhandled edge case
   - Modify code to handle case
   - Create unit tests
   - Create user-friendly error messages
   - Challenge: Implement automatic retry system

### Summary
You've learned about Ideation Engine architecture, framework retrieval, input validation, PRD synthesis, output formatting, and error handling. You've gained hands-on experience through exercises in customization, validation, synthesis, formatting, and error handling.

### Next Steps
1. Integrate with project management tools
2. Develop user interface for stakeholders
3. Implement dashboard for metrics tracking
4. Explore advanced AI prompt engineering
5. Set up CI/CD for Ideation Engine
6. Research additional AI capabilities
7. Consider contributing to open-source project

---

## Troubleshooting Guide

### Common Errors and Solutions

1. **Invalid Project Name**
   - Error: "Invalid project name provided"
   - Solution: Use only alphanumeric characters, hyphens, and underscores

2. **Validation Errors in Conversation Data**
   - Error: Various validation errors
   - Solution: Ensure data follows expected structure, review `validate_conversation_data` function

3. **Error Loading Sample PRD Template**
   - Error: "Error loading sample PRD"
   - Solution: Check file path and permissions, ensure file exists

4. **Error Generating PRD with Watsonx.ai**
   - Error: "Error generating PRD with watsonx"
   - Solution: Verify client configuration and permissions, check input data

5. **Failed to Save PRD to File**
   - Error: "Failed to save PRD to file"
   - Solution: Ensure output path is writable, check disk space and permissions

### Debugging Steps

1. **Enable Detailed Logging**
   ```python
   logger.setLevel(logging.DEBUG)
   ```

2. **Check Input Data**
   - Validate structure and content before passing to `synthesize_prd`

3. **Review Watsonx Client Configuration**
   - Ensure correct initialization with credentials

4. **Inspect Output Paths**
   - Verify path correctness and accessibility

5. **Traceback Analysis**
   - Review traceback to pinpoint error location

### FAQ

**Q: What is the Ideation Engine?**
A: Tool that transforms IBM Bob into proactive Technical Product Manager, orchestrating framework retrieval, validation, PRD synthesis, and output formatting.

**Q: How do I initialize the Ideation Engine?**
A: Create instance with WatsonxClient:
```python
engine = IdeationEngine(watsonx_client)
```

**Q: How do I retrieve the 7-pillar framework?**
A: Use `get_framework` method:
```python
framework = engine.get_framework(include_examples=True)
```

**Q: How do I format framework for display?**
A: Use `format_framework_for_display` method:
```python
markdown_framework = engine.format_framework_for_display()
```

**Q: How do I synthesize a PRD?**
A: Use `synthesize_prd` method:
```python
result = await engine.synthesize_prd(conversation_data, project_name="My Project")
```

### Known Issues

1. **Performance Bottlenecks**
   - PRD synthesis can be slow for large datasets
   - Consider optimizing data processing pipeline

2. **AI Model Limitations**
   - Watsonx.ai may not always generate accurate PRDs
   - Continuous improvements needed

3. **File Saving Issues**
   - Occasional failures due to permissions or disk space

### Support Resources

1. **Documentation**: Official documentation for detailed information
2. **Community Forums**: Join forums for help from other users
3. **Contact Support**: Email or support portal for unresolved issues
4. **Bug Reporting**: GitHub issue tracker with detailed descriptions
5. **Feature Requests**: Feature request portal with clear use cases

---

## Requirements Specification

### Functional Requirements

1. **Framework Retrieval**
   - Retrieve 7-pillar ideation framework
   - Provide option to include example answers
   - Format framework as readable markdown

2. **PRD Synthesis**
   - Generate comprehensive PRD from conversation data
   - Validate project name if provided
   - Validate conversation data with detailed error handling
   - Load sample PRD template for reference
   - Generate PRD using watsonx.ai
   - Determine output path (AI-driven or user-specified)
   - Save PRD to file
   - Prepare metadata (timestamp, project name, pillar count, file status, path)
   - Format final PRD output with metadata

3. **Error Handling**
   - Handle and report errors during PRD synthesis
   - Provide error messages with correction suggestions

### Non-Functional Requirements

1. **Performance**
   - Respond to framework retrieval within 1 second
   - Generate PRDs within 30 seconds on average

2. **Scalability**
   - Handle multiple concurrent PRD generation requests

3. **Security**
   - Not store sensitive user data or conversation content

4. **Usability**
   - Provide clear error messages and suggestions
   - Format outputs in user-friendly markdown

### System Constraints

1. Implemented in Python 3.8 or later
2. Use watsonx.ai service for PRD synthesis
3. Rely on provided libraries (lib.ideation.*)
4. No new external dependencies beyond specified

### Dependencies

1. **Watsonx.ai service** for PRD synthesis
2. **Libraries and modules:**
   - lib.ideation.framework
   - lib.ideation.validators
   - lib.ideation.formatters
   - lib.utils
3. **Python standard library** and third-party libraries in requirements

### Acceptance Criteria

1. Successfully retrieve 7-pillar framework when requested
2. Provide well-formatted markdown with/without examples
3. Generate comprehensive PRD from valid data and project name
4. Validate data and names with clear error messages
5. Generate PRDs within performance criteria
6. Save generated PRD to determined output path
7. Include relevant metadata in PRD output
8. Handle and report errors with informative messages
9. Implemented in Python 3.8+ without new dependencies
10. Tested to meet functional and non-functional requirements