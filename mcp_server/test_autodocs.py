"""
Doc Engine Verification Test Harness
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from watsonx_client import WatsonxClient
from lib.doc_engine import DocEngine

async def run_chronicler_test():
    print("=" * 60)
    print("RUNNING CHRONICLER AUTO-DOC VERIFICATION")
    print("=" * 60)
    
    # Initialize components using the provided framework instances
    client = WatsonxClient()
    engine = DocEngine(client)
    
    # Locate target verification files in the workspace
    dataset_root = Path(__file__).parent / "dataset_balancia"
    target_file = dataset_root / "src" / "app" / "actions.ts"
    
    # Dynamic fallback check if actions.ts is omitted
    if not target_file.exists():
        ts_files = list(dataset_root.rglob("*.ts"))
        if ts_files:
            target_file = ts_files[0]
        else:
            print("[SKIP] No code files found to build docs.")
            return

    print(f"Target selected: {target_file.relative_to(Path(__file__).parent)}")
    print("Generating comprehensive README and LOGIC FLOW mapping...")
    
    docs = await engine.generate_docs(str(target_file), doc_type="full")
    
    print("\n--- GENERATED DOCUMENTATION OUTPUT PREVIEW ---")
    print("\n".join(docs.splitlines()[:25]))
    print("\n... documentation complete ...")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_chronicler_test())