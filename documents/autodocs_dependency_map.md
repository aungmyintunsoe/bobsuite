# 📦 Dependency Chain Map
**Root Directory:** `autodocs`
**Analysis Time:** 2026-05-17T10:34:51.313541Z

## System Architecture
```mermaid
graph TD
    subgraph Root [ROOT Layer]
        core[core]
        generators[generators]
        prompts[prompts]
        root[root]
    end
    subgraph External [External Packages]
        ext_pathlib[(pathlib)]
        ext_typing[(typing)]
        ext_lib[(lib)]
        ext_asyncio[(asyncio)]
    end
    core -.->|depends on| ext_asyncio
    core -.->|depends on| ext_typing
    core -.->|depends on| ext_pathlib
    core -.->|depends on| ext_lib
    core --> prompts
    core --> generators
    generators -.->|depends on| ext_typing
    generators -.->|depends on| ext_pathlib
    generators -.->|depends on| ext_lib
    prompts -.->|depends on| ext_typing
    root --> core
    root --> generators
```

## Module Explanations
- **core** maps out to source path location: `core.py`
- **generators** maps out to source path location: `generators.py`
- **prompts** maps out to source path location: `prompts.py`
- **root** maps out to source path location: `__init__.py`