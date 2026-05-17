# Comprehensive Documentation for Visualizer Engine Core
**File:** mcp_server/lib/visualizer/core.py
**Language:** Python
**Documentation type:** Comprehensive Documentation
**Generated:** 2026-05-17T09:27:32.348892Z

---

## API Documentation

### VisualizerEngine Class

Production-grade visualization generator for project onboarding.

#### Methods

**`__init__(watsonx_client)`**
- Initialize the Visualizer Engine
- Parameters:
  - `watsonx_client`: WatsonxClient instance for AI analysis

**`async generate_dependency_chain(project_path, output_path=None, max_depth=3, include_external=False) -> Dict[str, Any]`**
- Generate visual dependency chain diagram
- Parameters:
  - `project_path`: Path to project directory
  - `output_path`: Optional custom output path
  - `max_depth`: Maximum depth for dependency analysis (default: 3)
  - `include_external`: Include external dependencies (default: False)
- Returns: Dictionary with success status, diagram type, markdown, mermaid code, and statistics

**`async generate_feature_flow(project_path, feature_name=None, output_path=None) -> Dict[str, Any]`**
- Generate feature flow sequence diagram
- Parameters:
  - `project_path`: Path to project directory
  - `feature_name`: Optional specific feature to analyze
  - `output_path`: Optional custom output path
- Returns: Dictionary with success status, diagram type, markdown, mermaid code, and features analyzed

**`async generate_project_concept(project_path, output_path=None) -> Dict[str, Any]`**
- Generate high-level project concept visualization
- Parameters:
  - `project_path`: Path to project directory
  - `output_path`: Optional custom output path
- Returns: Dictionary with success status, diagram type, markdown, mermaid code, and component count

---

## Quick Start Guide

### Minimal Setup Steps

1. **Install dependencies**
   ```bash
   pip install aiohttp pydantic mermaid-cli
   ```

2. **Get WatsonX client**
   ```python
   from watsonx_sdk import WatsonXClient
   wx = WatsonXClient(api_key="YOUR_API_KEY", base_url="https://api.watsonx.ibm.com")
   ```

3. **Create Visualizer instance**
   ```python
   engine = VisualizerEngine(wx)
   ```

4. **Configure output folder (optional)**
   ```python
   output_dir = Path("./visuals")
   ```

### Basic Usage Example

```python
import asyncio
from visualizer_engine import VisualizerEngine

async def main():
    # Initialize
    wx = WatsonXClient(api_key="YOUR_API_KEY")
    engine = VisualizerEngine(wx)

    # Generate Dependency Chain
    result = await engine.generate_dependency_chain(
        project_path="/path/to/your/project",
        output_path=None,
        max_depth=3,
        include_external=True
    )
    print("✅ Dependency chain:", result)

    # Generate Feature Flow
    feature_result = await engine.generate_feature_flow(
        project_path="/path/to/your/project",
        feature_name="User Registration"
    )
    print("✅ Feature flow:", feature_result)

    # Generate Project Concept
    concept_result = await engine.generate_project_concept(
        project_path="/path/to/your/project"
    )
    print("✅ Project concept:", concept_result)

if __name__ == "__main__":
    asyncio.run(main())
```

### Expected Output

- `dependency-chain_2025-08-21_14-30-00.md` - Mermaid graph with module table
- `feature-flow_User_Registration_2025-08-21_14-30-01.md` - Sequence diagram
- `project-concept_AppCore_2025-08-21_14-30-02.md` - Conceptual architecture
- PNG images saved alongside Markdown files

### Next Steps

1. Integrate with conversation platform
2. Add new diagram types (e.g., Data Flow)
3. Swap LLM provider (OpenAI, Claude)
4. Cache WatsonX responses
5. Support other languages (Java, Go, TypeScript)
6. Run in Docker container
7. Add CI-integrated visual checks

### Documentation Links

- WatsonX SDK: https://ibm.github.io/watsonx-sdk-python/
- Mermaid CLI: https://mermaid-js.github.io/mermaid-cli/
- Python AST: https://docs.python.org/3/library/ast.html
- Mermaid Syntax: https://mermaid-js.github.io/mermaid/#/

---

## User Manual

### Overview and Purpose

The Visualizer Engine automatically generates visual diagrams to aid in understanding project structure, dependencies, feature flows, and system concepts. It leverages AI to analyze project contexts and generate meaningful visual representations using Mermaid syntax.

### Installation Instructions

1. Clone repository with Visualizer Engine code
2. Create virtual environment and install dependencies
3. Configure Watsonx client credentials
4. Execute Visualizer Engine script with appropriate parameters

### Configuration Options

- **`project_path`**: Path to project directory to visualize
- **`output_path`**: Directory/file path for generated diagrams
- **`max_depth`**: Maximum depth for dependency chain analysis (default: 3)
- **`include_external`**: Include external dependencies (default: False)
- **`feature_name`**: Specific feature to analyze in feature flow

### Usage Examples

#### Dependency Chain Diagram
```python
engine = VisualizerEngine(watsonx_client)
result = await engine.generate_dependency_chain(
    project_path='/path/to/project',
    output_path='/path/to/output',
    max_depth=3,
    include_external=True
)
print(result)
```

#### Feature Flow Diagram
```python
engine = VisualizerEngine(watsonx_client)
result = await engine.generate_feature_flow(
    project_path='/path/to/project',
    feature_name='User Authentication',
    output_path='/path/to/output'
)
print(result)
```

#### Project Concept Diagram
```python
engine = VisualizerEngine(watsonx_client)
result = await engine.generate_project_concept(
    project_path='/path/to/project',
    output_path='/path/to/output'
)
print(result)
```

### Common Use Cases

- **Project Onboarding**: Generate visual diagrams for new team members
- **System Architecture Documentation**: Create comprehensive architecture diagrams
- **Dependency Management**: Analyze and visualize dependencies

### Best Practices

- Regularly update Visualizer Engine for latest features
- Customize prompts for project-specific needs
- Manually review generated diagrams for accuracy
- Integrate with CI/CD pipeline for automatic updates

---

## How-To Guide

### Objective
Create production-grade visualization generator for project onboarding with dependency chains, feature flows, and concept maps.

### Prerequisites
- Python 3.x
- Required libraries: ast, re, json, pathlib, typing, collections
- Watsonx client for AI analysis

### Step-by-Step Instructions

1. **Import necessary libraries**
   ```python
   import ast, re, json
   from pathlib import Path
   from typing import Dict, Any, List, Optional, Set
   from collections import defaultdict
   ```

2. **Create VisualizerEngine instance**
   ```python
   watsonx_client = WatsonxClient()
   visualizer_engine = VisualizerEngine(watsonx_client)
   ```

3. **Generate dependency chain**
   ```python
   project_path = "/path/to/project"
   output_path = "/path/to/output"
   result = visualizer_engine.generate_dependency_chain(
       project_path, 
       output_path,
       max_depth=3,
       include_external=False
   )
   ```

4. **Generate feature flow map**
   ```python
   result = visualizer_engine.generate_feature_flow(
       project_path,
       feature_name="Feature Name",
       output_path=output_path
   )
   ```

5. **Generate project concept**
   ```python
   result = visualizer_engine.generate_project_concept(
       project_path,
       output_path=output_path
   )
   ```

### Expected Outcomes

- Dependency chain returns: success, diagram_type, markdown, mermaid, saved_to, stats
- Feature flow returns: success, diagram_type, markdown, mermaid, saved_to, features_analyzed
- Project concept returns: success, diagram_type, markdown, mermaid, saved_to, image_saved_to, components

### Tips and Warnings

- Ensure project path exists and is accessible
- If output_path not provided, diagrams won't be saved to file
- Adjust max_depth based on project complexity
- Set include_external=True to include external dependencies
- Specify feature_name to analyze particular feature
- Generated diagrams saved as Markdown by default
- Use save_mermaid_as_png for PNG images
- Handle exceptions during generation process
- Customize prompts and rendering logic for specific needs

---

## Tutorial

### Learning Objectives
1. Understand Visualizer Engine architecture
2. Learn to analyze project dependencies
3. Map feature flows using AI-assisted analysis
4. Visualize project concepts with architectural diagrams
5. Work with AST and regular expressions
6. Integrate with external AI services

### Prerequisites
- Basic Python programming
- Familiarity with async programming
- Understanding of project structures
- Knowledge of diagram types
- Python 3.x installed
- Access to Watsonx API

### Step-by-Step Lessons

#### Lesson 1: Setting Up Environment
1. Install Python 3.x
2. Create virtual environment
3. Install required packages
4. Set up Watsonx API credentials
5. Clone Visualizer Engine repository

#### Lesson 2: Understanding Architecture
1. Examine VisualizerEngine class structure
2. Study initialization process
3. Understand dependency analysis flow
4. Learn about AI integration points
5. Explore diagram generation pipeline

#### Lesson 3: Dependency Chain Analysis
1. Study _analyze_dependencies method
2. Understand AST parsing for imports
3. Learn about dependency graph building
4. Practice with different max_depth values
5. Explore external dependency handling

#### Lesson 4: Feature Flow Mapping
1. Analyze _analyze_feature_flow_with_ai method
2. Understand AI prompt construction
3. Learn about sequence diagram generation
4. Practice mapping different features
5. Explore Mermaid syntax for sequences

#### Lesson 5: Project Concept Visualization
1. Study _analyze_project_concept_with_ai method
2. Understand high-level architecture analysis
3. Learn about component identification
4. Practice with different project types
5. Explore conceptual diagram patterns

#### Lesson 6: Mermaid Diagram Generation
1. Examine Mermaid syntax basics
2. Understand diagram type selection
3. Learn about rendering to PNG
4. Practice customizing diagram styles
5. Explore advanced Mermaid features

#### Lesson 7: Error Handling and Optimization
1. Analyze error handling strategies
2. Understand performance optimization
3. Learn about caching mechanisms
4. Practice debugging diagram generation
5. Explore logging and monitoring

### Practice Exercises

1. **Dependency Chain Exploration**
   - Create sample project with 3 modules
   - Run dependency_chain generator
   - Verify output shows correct relationships
   - Add external library import
   - Confirm external dependency appears

2. **Feature Flow Mapping**
   - Create feature module with database operations
   - Run feature_flow generator
   - Check sequence diagram shows correct flow
   - Add external API call
   - Verify external service appears

3. **Project Concept Visualization**
   - Create README describing project purpose
   - Run project_concept generator
   - Check concept diagram includes components
   - Add database component
   - Verify database appears in diagram

### Summary
You've learned about Visualizer Engine architecture, dependency analysis, feature flow mapping, project concept visualization, AST parsing, and AI integration.

### Next Steps
1. Experiment with different project structures
2. Modify prompts for different analysis results
3. Customize diagram outputs in renderers
4. Add new analysis components
5. Integrate into CI/CD pipeline

---

## Troubleshooting Guide

### Common Errors and Solutions

1. **ModuleNotFoundError: No module named 'lib.utils'**
   - Error: lib directory not in Python path
   - Solution: Ensure lib is in PYTHONPATH or run from project root

2. **ImportError: cannot import name 'DiagramGenerationError'**
   - Error: DiagramGenerationError class missing
   - Solution: Verify renderers.py contains DiagramGenerationError class

3. **AttributeError: 'VisualizerEngine' object has no attribute 'watsonx'**
   - Error: watsonx_client not passed to constructor
   - Solution: Instantiate with valid watsonx client object

4. **TypeError: 'str' object is not callable**
   - Error: target_path.iterdir() called as function
   - Solution: Ensure target_path is Path object, not string

5. **FileNotFoundError: No such file or directory**
   - Error: Specified file path doesn't exist
   - Solution: Verify file path is correct and file exists

### Debugging Steps

1. **Check Python Environment**
   - Verify Python version and installed packages
   - Ensure lib directory in Python path

2. **Verify File Paths**
   - Confirm all file paths exist and are accessible
   - Use Path.resolve() for absolute paths

3. **Inspect Variable Values**
   - Use print statements or debugger
   - Check _get_file_content return values

4. **Handle Exceptions**
   - Wrap code in try-except blocks
   - Print/log exception messages

5. **Test Individual Components**
   - Isolate and test individual functions
   - Use unit tests for verification

### FAQ

**Q: What is the purpose of VisualizerEngine?**
A: Generate visual diagrams for project onboarding including dependency chains, feature flows, and concept visualizations.

**Q: How do I instantiate VisualizerEngine?**
A: Pass valid watsonx client: `engine = VisualizerEngine(watsonx_client)`

**Q: What methods are available?**
A: generate_dependency_chain, generate_feature_flow, generate_project_concept

**Q: How do I save generated diagrams?**
A: Use output_path parameter in respective methods

**Q: What diagram types are supported?**
A: dependency_chain, feature_flow, project_concept

### Known Issues

1. **DiagramGenerationError not defined**
   - Description: Class missing from renderers
   - Workaround: Ensure class properly defined

2. **watsonx client not available**
   - Description: Client not properly initialized
   - Workaround: Verify client initialization

3. **max_depth parameter not respected**
   - Description: Method doesn't limit depth
   - Workaround: Modify _analyze_dependencies method

4. **External dependencies not included**
   - Description: External deps not in diagram
   - Workaround: Set include_external=True

5. **Async methods not awaited**
   - Description: Methods not awaited properly
   - Workaround: Use await when calling methods

### Support Resources

- **Documentation**: Project documentation for detailed information
- **GitHub Repository**: Latest updates and issues
- **Issue Tracker**: Report bugs or request features
- **Community Forum**: Ask questions and share experiences
- **Contact Support**: Email support team for assistance

---

## Requirements Specification

### Functional Requirements

1. **Dependency Chain Generation**
   - Analyze project dependencies
   - Generate visual dependency graph
   - Support configurable depth
   - Include/exclude external dependencies
   - Save as Markdown and PNG

2. **Feature Flow Mapping**
   - Analyze feature implementations
   - Generate sequence diagrams
   - Support specific feature selection
   - Show component interactions
   - Save as Markdown and PNG

3. **Project Concept Visualization**
   - Analyze overall project structure
   - Generate conceptual architecture
   - Identify key components
   - Show high-level relationships
   - Save as Markdown and PNG

### Non-Functional Requirements

1. **Performance**
   - Generate diagrams within 30 seconds
   - Handle projects with 1000+ files
   - Efficient AST parsing

2. **Scalability**
   - Support multiple concurrent requests
   - Handle large codebases
   - Optimize memory usage

3. **Usability**
   - Clear error messages
   - Intuitive API
   - Comprehensive documentation

4. **Reliability**
   - Graceful error handling
   - Consistent output format
   - Robust file operations

### System Constraints

1. Implemented in Python 3.x
2. Use Watsonx for AI analysis
3. Generate Mermaid diagrams
4. Support PNG rendering
5. Async operation support

### Dependencies

1. **Python Standard Library**: ast, re, json, pathlib, typing, collections
2. **External Libraries**: aiohttp, pydantic, mermaid-cli
3. **AI Service**: Watsonx client
4. **Internal Modules**: lib.utils, lib.visualizer.prompts, lib.visualizer.renderers

### Acceptance Criteria

1. Successfully generate dependency chain diagrams
2. Successfully generate feature flow diagrams
3. Successfully generate project concept diagrams
4. Save diagrams in Markdown and PNG formats
5. Handle errors gracefully with informative messages
6. Support configurable parameters
7. Generate diagrams within performance criteria
8. Work with various project structures
9. Integrate with AI services successfully
10. Provide comprehensive documentation