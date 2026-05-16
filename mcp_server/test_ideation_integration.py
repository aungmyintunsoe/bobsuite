"""
Comprehensive Integration Test for Ideation Engine
Tests the complete flow with real watsonx.ai integration
"""

import asyncio
import json
from pathlib import Path
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from watsonx_client import WatsonxClient
from lib.ideation import IdeationEngine
from lib.ideation.framework import get_framework_definition, get_critical_pillars
from lib.ideation.validators import validate_conversation_data, sanitize_project_name
from lib.ideation.formatters import determine_output_path


class IdeationIntegrationTest:
    """Comprehensive integration test suite"""
    
    def __init__(self):
        self.watsonx = None
        self.engine = None
        self.test_results = []
        self.start_time = None
    
    def log(self, message: str, level: str = "INFO"):
        """Log test messages with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    def log_test(self, test_name: str, passed: bool, message: str = "", details: str = ""):
        """Log test results"""
        status = "✓ PASS" if passed else "✗ FAIL"
        self.test_results.append({
            "test": test_name,
            "passed": passed,
            "message": message,
            "details": details
        })
        self.log(f"{status}: {test_name}", "PASS" if passed else "FAIL")
        if message:
            self.log(f"  → {message}", "INFO")
        if details and not passed:
            self.log(f"  Details: {details}", "ERROR")
    
    async def setup(self):
        """Initialize test environment"""
        self.log("="*70)
        self.log("🧪 IDEATION ENGINE - COMPREHENSIVE INTEGRATION TEST")
        self.log("="*70)
        self.log("")
        
        try:
            self.log("Initializing watsonx.ai client...")
            self.watsonx = WatsonxClient()
            self.engine = IdeationEngine(self.watsonx)
            self.log("✓ Initialization successful")
            return True
        except Exception as e:
            self.log(f"✗ Initialization failed: {str(e)}", "ERROR")
            return False
    
    # ------------------------------------------------------------------ #
    #                       MODULE TESTS                                  #
    # ------------------------------------------------------------------ #
    
    def test_framework_module(self):
        """Test framework.py module"""
        self.log("\n📋 Testing Framework Module...")
        
        try:
            # Test framework retrieval
            framework = get_framework_definition()
            assert framework is not None
            assert "pillars" in framework
            assert len(framework["pillars"]) == 7
            
            # Test critical pillars
            critical = get_critical_pillars()
            assert len(critical) == 4  # description, in_scope, acceptance, timeline
            assert "description" in critical
            assert "timeline" in critical
            
            self.log_test(
                "Framework Module",
                True,
                f"7 pillars loaded, {len(critical)} critical pillars identified"
            )
        except Exception as e:
            self.log_test("Framework Module", False, str(e))
    
    def test_validators_module(self):
        """Test validators.py module"""
        self.log("\n🔍 Testing Validators Module...")
        
        try:
            # Test empty data validation
            result = validate_conversation_data({})
            assert not result["valid"]
            assert "error" in result
            
            # Test project name sanitization
            sanitized = sanitize_project_name("My Awesome Project!")
            assert sanitized == "my-awesome-project"
            
            # Test valid structured data
            valid_data = {
                "conversation_type": "structured",
                "pillars": {
                    "description": {"answer": "A" * 60},
                    "in_scope": {"answer": "B" * 110},
                    "acceptance": {"answer": "C" * 90},
                    "timeline": {"answer": "D" * 70}
                }
            }
            result = validate_conversation_data(valid_data)
            assert result["valid"]
            
            self.log_test(
                "Validators Module",
                True,
                "Empty data rejected, valid data accepted, name sanitization works"
            )
        except Exception as e:
            self.log_test("Validators Module", False, str(e))
    
    def test_formatters_module(self):
        """Test formatters.py module"""
        self.log("\n🎨 Testing Formatters Module...")
        
        try:
            # Test output path determination
            path1 = determine_output_path(project_name="Test Project")
            assert "test-project" in path1.lower()
            assert path1.endswith(".md")
            
            # Test custom path
            custom_path = "/custom/path/prd.md"
            path2 = determine_output_path(output_path=custom_path)
            assert path2 == custom_path
            
            self.log_test(
                "Formatters Module",
                True,
                "Path determination and formatting work correctly"
            )
        except Exception as e:
            self.log_test("Formatters Module", False, str(e))
    
    # ------------------------------------------------------------------ #
    #                       INTEGRATION TESTS                             #
    # ------------------------------------------------------------------ #
    
    async def test_framework_retrieval(self):
        """Test framework retrieval through engine"""
        self.log("\n📖 Testing Framework Retrieval...")
        
        try:
            # Test with examples
            framework = self.engine.get_framework(include_examples=True)
            assert "pillars" in framework
            assert "examples" in framework["pillars"][0]
            
            # Test without examples
            framework_no_ex = self.engine.get_framework(include_examples=False)
            assert "examples" not in framework_no_ex["pillars"][0]
            
            # Test display formatting
            display = self.engine.format_framework_for_display()
            assert "Pillar 1:" in display
            assert "Pillar 7:" in display
            assert len(display) > 1000
            
            self.log_test(
                "Framework Retrieval",
                True,
                f"Framework retrieved, display formatted ({len(display)} chars)"
            )
        except Exception as e:
            self.log_test("Framework Retrieval", False, str(e))
    
    async def test_prd_synthesis_minimal(self):
        """Test PRD synthesis with minimal valid data"""
        self.log("\n🤖 Testing PRD Synthesis (Minimal Data)...")
        
        try:
            test_data = {
                "conversation_type": "structured",
                "pillars": {
                    "description": {
                        "answer": "A simple note-taking Chrome extension for quick thoughts and ideas with minimal friction and distraction-free writing experience."
                    },
                    "in_scope": {
                        "answer": "Create, edit, delete notes with markdown support, local storage sync, search functionality, keyboard shortcuts for quick access, dark mode support."
                    },
                    "out_scope": {
                        "answer": "Collaboration features, rich media embeds, mobile apps, cloud sync across devices, advanced formatting tools."
                    },
                    "implementation": {
                        "answer": "Chrome Extension Manifest V3, vanilla JavaScript for popup UI, Chrome Storage API for persistence, markdown parser library."
                    },
                    "acceptance": {
                        "answer": "Notes save automatically within 1 second, search returns results in under 500ms, extension loads without impacting page performance, zero data loss on browser restart."
                    },
                    "timeline": {
                        "answer": "Week 1: Extension scaffold and storage, Week 2: UI and markdown, Week 3: Search and polish, Week 4: Testing and Chrome Web Store submission. Total: 4 weeks."
                    },
                    "resources": {
                        "answer": "1 full-stack developer, Chrome Web Store developer account ($5 one-time), no ongoing costs for MVP."
                    }
                }
            }
            
            self.log("  Calling watsonx.ai for PRD generation...")
            result = await self.engine.synthesize_prd(
                conversation_data=test_data,
                project_name="Quick Notes Extension"
            )
            
            if result["success"]:
                prd = result["prd_markdown"]
                metadata = result["metadata"]
                
                # Validate PRD content
                assert len(prd) > 500, "PRD too short"
                assert "note" in prd.lower() or "extension" in prd.lower(), "PRD missing key terms"
                assert metadata["pillar_count"] == 7
                
                # Check if file was saved
                if result.get("file_path"):
                    file_path = Path(result["file_path"])
                    assert file_path.exists(), "PRD file not found"
                    self.log(f"  ✓ PRD saved to: {file_path}")
                
                self.log_test(
                    "PRD Synthesis (Minimal)",
                    True,
                    f"Generated {len(prd)} character PRD, file saved: {metadata['file_saved']}"
                )
            else:
                self.log_test(
                    "PRD Synthesis (Minimal)",
                    False,
                    result.get("error", "Unknown error"),
                    json.dumps(result, indent=2)
                )
        except Exception as e:
            self.log_test("PRD Synthesis (Minimal)", False, str(e), str(type(e)))
    
    async def test_prd_synthesis_comprehensive(self):
        """Test PRD synthesis with comprehensive data including follow-ups"""
        self.log("\n🚀 Testing PRD Synthesis (Comprehensive Data)...")
        
        try:
            test_data = {
                "conversation_type": "structured",
                "pillars": {
                    "description": {
                        "answer": "A real-time collaborative whiteboard application for distributed design teams to brainstorm and iterate on ideas together. Target users are remote design teams (5-20 people) who need to visualize concepts synchronously during meetings.",
                        "follow_ups": [
                            {
                                "q": "What makes this different from existing tools like Miro or FigJam?",
                                "a": "Focus on simplicity and speed - no learning curve, instant collaboration, optimized for quick brainstorming sessions rather than long-term project management."
                            }
                        ]
                    },
                    "in_scope": {
                        "answer": "Real-time drawing tools (pen, shapes, text), shape library with common UI elements, user presence indicators showing who's active, basic export to PNG/SVG, user authentication and workspace management, undo/redo functionality, zoom and pan controls."
                    },
                    "out_scope": {
                        "answer": "Video chat integration, advanced animation tools, 3D modeling capabilities, mobile native apps (web-only for MVP), offline mode, version history beyond basic undo/redo, advanced permissions and roles."
                    },
                    "implementation": {
                        "answer": "Frontend: React with HTML5 Canvas API for drawing, WebSocket for real-time sync using Socket.io. Backend: Node.js with Express, MongoDB for persistence, Redis for session management and real-time state. Authentication: JWT tokens with refresh mechanism. Deployment: Docker containers on AWS ECS with CloudFront CDN."
                    },
                    "acceptance": {
                        "answer": "Multiple users can draw simultaneously with less than 100ms latency, changes sync across all connected clients in real-time, no data loss on disconnect/reconnect, canvas supports minimum 1000 objects without performance degradation, export generates valid PNG/SVG files, 95% of users complete onboarding without help documentation."
                    },
                    "timeline": {
                        "answer": "Phase 1 (Weeks 1-2): Core drawing engine and canvas implementation. Phase 2 (Weeks 3-4): Real-time sync with WebSocket integration and conflict resolution. Phase 3 (Weeks 5-6): User management, authentication, and workspace features. Phase 4 (Weeks 7-8): Polish, performance optimization, testing, and deployment. Target MVP: 8 weeks from kickoff. Beta launch: Week 9 with 10 test teams. Full launch: Week 10."
                    },
                    "resources": {
                        "answer": "Team: 3 full-stack developers (React + Node.js experience), 1 UX designer (canvas/drawing UI expertise), 1 QA engineer. Infrastructure: AWS account with estimated $300/month for hosting (EC2, RDS, CloudFront). Tools: GitHub for version control, Figma for design, Linear for project management. Third-party services: Socket.io for WebSocket ($0 for MVP), SendGrid for transactional emails ($20/month). Time commitment: 40 hours/week per team member."
                    }
                }
            }
            
            self.log("  Calling watsonx.ai for comprehensive PRD generation...")
            result = await self.engine.synthesize_prd(
                conversation_data=test_data,
                project_name="Collaborative Whiteboard"
            )
            
            if result["success"]:
                prd = result["prd_markdown"]
                metadata = result["metadata"]
                
                # Validate PRD quality
                assert len(prd) > 1000, "Comprehensive PRD should be substantial"
                assert "whiteboard" in prd.lower(), "PRD missing project context"
                assert "real-time" in prd.lower(), "PRD missing key feature"
                
                # Check structure
                assert "##" in prd, "PRD should have sections"
                
                self.log_test(
                    "PRD Synthesis (Comprehensive)",
                    True,
                    f"Generated {len(prd)} character PRD with rich context"
                )
                
                # Save a copy for manual review
                review_path = Path(__file__).parent / "lib" / "ideation" / "test-output-comprehensive.md"
                with open(review_path, 'w') as f:
                    f.write(prd)
                self.log(f"  ✓ Saved for review: {review_path}")
                
            else:
                self.log_test(
                    "PRD Synthesis (Comprehensive)",
                    False,
                    result.get("error", "Unknown error"),
                    json.dumps(result, indent=2)
                )
        except Exception as e:
            self.log_test("PRD Synthesis (Comprehensive)", False, str(e), str(type(e)))
    
    async def test_error_handling(self):
        """Test error handling with invalid inputs"""
        self.log("\n⚠️  Testing Error Handling...")
        
        try:
            # Test empty data
            result1 = await self.engine.synthesize_prd(conversation_data={})
            assert not result1["success"]
            assert "error" in result1
            
            # Test missing critical pillars
            incomplete_data = {
                "conversation_type": "structured",
                "pillars": {
                    "description": {"answer": "A simple app"}
                }
            }
            result2 = await self.engine.synthesize_prd(conversation_data=incomplete_data)
            assert not result2["success"]
            assert "missing" in result2["error"].lower()
            
            # Test invalid project name
            result3 = await self.engine.synthesize_prd(
                conversation_data={"pillars": {}},
                project_name="Invalid/Name:With*Chars"
            )
            assert not result3["success"]
            
            self.log_test(
                "Error Handling",
                True,
                "All error cases handled gracefully with helpful messages"
            )
        except Exception as e:
            self.log_test("Error Handling", False, str(e))
    
    # ------------------------------------------------------------------ #
    #                       TEST RUNNER                                   #
    # ------------------------------------------------------------------ #
    
    async def run_all_tests(self):
        """Run all integration tests"""
        self.start_time = datetime.now()
        
        # Setup
        if not await self.setup():
            self.log("Setup failed. Aborting tests.", "ERROR")
            return False
        
        # Module tests (synchronous)
        self.log("\n" + "="*70)
        self.log("PHASE 1: MODULE TESTS")
        self.log("="*70)
        self.test_framework_module()
        self.test_validators_module()
        self.test_formatters_module()
        
        # Integration tests (asynchronous)
        self.log("\n" + "="*70)
        self.log("PHASE 2: INTEGRATION TESTS")
        self.log("="*70)
        await self.test_framework_retrieval()
        await self.test_prd_synthesis_minimal()
        await self.test_prd_synthesis_comprehensive()
        await self.test_error_handling()
        
        # Generate report
        self.generate_report()
        
        # Return success status
        passed = sum(1 for r in self.test_results if r["passed"])
        return passed == len(self.test_results)
    
    def generate_report(self):
        """Generate comprehensive test report"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        self.log("\n" + "="*70)
        self.log("📊 TEST REPORT")
        self.log("="*70)
        
        passed = sum(1 for r in self.test_results if r["passed"])
        failed = len(self.test_results) - passed
        
        self.log(f"\nTotal Tests: {len(self.test_results)}")
        self.log(f"Passed: {passed} ✓")
        self.log(f"Failed: {failed} ✗")
        self.log(f"Success Rate: {(passed/len(self.test_results)*100):.1f}%")
        self.log(f"Duration: {duration:.2f} seconds")
        
        if failed > 0:
            self.log("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["passed"]:
                    self.log(f"  - {result['test']}")
                    self.log(f"    Error: {result['message']}")
                    if result.get("details"):
                        self.log(f"    Details: {result['details'][:200]}...")
        
        if passed == len(self.test_results):
            self.log("\n✨ ALL TESTS PASSED!")
            self.log("The Ideation Engine is working correctly with real AI integration.")
        else:
            self.log("\n⚠️  SOME TESTS FAILED")
            self.log("Review the errors above and check your watsonx.ai configuration.")
        
        self.log("\n" + "="*70)


async def main():
    """Main test runner"""
    tester = IdeationIntegrationTest()
    success = await tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())


# Made with Bob