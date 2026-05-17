"""
Test script for QA Sentry's new features:
1. Network Performance Testing
2. Unit Test Generation

This script tests both features with sample code files.
"""

import asyncio
import sys
from pathlib import Path

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from watsonx_client import WatsonxClient
from lib.qa_sentry import QASentry


# Sample API code for network performance testing
SAMPLE_API_CODE = '''
import express from 'express';
import axios from 'axios';

const app = express();
app.use(express.json());

// User API endpoint
app.get('/api/users/:id', async (req, res) => {
    try {
        const userId = req.params.id;
        const response = await axios.get(`https://jsonplaceholder.typicode.com/users/${userId}`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch user' });
    }
});

// Create user endpoint
app.post('/api/users', async (req, res) => {
    try {
        const userData = req.body;
        const response = await axios.post('https://jsonplaceholder.typicode.com/users', userData);
        res.status(201).json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Failed to create user' });
    }
});

// Rate-limited endpoint
let requestCount = 0;
const RATE_LIMIT = 100;
const TIME_WINDOW = 60000; // 1 minute

app.get('/api/limited', (req, res) => {
    requestCount++;
    if (requestCount > RATE_LIMIT) {
        return res.status(429).json({ error: 'Rate limit exceeded' });
    }
    res.json({ message: 'Success', requestCount });
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
'''

# Sample business logic code for unit testing
SAMPLE_BUSINESS_LOGIC = '''
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.discount_rate = 0
    
    def add_item(self, item, quantity=1):
        """Add an item to the cart"""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        self.items.append({
            'name': item['name'],
            'price': item['price'],
            'quantity': quantity
        })
    
    def remove_item(self, item_name):
        """Remove an item from the cart"""
        self.items = [item for item in self.items if item['name'] != item_name]
    
    def apply_discount(self, discount_rate):
        """Apply a discount to the cart"""
        if discount_rate < 0 or discount_rate > 1:
            raise ValueError("Discount rate must be between 0 and 1")
        self.discount_rate = discount_rate
    
    def calculate_total(self):
        """Calculate the total price with discount"""
        subtotal = sum(item['price'] * item['quantity'] for item in self.items)
        discount_amount = subtotal * self.discount_rate
        return subtotal - discount_amount
    
    def get_item_count(self):
        """Get total number of items in cart"""
        return sum(item['quantity'] for item in self.items)
    
    def clear_cart(self):
        """Clear all items from cart"""
        self.items = []
        self.discount_rate = 0
'''


async def test_network_performance_tests():
    """Test the network performance test generation feature"""
    print("\n" + "="*80)
    print("TEST 1: Network Performance Test Generation")
    print("="*80)
    
    # Create temporary test file
    test_file = Path("mcp_server/test_output/sample_api.js")
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text(SAMPLE_API_CODE)
    
    try:
        # Initialize QA Sentry
        watsonx = WatsonxClient()
        qa_sentry = QASentry(watsonx)
        
        print("\n📝 Testing with autonomous library selection...")
        result1 = await qa_sentry.generate_network_performance_tests(
            file_path=str(test_file)
        )
        
        print(f"\n✅ Success: {result1.get('success')}")
        print(f"📦 Framework Selected: {result1.get('test_framework')}")
        print(f"📋 Test Files Generated: {len(result1.get('test_files', []))}")
        print(f"⚙️  Configuration Files: {len(result1.get('configuration_files', []))}")
        
        # Save detailed output
        output_file = Path("mcp_server/test_output/network_performance_tests.md")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Network Performance Tests - Autonomous Selection\n\n")
            f.write(f"**File Analyzed:** `{result1.get('file_path')}`\n")
            f.write(f"**Language:** {result1.get('language')}\n")
            f.write(f"**Test Framework:** {result1.get('test_framework')}\n")
            f.write(f"**Timestamp:** {result1.get('timestamp')}\n\n")
            
            f.write("## Framework Justification\n\n")
            f.write(f"{result1.get('framework_justification')}\n\n")
            
            f.write("## Dependencies\n\n```bash\n")
            for dep in result1.get('dependencies', []):
                f.write(f"{dep}\n")
            f.write("```\n\n")
            
            if result1.get('setup_commands'):
                f.write("## Setup Commands\n\n```bash\n")
                for cmd in result1.get('setup_commands', []):
                    f.write(f"{cmd}\n")
                f.write("```\n\n")
            
            f.write("## Test Files\n\n")
            for test_file_data in result1.get('test_files', []):
                f.write(f"### {test_file_data['filename']}\n\n")
                f.write(f"{test_file_data['description']}\n\n")
                f.write(f"```javascript\n{test_file_data['content']}\n```\n\n")
            
            if result1.get('configuration_files'):
                f.write("## Configuration Files\n\n")
                for config in result1.get('configuration_files', []):
                    f.write(f"### {config['filename']}\n\n")
                    f.write(f"{config['description']}\n\n")
                    f.write(f"```javascript\n{config['content']}\n```\n\n")
            
            f.write("## Execution Command\n\n")
            f.write(f"```bash\n{result1.get('execution_command')}\n```\n\n")
            
            if result1.get('performance_thresholds'):
                f.write("## Performance Thresholds\n\n")
                thresholds = result1['performance_thresholds']
                f.write(f"- **Response Time:** {thresholds.get('response_time_ms', 'N/A')} ms\n")
                f.write(f"- **Throughput:** {thresholds.get('throughput_rps', 'N/A')} requests/sec\n")
                f.write(f"- **Error Rate:** {thresholds.get('error_rate_percent', 'N/A')}%\n\n")
            
            if result1.get('test_scenarios'):
                f.write("## Test Scenarios\n\n")
                for scenario in result1['test_scenarios']:
                    f.write(f"- {scenario}\n")
                f.write("\n")
            
            if result1.get('notes'):
                f.write(f"## Notes\n\n{result1['notes']}\n")
        
        print(f"\n💾 Detailed output saved to: {output_file}")
        
        # Test with specific library
        print("\n📝 Testing with specific library (Jest)...")
        result2 = await qa_sentry.generate_network_performance_tests(
            file_path=str(test_file),
            testing_library="jest",
            test_requirements="Focus on timeout handling and concurrent requests"
        )
        
        print(f"\n✅ Success: {result2.get('success')}")
        print(f"📦 Framework Used: {result2.get('test_framework')}")
        
        return result1.get('success') and result2.get('success')
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_unit_test_generation():
    """Test the unit test generation feature"""
    print("\n" + "="*80)
    print("TEST 2: Unit Test Generation (Steve Sanderson Principles)")
    print("="*80)
    
    # Create temporary test file
    test_file = Path("mcp_server/test_output/sample_cart.py")
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text(SAMPLE_BUSINESS_LOGIC)
    
    try:
        # Initialize QA Sentry
        watsonx = WatsonxClient()
        qa_sentry = QASentry(watsonx)
        
        print("\n📝 Testing with autonomous library selection...")
        result1 = await qa_sentry.generate_unit_tests(
            file_path=str(test_file)
        )
        
        print(f"\n✅ Success: {result1.get('success')}")
        print(f"📦 Framework Selected: {result1.get('test_framework')}")
        print(f"📋 Test Files Generated: {len(result1.get('test_files', []))}")
        print(f"🎯 Test Count: {result1.get('test_coverage', {}).get('test_count', 'N/A')}")
        print(f"🔧 Mocking Library: {result1.get('mock_strategy', {}).get('mocking_library', 'N/A')}")
        
        # Save detailed output
        output_file = Path("mcp_server/test_output/unit_tests_generated.md")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Unit Tests Generated - Steve Sanderson Principles\n\n")
            f.write(f"**File Analyzed:** `{result1.get('file_path')}`\n")
            f.write(f"**Language:** {result1.get('language')}\n")
            f.write(f"**Test Framework:** {result1.get('test_framework')}\n")
            f.write(f"**Timestamp:** {result1.get('timestamp')}\n\n")
            
            f.write("## Framework Justification\n\n")
            f.write(f"{result1.get('framework_justification')}\n\n")
            
            f.write("## Dependencies\n\n```bash\n")
            for dep in result1.get('dependencies', []):
                f.write(f"{dep}\n")
            f.write("```\n\n")
            
            if result1.get('setup_commands'):
                f.write("## Setup Commands\n\n```bash\n")
                for cmd in result1.get('setup_commands', []):
                    f.write(f"{cmd}\n")
                f.write("```\n\n")
            
            f.write("## Test Files\n\n")
            for test_file_data in result1.get('test_files', []):
                f.write(f"### {test_file_data['filename']}\n\n")
                f.write(f"{test_file_data['description']}\n\n")
                f.write(f"```python\n{test_file_data['content']}\n```\n\n")
            
            if result1.get('configuration_files'):
                f.write("## Configuration Files\n\n")
                for config in result1.get('configuration_files', []):
                    f.write(f"### {config['filename']}\n\n")
                    f.write(f"{config['description']}\n\n")
                    f.write(f"```python\n{config['content']}\n```\n\n")
            
            f.write("## Execution Command\n\n")
            f.write(f"```bash\n{result1.get('execution_command')}\n```\n\n")
            
            if result1.get('mock_strategy'):
                f.write("## Mock Strategy\n\n")
                mock_strat = result1['mock_strategy']
                f.write(f"**Mocking Library:** {mock_strat.get('mocking_library', 'N/A')}\n\n")
                if mock_strat.get('external_dependencies'):
                    f.write("**External Dependencies Mocked:**\n\n")
                    for dep in mock_strat['external_dependencies']:
                        f.write(f"- {dep}\n")
                    f.write("\n")
                if mock_strat.get('mock_examples'):
                    f.write("**Mock Patterns:**\n\n")
                    for example in mock_strat['mock_examples']:
                        f.write(f"- {example}\n")
                    f.write("\n")
            
            if result1.get('test_coverage'):
                f.write("## Test Coverage\n\n")
                coverage = result1['test_coverage']
                f.write(f"**Total Tests:** {coverage.get('test_count', 'N/A')}\n\n")
                if coverage.get('units_tested'):
                    f.write("**Units Tested:**\n\n")
                    for unit in coverage['units_tested']:
                        f.write(f"- {unit}\n")
                    f.write("\n")
                if coverage.get('coverage_notes'):
                    f.write(f"{coverage['coverage_notes']}\n\n")
            
            if result1.get('design_principles_applied'):
                f.write("## Design Principles Applied\n\n")
                for principle in result1['design_principles_applied']:
                    f.write(f"- {principle}\n")
                f.write("\n")
            
            if result1.get('notes'):
                f.write(f"## Notes\n\n{result1['notes']}\n")
        
        print(f"\n💾 Detailed output saved to: {output_file}")
        
        # Test with specific library
        print("\n📝 Testing with specific library (pytest)...")
        result2 = await qa_sentry.generate_unit_tests(
            file_path=str(test_file),
            testing_library="pytest",
            test_requirements="Focus on edge cases and error handling"
        )
        
        print(f"\n✅ Success: {result2.get('success')}")
        print(f"📦 Framework Used: {result2.get('test_framework')}")
        
        return result1.get('success') and result2.get('success')
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("QA SENTRY NEW FEATURES TEST SUITE")
    print("="*80)
    
    results = []
    
    # Test 1: Network Performance Tests
    result1 = await test_network_performance_tests()
    results.append(("Network Performance Tests", result1))
    
    # Test 2: Unit Test Generation
    result2 = await test_unit_test_generation()
    results.append(("Unit Test Generation", result2))
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    print("\n📁 Test outputs saved to: mcp_server/test_output/")
    print("="*80 + "\n")
    
    return all_passed


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

# Made with Bob
