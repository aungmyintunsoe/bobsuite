import asyncio
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from watsonx_client import WatsonxClient
from lib.qa_sentry import QASentry
from lib.autodocs import AutoDocs
from lib.visualizer import VisualizerEngine
from lib.ideation import IdeationEngine

async def run_features():
    print("Initializing components...")
    watsonx = WatsonxClient()
    qa_sentry = QASentry(watsonx)
    autodocs = AutoDocs(watsonx)
    visualizer = VisualizerEngine(watsonx)
    ideation = IdeationEngine(watsonx)
    
    # Paths
    dataset_path = Path(__file__).parent / "dataset_balancia"
    output_dir = Path(__file__).parent / "test_output"
    output_dir.mkdir(exist_ok=True)
    
    # Find a sample file for code analysis/docs
    sample_file = list(dataset_path.rglob("*.ts"))[0]
    
    print(f"\n1. Running QA Sentry on {sample_file.name}...")
    qa_result = await qa_sentry.scan_code(str(sample_file), auto_fix=False)
    if qa_result.get("success"):
        report = qa_sentry.generate_report([qa_result])
        (output_dir / "qa_sentry_report.md").write_text(report, encoding="utf-8")
        print(" -> QA Sentry report saved.")
    
    print("\n2. Running AutoDocs (Full) on {sample_file.name}...")
    docs_result = await autodocs.generate_docs(str(sample_file), doc_type="full")
    (output_dir / "autodocs_full.md").write_text(docs_result, encoding="utf-8")
    print(" -> AutoDocs report saved.")
    
    print("\n3. Running Visualizer (Dependency Chain)...")
    viz_dep = await visualizer.generate_dependency_chain(str(dataset_path), max_depth=2)
    if viz_dep.get("success"):
        (output_dir / "visualizer_dependency.md").write_text(viz_dep.get("markdown", ""), encoding="utf-8")
        print(" -> Dependency chain saved.")
        
    print("\n4. Running Visualizer (Project Concept)...")
    viz_concept = await visualizer.generate_project_concept(str(dataset_path))
    if viz_concept.get("success"):
        (output_dir / "visualizer_concept.md").write_text(viz_concept.get("markdown", ""), encoding="utf-8")
        print(" -> Project concept saved.")
        
    print("\n5. Running Ideation (Framework retrieval)...")
    framework = ideation.get_framework()
    (output_dir / "ideation_framework.json").write_text(json.dumps(framework, indent=2), encoding="utf-8")
    print(" -> Ideation framework saved.")
    
    print("\nDone! Check the test_output folder.")

if __name__ == "__main__":
    asyncio.run(run_features())
