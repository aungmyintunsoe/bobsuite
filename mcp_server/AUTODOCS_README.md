# AutoDocs - 12 Documentation Types Generator

## Overview

AutoDocs is a comprehensive documentation generation system that supports **12 different documentation types** for various use cases. Simply prompt the system with what you need (e.g., "generate wireframe"), and it will automatically create the appropriate documentation using AI-powered analysis.

## 🎯 Supported Documentation Types

| # | Type | Description | Use Case |
|---|------|-------------|----------|
| 1 | **user_manual** | Comprehensive user manuals | End-user documentation with installation, configuration, and usage |
| 2 | **how_to_guide** | Step-by-step how-to guides | Task-oriented guides for specific operations |
| 3 | **quick_start** | Quick-start guides | Get users up and running quickly |
| 4 | **tutorial** | Interactive tutorials | Learning-oriented documentation with exercises |
| 5 | **troubleshooting** | Troubleshooting guides | Common errors, debugging steps, and solutions |
| 6 | **user_persona** | User personas | User types, goals, pain points, and scenarios |
| 7 | **knowledge_base** | Knowledge base articles | Internal documentation and FAQs |
| 8 | **ux_design** | UX design documentation | UI components, user flows, and design principles |
| 9 | **wireframe** | Wireframe documentation | Screen layouts (ASCII art), component hierarchy, navigation |
| 10 | **requirements** | Software requirements | Functional/non-functional requirements and acceptance criteria |
| 11 | **api** | API documentation | Endpoints, parameters, return values, and examples |
| 12 | **full** | Comprehensive documentation | All types combined into one document |

## 🚀 Quick Start

### Basic Usage

```bash
# Generate wireframe documentation
python generate_docs.py wireframe path/to/file.ts

# Generate user manual
python generate_docs.py user_manual path/to/file.py

# Generate quick start guide
python generate_docs.py quick_start path/to/file.js
```

### Natural Language Prompts

You can also use natural language:

```bash
# These all work!
python generate_docs.py "generate wireframe" path/to/file.ts
python generate_docs.py "create user manual for" path/to/file.py
python generate_docs.py "i want to generate the wireframe" path/to/file.ts
```

### Programmatic Usage

```python
from lib.autodocs import AutoDocs
from watsonx_client import WatsonxClient

# Initialize
watsonx = WatsonxClient()
autodocs = AutoDocs(watsonx)

# Generate wireframe documentation
docs = await autodocs.generate_docs("path/to/file.ts", "wireframe")

# Generate user manual
docs = await autodocs.generate_docs("path/to/file.py", "user_manual")

# Generate comprehensive documentation (all types)
docs = await autodocs.generate_docs("path/to/file.js", "full")
```

## 📝 Documentation Type Details

### 1. User Manual (`user_manual`)

**What it generates:**
- Overview and purpose
- Installation instructions
- Configuration options
- Usage examples
- Common use cases
- Best practices

**Example prompt:**
```bash
python generate_docs.py user_manual src/app/actions.ts
```

### 2. How-To Guide (`how_to_guide`)

**What it generates:**
- Clear objective
- Prerequisites
- Step-by-step instructions
- Expected outcomes
- Tips and warnings

**Example prompt:**
```bash
python generate_docs.py how_to_guide lib/utils.py
```

### 3. Quick Start Guide (`quick_start`)

**What it generates:**
- Minimal setup steps
- Basic usage example
- Next steps
- Links to detailed documentation

**Example prompt:**
```bash
python generate_docs.py quick_start index.js
```

### 4. Tutorial (`tutorial`)

**What it generates:**
- Learning objectives
- Prerequisites
- Step-by-step lessons
- Practice exercises
- Summary and next steps

**Example prompt:**
```bash
python generate_docs.py tutorial components/Button.tsx
```

### 5. Troubleshooting Guide (`troubleshooting`)

**What it generates:**
- Common errors and solutions
- Debugging steps
- FAQ
- Known issues
- Support resources

**Example prompt:**
```bash
python generate_docs.py troubleshooting api/server.py
```

### 6. User Persona (`user_persona`)

**What it generates:**
- User types and roles
- Goals and motivations
- Pain points
- Technical skill level
- Use case scenarios

**Example prompt:**
```bash
python generate_docs.py user_persona app/dashboard.tsx
```

### 7. Knowledge Base Article (`knowledge_base`)

**What it generates:**
- Article title and summary
- Problem description
- Solution steps
- Related articles
- Tags and categories

**Example prompt:**
```bash
python generate_docs.py knowledge_base lib/auth.py
```

### 8. UX Design Documentation (`ux_design`)

**What it generates:**
- User interface components
- User flows
- Interaction patterns
- Accessibility considerations
- Design principles

**Example prompt:**
```bash
python generate_docs.py ux_design components/Form.tsx
```

### 9. Wireframe Documentation (`wireframe`)

**What it generates:**
- Screen layouts (ASCII art or description)
- Component hierarchy
- Navigation flow
- Interactive elements
- Responsive design notes

**Example prompt:**
```bash
python generate_docs.py wireframe pages/home.tsx
```

**Example output:**
```
+--------------------------------------------------+
|                   Balancia                      |
|                                                  |
|  Welcome, [User Name]!                           |
|                                                  |
|  [Get Balance]   [Transfer Funds]                |
|                                                  |
+--------------------------------------------------+
```

### 10. Software Requirements (`requirements`)

**What it generates:**
- Functional requirements
- Non-functional requirements
- System constraints
- Dependencies
- Acceptance criteria

**Example prompt:**
```bash
python generate_docs.py requirements api/endpoints.py
```

### 11. API Documentation (`api`)

**What it generates:**
- Endpoints/Functions
- Parameters and types
- Return values
- Error codes
- Usage examples

**Example prompt:**
```bash
python generate_docs.py api routes/users.ts
```

### 12. Comprehensive Documentation (`full`)

**What it generates:**
All of the above types combined into a single comprehensive document with sections for:
- API Documentation
- Quick Start Guide
- User Manual
- How-To Guide
- Tutorial
- Troubleshooting Guide
- Requirements Specification

**Example prompt:**
```bash
python generate_docs.py full src/main.py
```

## 🎨 Natural Language Aliases

The system understands various aliases for each documentation type:

| Type | Aliases |
|------|---------|
| user_manual | manual |
| how_to_guide | guide |
| quick_start | quickstart, quick-start |
| tutorial | tut |
| troubleshooting | troubleshoot |
| user_persona | persona |
| knowledge_base | kb |
| ux_design | ux, design |
| wireframe | wire, mockup |
| requirements | req, spec, specification |
| api | api_doc |
| full | comprehensive, all |

## 📂 Output Files

Generated documentation is saved with the following naming pattern:
```
{filename}_{doc_type}.md
```

Examples:
- `actions_wireframe.md`
- `utils_user_manual.md`
- `api_quick_start.md`

## 🔧 Advanced Usage

### Custom Output File

```bash
python generate_docs.py wireframe src/app.tsx my_custom_wireframe.md
```

### Batch Generation

```python
import asyncio
from lib.autodocs import AutoDocs
from watsonx_client import WatsonxClient

async def generate_all_docs():
    watsonx = WatsonxClient()
    autodocs = AutoDocs(watsonx)
    
    doc_types = ["wireframe", "user_manual", "api", "quick_start"]
    
    for doc_type in doc_types:
        docs = await autodocs.generate_docs("src/app.ts", doc_type)
        with open(f"output_{doc_type}.md", "w") as f:
            f.write(docs)

asyncio.run(generate_all_docs())
```

## 🎯 Use Case Examples

### For Product Managers
```bash
# Generate requirements specification
python generate_docs.py requirements features/payment.ts

# Generate user personas
python generate_docs.py user_persona app/dashboard.tsx
```

### For Designers
```bash
# Generate wireframes
python generate_docs.py wireframe pages/checkout.tsx

# Generate UX design documentation
python generate_docs.py ux_design components/Navigation.tsx
```

### For Developers
```bash
# Generate API documentation
python generate_docs.py api routes/api.ts

# Generate troubleshooting guide
python generate_docs.py troubleshooting lib/database.py
```

### For Technical Writers
```bash
# Generate user manual
python generate_docs.py user_manual src/main.py

# Generate how-to guide
python generate_docs.py how_to_guide lib/auth.py
```

### For End Users
```bash
# Generate quick start guide
python generate_docs.py quick_start index.js

# Generate tutorial
python generate_docs.py tutorial examples/basic.ts
```

## 🛠️ Testing

Run the comprehensive test suite:

```bash
# Test all 12 documentation types
python test_all_doc_types.py

# Test specific type
python generate_docs.py wireframe dataset_balancia/src/app/actions.ts
```

## 📊 Features

✅ **12 Documentation Types** - Covers all common documentation needs
✅ **Natural Language Support** - Use conversational prompts
✅ **AI-Powered** - Leverages WatsonX AI for intelligent content generation
✅ **Type-Safe** - Full type checking and validation
✅ **Flexible Output** - Markdown format with metadata
✅ **Batch Processing** - Generate multiple types at once
✅ **Extensible** - Easy to add new documentation types

## 🔍 How It Works

1. **Input**: You provide a file path and documentation type
2. **Analysis**: The system reads and analyzes the code
3. **AI Generation**: WatsonX AI generates appropriate documentation
4. **Formatting**: Content is formatted with metadata and structure
5. **Output**: Markdown file is saved with preview

## 📖 Documentation Structure

Each generated document includes:

```markdown
# {Doc Type} for {filename}
**File:** path/to/file
**Language:** TypeScript/Python/etc
**Documentation type:** {Type Name}
**Generated:** {Timestamp}

---

{AI-Generated Content}

---
*Generated by AutoDocs - {Type} Generator*
```

## 🎓 Best Practices

1. **Choose the Right Type**: Select the documentation type that matches your audience
2. **Review Output**: Always review AI-generated content for accuracy
3. **Iterate**: Generate multiple types for comprehensive coverage
4. **Customize**: Edit the output to add project-specific details
5. **Version Control**: Track documentation changes alongside code

## 🚨 Troubleshooting

### File Not Found
```bash
[ERROR] File not found: path/to/file.ts
```
**Solution**: Verify the file path is correct and the file exists

### Invalid Documentation Type
```bash
[ERROR] Invalid documentation type: invalid_type
```
**Solution**: Use one of the 12 supported types or their aliases

### Unicode Encoding Errors
The system automatically handles encoding issues by using ASCII-safe characters.

## 📞 Support

For issues or questions:
1. Check this README
2. Review generated examples in `mcp_server/`
3. Run test suite: `python test_all_doc_types.py`

## 🎉 Success Stories

**Wireframe Generation Example:**
```bash
$ python generate_docs.py wireframe src/app/actions.ts

[OK] Detected documentation type: wireframe
Generating wireframe documentation...
[SUCCESS]
Documentation saved to: actions_wireframe.md
```

Generated complete ASCII art wireframes with:
- Screen layouts
- Component hierarchy
- Navigation flow
- Responsive design notes
- Accessibility considerations

---

**Made with ❤️ by AutoDocs - Your AI Documentation Assistant**