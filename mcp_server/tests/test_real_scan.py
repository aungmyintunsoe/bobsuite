"""
Real-world scan test for QA Sentry
Scans multiple files from the Balancia dataset and prints the final report
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from watsonx_client import WatsonxClient
from lib.qa_sentry import QASentry

async def main():
    print("🚀 Starting Production Scan on Balancia Dataset...")
    
    client = WatsonxClient()
    sentry = QASentry(client)
    
    # Files to scan
    files = [
        "d:/ibmbobhack/dataset_balancia/src/app/actions.ts",
        "d:/ibmbobhack/dataset_balancia/src/lib/ilmu.ts"
    ]
    
    # Run batch scan
    results = await sentry.batch_scan(files)
    
    # Generate the rich report
    report = sentry.generate_report(results)
    
    print("\n" + "="*80)
    print("FINAL QA SENTRY PRIME REPORT")
    print("="*80)
    print(report)
    print("="*80)

if __name__ == "__main__":
    asyncio.run(main())
