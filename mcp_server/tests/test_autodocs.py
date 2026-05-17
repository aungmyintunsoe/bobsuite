"""
AutoDocs Verification Test Harness
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from watsonx_client import WatsonxClient
from lib.autodocs import AutoDocs

async def run_chronicler_test():
    print("=" * 60)
    print("RUNNING AUTODOCS VERIFICATION")
    print("=" * 60)
    
    # Initialize components
    client = WatsonxClient()
    engine = AutoDocs(client)
    
    # Locate target verification files
    dataset_root = Path(__file__).parent.parent.parent / "dataset_balancia"
    target_file = dataset_root / "src" / "app" / "actions.ts"
    
    # Dynamic fallback
    if not target_file.exists():
        ts_files = list(dataset_root.rglob("*.ts"))
        if ts_files:
            target_file = ts_files[0]
        else:
            print("[SKIP] No code files found to build docs.")
            return

    print(f"Target selected: {target_file.name}")
    print("Generating comprehensive documentation...")
    
    docs = await engine.generate_docs(str(target_file), doc_type="api")
    
    print("\n--- GENERATED DOCUMENTATION OUTPUT PREVIEW ---")
    print("\n".join(docs.splitlines()[:25]))
    print("\n... documentation complete ...")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_chronicler_test())