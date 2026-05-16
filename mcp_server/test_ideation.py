"""
Test Suite for Ideation Engine
Comprehensive tests for feature planning and PRD generation
"""

import asyncio
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from watsonx_client import WatsonxClient
from lib.ideation import IdeationEngine


class TestIdeationEngine:
    """Test suite for the Ideation Engine"""
    
    def __init__(self):
        self.watsonx = WatsonxClient()
        self.engine = IdeationEngine(self.watsonx)
        self.test_results = []
    
    def log_test(self, test_name: str, passed: bool, message: str = ""):
        """Log test results"""
        status = "✓ PASS" if passed else "✗ FAIL"
        self.test_results.append({
            "test": test_name,
            "passed": passed,
            "message": message
        })
        print(f"{status}: {test_name}")
        if message:
            print(f"  → {message}")
    
    # ------------------------------------------------------------------ #
    #                       UNIT TESTS                                    #
    # ------------------------------------------------------------------ #
    
    def test_framework_retrieval(self):
        """Test 1: Framework retrieval with and without examples"""
        try:
            # Test with examples
            framework_with_examples = self.engine.get_framework(include_examples=True)
            assert "pillars" in framework_with_examples
            assert len(framework_with_examples["pillars"]) == 7
            assert "examples" in framework_with_examples["pillars"][0]
            
            # Test without examples
            framework_no_examples = self.engine.get_framework(include_examples=False)
            assert "pillars" in framework_no_examples
            assert "examples" not in framework_no_examples["pillars"][0]
            
            self.log_test("Framework Retrieval", True, "7 pillars loaded correctly")
        except Exception as e:
            self.log_test("Framework Retrieval", False, str(e))
    
    def test_framework_structure(self):
        """Test 2: Validate framework structure"""
        try:
            framework = self.engine.get_framework()
            
            # Check all required pillars exist
            required_pillars = ["description", "in_scope", "out_scope", "implementation", 
                              "acceptance", "timeline", "resources"]
            pillar_ids = [p["id"] for p in framework["pillars"]]
            
            for required in required_pillars:
                assert required in pillar_ids, f"Missing pillar: {required}"
            
            # Check each pillar has required fields
            for pillar in framework["pillars"]:
                assert "id" in pillar
                assert "title" in pillar
                assert "prompt" in pillar
                assert "guidance" in pillar
                assert "importance" in pillar
            
            self.log_test("Framework Structure", True, "All pillars have required fields")
        except Exception as e:
            self.log_test("Framework Structure", False, str(e))
    
    def test_input_validation_empty(self):
        """Test 3: Input validation with empty data"""
        try:
            result = self.engine._validate_input({})
            assert not result["valid"]
            assert "error" in result
            
            self.log_test("Input Validation (Empty)", True, "Correctly rejects empty input")
        except Exception as e:
            self.log_test("Input Validation (Empty)", False, str(e))
    
    def test_input_validation_missing_critical(self):
        """Test 4: Input validation with missing critical pillars"""
        try:
            incomplete_data = {
                "conversation_type": "structured",
                "pillars": {
                    "description": {"answer": "A task management app"}
                    # Missing other critical pillars
                }
            }
            
            result = self.engine._validate_input(incomplete_data)
            assert not result["valid"]
            assert "missing critical pillars" in result["error"].lower()
            
            self.log_test("Input Validation (Missing Critical)", True, 
                         "Correctly identifies missing critical pillars")
        except Exception as e:
            self.log_test("Input Validation (Missing Critical)", False, str(e))
    
    def test_input_validation_short_responses(self):
        """Test 5: Input validation with too-short responses"""
        try:
            short_data = {
                "conversation_type": "structured",
                "pillars": {
                    "description": {"answer": "App"},  # Too short
                    "in_scope": {"answer": "Features for managing tasks efficiently"},
                    "acceptance": {"answer": "Users can create tasks quickly"},
                    "timeline": {"answer": "6 weeks total development time"}
                }
            }
            
            result = self.engine._validate_input(short_data)
            assert not result["valid"]
            assert "too short" in result["error"].lower()
            
            self.log_test("Input Validation (Short Responses)", True, 
                         "Correctly rejects too-short responses")
        except Exception as e:
            self.log_test("Input Validation (Short Responses)", False, str(e))
    
    def test_input_validation_valid(self):
        """Test 6: Input validation with valid data"""
        try:
            valid_data = {
                "conversation_type": "structured",
                "pillars": {
                    "description": {
                        "answer": "A comprehensive task management application for remote teams to coordinate work asynchronously"
                    },
                    "in_scope": {
                        "answer": "User authentication, task CRUD operations, project organization, due date tracking, and basic notifications"
                    },
                    "out_scope": {
                        "answer": "Mobile native apps, advanced analytics, third-party integrations"
                    },
                    "implementation": {
                        "answer": "React frontend with TypeScript, Node.js backend, PostgreSQL database, JWT authentication"
                    },
                    "acceptance": {
                        "answer": "Users can create tasks in under 2 seconds, all operations respond in under 200ms"
                    },
                    "timeline": {
                        "answer": "Phase 1 (Weeks 1-2): Infrastructure, Phase 2 (Weeks 3-4): Features, Phase 3 (Weeks 5-6): Testing"
                    },
                    "resources": {
                        "answer": "Team of 2 developers, 1 designer, AWS infrastructure with $500/month budget"
                    }
                }
            }
            
            result = self.engine._validate_input(valid_data)
            assert result["valid"]
            
            self.log_test("Input Validation (Valid)", True, "Accepts valid structured data")
        except Exception as e:
            self.log_test("Input Validation (Valid)", False, str(e))
    
    def test_output_path_determination(self):
        """Test 7: Output path determination logic"""
        try:
            # Test with user-specified path
            custom_path = "/custom/path/my-prd.md"
            result = self.engine._determine_output_path(
                output_path=custom_path,
                project_name="Test Project",
                conversation_data={}
            )
            assert result == custom_path
            
            # Test with project name (auto-generated)
            result = self.engine._determine_output_path(
                output_path=None,
                project_name="My Awesome Project",
                conversation_data={}
            )
            assert "my-awesome-project" in result.lower()
            assert result.endswith(".md")
            
            # Test without project name (default)
            result = self.engine._determine_output_path(
                output_path=None,
                project_name=None,
                conversation_data={}
            )
            assert "project" in result.lower()
            assert result.endswith(".md")
            
            self.log_test("Output Path Determination", True, "Correctly determines output paths")
        except Exception as e:
            self.log_test("Output Path Determination", False, str(e))
    
    def test_framework_display_formatting(self):
        """Test 8: Framework display formatting"""
        try:
            formatted = self.engine.format_framework_for_display()
            
            # Check it's markdown
            assert formatted.startswith("#")
            assert "Pillar 1:" in formatted
            assert "Pillar 7:" in formatted
            assert "timeline" in formatted.lower()
            assert "resources" in formatted.lower()
            
            self.log_test("Framework Display Formatting", True, "Generates proper markdown")
        except Exception as e:
            self.log_test("Framework Display Formatting", False, str(e))
    
    # ------------------------------------------------------------------ #
    #                       INTEGRATION TESTS                             #
    # ------------------------------------------------------------------ #
    
    async def test_prd_synthesis_structured(self):
        """Test 9: PRD synthesis with structured data"""
        try:
            test_data = {
                "conversation_type": "structured",
                "pillars": {
                    "description": {
                        "answer": "A real-time collaborative whiteboard application for distributed design teams to brainstorm and iterate on ideas together."
                    },
                    "in_scope": {
                        "answer": "Real-time drawing tools, shape library, text annotations, user presence indicators, basic export to PNG/SVG, user authentication"
                    },
                    "out_scope": {
                        "answer": "Video chat integration, advanced animation tools, 3D modeling, mobile apps, offline mode"
                    },
                    "implementation": {
                        "answer": "React with Canvas API for drawing, WebSocket for real-time sync, Node.js backend, MongoDB for persistence, Redis for session management"
                    },
                    "acceptance": {
                        "answer": "Multiple users can draw simultaneously with <100ms latency, changes sync across all clients, no data loss on disconnect/reconnect"
                    },
                    "timeline": {
                        "answer": "Week 1-2: Core drawing engine, Week 3-4: Real-time sync, Week 5-6: User management and polish, Week 7-8: Testing and launch"
                    },
                    "resources": {
                        "answer": "3 full-stack developers, 1 UX designer, AWS infrastructure ($300/month), WebSocket service (Pusher or similar, $50/month)"
                    }
                }
            }
            
            result = await self.engine.synthesize_prd(
                conversation_data=test_data,
                project_name="Collaborative Whiteboard",
                output_path=None  # Let AI decide
            )
            
            assert result["success"]
            assert "prd_markdown" in result
            assert len(result["prd_markdown"]) > 500  # Should be substantial
            assert "metadata" in result
            
            # Check PRD content quality
            prd = result["prd_markdown"]
            assert "whiteboard" in prd.lower()
            assert "real-time" in prd.lower()
            
            self.log_test("PRD Synthesis (Structured)", True, 
                         f"Generated {len(prd)} character PRD")
        except Exception as e:
            self.log_test("PRD Synthesis (Structured)", False, str(e))
    
    async def test_prd_synthesis_with_file_save(self):
        """Test 10: PRD synthesis with file saving"""
        try:
            test_data = {
                "conversation_type": "structured",
                "pillars": {
                    "description": {"answer": "A simple note-taking app for quick thoughts and ideas with minimal friction"},
                    "in_scope": {"answer": "Create, edit, delete notes, markdown support, search functionality, cloud sync"},
                    "out_scope": {"answer": "Collaboration features, rich media embeds, mobile apps"},
                    "implementation": {"answer": "Vue.js frontend, Firebase backend for auth and storage, Algolia for search"},
                    "acceptance": {"answer": "Notes save automatically within 1 second, search returns results in <500ms"},
                    "timeline": {"answer": "4 weeks total: Week 1-2 core features, Week 3-4 polish and launch"},
                    "resources": {"answer": "1 full-stack developer, Firebase free tier, Algolia free tier"}
                }
            }
            
            # Use a test output path
            test_output = Path(__file__).parent / "lib" / "ideation" / "test-prd-output.md"
            
            result = await self.engine.synthesize_prd(
                conversation_data=test_data,
                project_name="Quick Notes",
                output_path=str(test_output)
            )
            
            assert result["success"]
            assert result["metadata"]["file_saved"]
            assert test_output.exists()
            
            # Clean up test file
            if test_output.exists():
                test_output.unlink()
            
            self.log_test("PRD Synthesis (File Save)", True, "PRD saved to file successfully")
        except Exception as e:
            self.log_test("PRD Synthesis (File Save)", False, str(e))
    
    # ------------------------------------------------------------------ #
    #                       TEST RUNNER                                   #
    # ------------------------------------------------------------------ #
    
    async def run_all_tests(self):
        """Run all tests and generate report"""
        print("\n" + "="*70)
        print("🧪 IDEATION ENGINE TEST SUITE")
        print("="*70 + "\n")
        
        # Unit tests (synchronous)
        print("📋 UNIT TESTS\n")
        self.test_framework_retrieval()
        self.test_framework_structure()
        self.test_input_validation_empty()
        self.test_input_validation_missing_critical()
        self.test_input_validation_short_responses()
        self.test_input_validation_valid()
        self.test_output_path_determination()
        self.test_framework_display_formatting()
        
        # Integration tests (asynchronous)
        print("\n🔗 INTEGRATION TESTS\n")
        await self.test_prd_synthesis_structured()
        await self.test_prd_synthesis_with_file_save()
        
        # Generate summary
        print("\n" + "="*70)
        print("📊 TEST SUMMARY")
        print("="*70 + "\n")
        
        passed = sum(1 for r in self.test_results if r["passed"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n✨ All tests passed! Ideation Engine is ready to use.")
        else:
            print("\n⚠️  Some tests failed. Review the output above.")
            print("\nFailed tests:")
            for result in self.test_results:
                if not result["passed"]:
                    print(f"  - {result['test']}: {result['message']}")
        
        print("\n" + "="*70 + "\n")
        
        return passed == total


async def main():
    """Main test runner"""
    tester = TestIdeationEngine()
    success = await tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())


# Made with Bob