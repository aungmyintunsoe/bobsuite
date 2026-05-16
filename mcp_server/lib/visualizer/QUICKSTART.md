# Visualizer Engine - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Test the Installation

```bash
cd mcp_server
python test_visualizer.py
```

This verifies everything works and generates sample visualizations in `test_outputs/`.

### Step 2: Use in IBM Bob

Open IBM Bob and try these commands:

**Generate Dependency Chain:**
```
Bob, generate a dependency chain for the mcp_server directory
```

**Generate Feature Flow:**
```
Bob, create a feature flow visualization for the dataset_balancia project
```

**Generate Project Concept:**
```
Bob, generate a project concept map for the entire bobsuite project
```

### Step 3: Save Your Visualizations

Add output paths to save diagrams:

```
Bob, generate a dependency chain for mcp_server and save it to docs/visualizations/
```

---

## 📊 What You Get

### Dependency Chain
- Shows which modules import which
- Identifies external dependencies
- Perfect for understanding code structure

### Feature Flow Maps
- Illustrates how features work end-to-end
- Shows user journeys through the system
- Great for onboarding and documentation

### Project Concept Maps
- High-level architecture overview
- Shows main components and connections
- Ideal for README and presentations

---

## 💡 Pro Tips

1. **Create a visualizations directory:**
   ```bash
   mkdir -p docs/visualizations
   ```

2. **Update regularly:**
   - After adding new features
   - After refactoring
   - Before major releases

3. **Include in README:**
   ```markdown
   ## Architecture
   See our [visualizations](docs/visualizations/) for project overview.
   ```

4. **View diagrams:**
   - GitHub: Renders automatically
   - VS Code: Install "Markdown Preview Mermaid Support"
   - Online: Use [mermaid.live](https://mermaid.live)

---

## 🔗 Next Steps

- Read the [full usage guide](USAGE_GUIDE.md) for detailed examples
- Check [ARCHITECTURE.md](../../ARCHITECTURE.md) for technical details
- Run `python test_visualizer.py` to see all features

---

**Happy Visualizing! 🎨**