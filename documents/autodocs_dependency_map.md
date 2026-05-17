# 📦 Dependency Chain — `autodocs`
> Generated: 2026-05-17T11:11:09.350820Z

## 📊 Summary

| Metric | Value |
|--------|-------|
| Total Modules | **4** |
| Internal Dependencies | **9** |
| External Packages | **4** |
| Architecture Layers | **1** |

## 🏗️ Architecture Diagram

```mermaid
%%{init: {'theme': 'default', 'themeVariables': { 'background': '#ffffff'}}}%%
graph TD
    subgraph Root [🔹 ROOT]
    direction TB
        core([🧩 core])
        generators([🧩 generators])
        prompts([🧩 prompts])
        root([🧩 root])
    end
    subgraph External [📦 EXTERNAL PACKAGES]
    direction TB
        ext_lib[/lib\]
        ext_typing[/typing\]
        ext_pathlib[/pathlib\]
        ext_asyncio[/asyncio\]
    end
    core -.->|uses| ext_asyncio
    core -.->|uses| ext_typing
    core -.->|uses| ext_pathlib
    core -.->|uses| ext_lib
    core -->|imports| prompts
    core -->|imports| generators
    generators -.->|uses| ext_typing
    generators -.->|uses| ext_pathlib
    generators -.->|uses| ext_lib
    prompts -.->|uses| ext_typing
    root -->|imports| core
    root -->|imports| generators

    classDef coreNode fill:#3b82f6,stroke:#1d4ed8,stroke-width:2px,color:#fff,rx:12
    classDef libNode fill:#8b5cf6,stroke:#6d28d9,stroke-width:2px,color:#fff,rx:12
    classDef testNode fill:#ec4899,stroke:#be185d,stroke-width:2px,color:#fff,rx:12
    classDef extNode fill:#10b981,stroke:#047857,stroke-width:2px,color:#fff,rx:8
    class core coreNode
    class generators coreNode
    class prompts coreNode
    class root coreNode
    class ext_lib extNode
    class ext_typing extNode
    class ext_pathlib extNode
    class ext_asyncio extNode

    style Root fill:#f8fafc,stroke:#cbd5e1,stroke-width:2px,color:#334155,rx:16
    style External fill:#f0fdfa,stroke:#a7f3d0,stroke-width:2px,color:#065f46,rx:16
```

## 🎨 Legend

| Color | Layer |
|-------|-------|
| 🔵 Blue | Core entry points |
| 🟣 Purple | Library modules |
| 🩷 Pink | Test suites |
| 🟢 Green | External packages |

## 📁 Module Reference

| Module | Source Path |
|--------|------------|
| `core` | `core.py` |
| `generators` | `generators.py` |
| `prompts` | `prompts.py` |
| `root` | `__init__.py` |

---
*Made with IBM Bob — BobSuite Visualizer Engine*