# 🔄 Feature Flow Map — `mcp_server`
> Generated: 2026-05-17T10:49:12.619423Z

## 📊 Summary

**Features Analyzed:** 4

## 🔀 Execution Sequence

```mermaid
%%{init: {'theme': 'default', 'themeVariables': { 'background': '#ffffff'}}}%%
sequenceDiagram
    autonumber
    participant p_0 as AutoDocs
    participant p_1 as IdeationEngine
    participant p_2 as QASentry
    actor p_3 as 👤 User
    participant p_4 as VisualizerEngine
    participant p_5 as autodocs/core
    participant p_6 as autodocs/generators
    participant p_7 as formatters
    participant p_8 as ideation/core
    participant p_9 as ideation/formatters
    participant p_10 as ideation/framework
    participant p_11 as qa_sentry/agents
    participant p_12 as qa_sentry/core
    participant p_13 as qa_sentry/reporting
    participant p_14 as visualizer/core
    participant p_15 as visualizer/prompts
    participant p_16 as server

    rect rgb(59,130,246,0.1)
    Note right of p_0: 🔷 Code Quality Analysis
    p_3->>+p_16: Uploads code
    p_16-->>-p_3: ✓ done
    p_16->>+p_12: Initializes QASentry
    p_12-->>-p_16: ✓ done
    p_2->>+p_11: Analyzes code
    p_11-->>-p_2: ✓ done
    p_2->>+p_13: Generates quality report
    p_13-->>-p_2: ✓ done
    p_16->>+p_3: Returns analysis results
    p_3-->>-p_16: ✓ done
    end

    rect rgb(139,92,246,0.1)
    Note right of p_0: 🔷 Documentation Generation
    p_3->>+p_16: Requests documentation
    p_16-->>-p_3: ✓ done
    p_16->>+p_5: Initializes AutoDocs
    p_5-->>-p_16: ✓ done
    p_0->>+p_6: Generates documentation
    p_6-->>-p_0: ✓ done
    p_0->>+p_7: Formats documentation
    p_7-->>-p_0: ✓ done
    p_16->>+p_3: Returns generated documentation
    p_3-->>-p_16: ✓ done
    end

    rect rgb(236,72,153,0.1)
    Note right of p_0: 🔷 Ideation Engine
    p_3->>+p_16: Requests ideation
    p_16-->>-p_3: ✓ done
    p_16->>+p_8: Initializes IdeationEngine
    p_8-->>-p_16: ✓ done
    p_1->>+p_10: Generates ideas
    p_10-->>-p_1: ✓ done
    p_1->>+p_9: Formats ideas
    p_9-->>-p_1: ✓ done
    p_16->>+p_3: Returns generated ideas
    p_3-->>-p_16: ✓ done
    end

    rect rgb(16,185,129,0.1)
    Note right of p_0: 🔷 Visualizer Engine
    p_3->>+p_16: Requests visualization
    p_16-->>-p_3: ✓ done
    p_16->>+p_14: Initializes VisualizerEngine
    p_14-->>-p_16: ✓ done
    p_4->>+p_15: Generates visualization
    p_15-->>-p_4: ✓ done
    p_4->>+p_14: Formats visualization
    p_14-->>-p_4: ✓ done
    p_16->>+p_3: Returns generated visualization
    p_3-->>-p_16: ✓ done
    end
```

## 📋 Feature Details

### 1. Code Quality Analysis
- **Description:** Analyzes code quality using IBM watsonx.ai and Sentry
- **Entry Point:** `server.py`
- **Flow Steps:** 5

### 2. Documentation Generation
- **Description:** Generates documentation using IBM watsonx.ai
- **Entry Point:** `server.py`
- **Flow Steps:** 5

### 3. Ideation Engine
- **Description:** Generates ideas and implementations using IBM watsonx.ai
- **Entry Point:** `server.py`
- **Flow Steps:** 5

### 4. Visualizer Engine
- **Description:** Visualizes code and documentation using IBM watsonx.ai
- **Entry Point:** `server.py`
- **Flow Steps:** 5

---
*Made with IBM Bob — BobSuite Visualizer Engine*