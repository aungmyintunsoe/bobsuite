# 🧠 Ideation Engine - Usage Guide

## Overview

The Ideation Engine transforms IBM Bob into a proactive Technical Product Manager, helping you plan features through a structured 7-pillar framework before writing any code.

---

## 🚀 Quick Start

### Step 1: Initiate Planning Session

In IBM Bob's chat interface, simply say:

```
I want to plan a new feature
```

or

```
Help me create a PRD for [feature name]
```

Bob will automatically retrieve the ideation framework and begin guiding you through the planning process.

---

## 📋 The 7-Pillar Framework

Bob will guide you through these questions:

### 1. **What are we building?** (Description)
- Define the core objective
- Identify target audience
- Explain the primary value proposition

**Example Response:**
```
A real-time collaborative whiteboard application for distributed design teams 
to brainstorm and iterate on ideas together. Target users are remote design 
teams (5-20 people) who need to visualize concepts synchronously.
```

### 2. **What are we including?** (In Scope)
- List specific MVP features
- Be concrete and actionable
- Focus on "must-haves" for v1.0

**Example Response:**
```
- Real-time drawing tools (pen, shapes, text)
- Shape library with common UI elements
- User presence indicators
- Basic export to PNG/SVG
- User authentication and workspace management
- Undo/redo functionality
```

### 3. **What are we excluding?** (Out of Scope)
- Explicitly state what's NOT in this iteration
- Prevents feature creep
- Manages stakeholder expectations

**Example Response:**
```
- Video chat integration
- Advanced animation tools
- 3D modeling capabilities
- Mobile native apps (web-only for MVP)
- Offline mode
- Version history beyond basic undo/redo
```

### 4. **How might we build it?** (Implementation)
- Share initial technical thoughts
- Mention APIs, libraries, frameworks
- Describe architecture patterns

**Example Response:**
```
Frontend: React with HTML5 Canvas API for drawing, WebSocket for real-time 
sync. Backend: Node.js with Express, MongoDB for persistence, Redis for 
session management. Real-time: Socket.io for WebSocket connections. 
Authentication: JWT tokens with refresh mechanism.
```

### 5. **How do we know it works?** (Acceptance Criteria)
- Define measurable success criteria
- Be specific and testable
- Include performance benchmarks

**Example Response:**
```
- Multiple users can draw simultaneously with <100ms latency
- Changes sync across all connected clients in real-time
- No data loss on disconnect/reconnect
- Canvas supports minimum 1000 objects without lag
- Export generates valid PNG/SVG files
- 95% of users complete onboarding without help
```

### 6. **What's the timeline?** (Timeline)
- Break project into phases
- Set realistic milestones
- Include buffer time

**Example Response:**
```
Phase 1 (Weeks 1-2): Core drawing engine and canvas implementation
Phase 2 (Weeks 3-4): Real-time sync with WebSocket integration
Phase 3 (Weeks 5-6): User management, authentication, and workspaces
Phase 4 (Weeks 7-8): Polish, testing, and deployment
Target MVP: 8 weeks from kickoff
Beta launch: Week 9, Full launch: Week 10
```

### 7. **What resources do we need?** (Resources)
- Identify team composition
- List required tools and services
- Estimate budget

**Example Response:**
```
Team: 3 full-stack developers, 1 UX designer, 1 QA engineer
Infrastructure: AWS account with $300/month budget for hosting
Tools: GitHub for code, Figma for design, Linear for project management
Third-party services: 
  - WebSocket service (Pusher or similar, $50/month)
  - SendGrid for emails ($20/month)
Time commitment: 40 hours/week per team member
```

---

## 💡 Tips for Better PRDs

### Be Specific
❌ **Bad:** "The app should be fast"  
✅ **Good:** "API responses must return in <200ms for 95% of requests"

### Think About Edge Cases
Bob may ask follow-up questions like:
- "What happens if a user loses connection during collaboration?"
- "How will you handle conflicting edits?"
- "What's the maximum number of concurrent users?"

### Consider Constraints
Mention any limitations:
- Budget constraints
- Technical debt
- Team skill gaps
- Regulatory requirements

### Use Examples
Provide concrete examples when possible:
- "Similar to Figma's real-time cursors"
- "Authentication flow like GitHub's"
- "Export quality comparable to Canva"

---

## 🤖 How Bob Helps

### AI-Driven Follow-ups
Bob will ask clarifying questions based on your responses:

```
You: "We'll use React for the frontend"

Bob: "Great! Are you planning to use TypeScript or JavaScript? 
      And what state management approach - Redux, Context API, or something else?"
```

### Critique and Validation
Bob identifies potential gaps:

```
You: "Timeline is 2 weeks"

Bob: "That seems ambitious for a real-time collaborative app. 
      Have you considered time for WebSocket debugging and load testing? 
      Most similar projects take 6-8 weeks for MVP."
```

### Context-Aware Questions
Bob adapts based on your project type:

```
You: "Building a machine learning model"

Bob: "What's your training data strategy? 
      Do you have labeled datasets ready? 
      What's your model evaluation approach?"
```

---

## 📄 PRD Generation

### Automatic Synthesis
Once you've answered all 7 pillars, Bob will:

1. Validate your responses for completeness
2. Call the `synthesize_project_plan` tool
3. Use IBM watsonx.ai to generate a professional PRD
4. Return the PRD in chat
5. Save it to a file automatically

### Output Format
The generated PRD includes:

- **Overview Section** - Project description and goals
- **Scope Definition** - In/Out of scope features
- **Technical Requirements** - Architecture and tech stack
- **Success Criteria** - Measurable acceptance criteria
- **Timeline & Milestones** - Project phases
- **Resources & Team** - Required resources
- **Additional Sections** - Security, scalability, etc.

### File Location
PRDs are saved to:
```
mcp_server/lib/ideation/{project-name}-prd-{timestamp}.md
```

You can also specify a custom path:
```
Bob, save the PRD to /path/to/my-project/docs/prd.md
```

---

## 🔧 Advanced Usage

### Structured Data Format
If you're integrating programmatically, use this JSON structure:

```json
{
  "conversation_type": "structured",
  "pillars": {
    "description": {
      "answer": "Your answer here",
      "follow_ups": [
        {"q": "Follow-up question", "a": "Your answer"}
      ]
    },
    "in_scope": {"answer": "..."},
    "out_scope": {"answer": "..."},
    "implementation": {"answer": "..."},
    "acceptance": {"answer": "..."},
    "timeline": {"answer": "..."},
    "resources": {"answer": "..."}
  }
}
```

### Transcript Format
Alternatively, provide a raw conversation:

```json
{
  "conversation_type": "transcript",
  "messages": [
    {"role": "assistant", "content": "What are we building?"},
    {"role": "user", "content": "A task management app..."},
    {"role": "assistant", "content": "Who is the target audience?"},
    {"role": "user", "content": "Remote teams..."}
  ]
}
```

---

## 🧪 Testing Your Setup

Run the test suite to verify everything works:

```bash
cd mcp_server
python test_ideation.py
```

Expected output:
```
🧪 IDEATION ENGINE TEST SUITE
======================================================================

📋 UNIT TESTS

✓ PASS: Framework Retrieval
✓ PASS: Framework Structure
✓ PASS: Input Validation (Empty)
...

🔗 INTEGRATION TESTS

✓ PASS: PRD Synthesis (Structured)
✓ PASS: PRD Synthesis (File Save)

📊 TEST SUMMARY
======================================================================

Total Tests: 10
Passed: 10
Failed: 0
Success Rate: 100.0%

✨ All tests passed! Ideation Engine is ready to use.
```

---

## 📚 Example Conversation

Here's a complete example of how a planning session flows:

```
Developer: I want to plan a new feature

Bob: Great! Let's use the ideation framework to create a comprehensive PRD. 
     I'll guide you through 7 key questions.
     
     First, what are we building? Describe the core objective, target 
     audience, and primary value.

Developer: A Chrome extension that automatically summarizes long articles 
           using AI. Target users are busy professionals who need to quickly 
           understand content without reading everything.

Bob: Excellent! That's a clear value proposition. A few follow-ups:
     - What types of articles? News, blogs, academic papers, or all?
     - What's the ideal summary length?
     - Any specific industries or use cases in mind?

Developer: Primarily news articles and blog posts. Summaries should be 
           3-5 bullet points. Main use case is tech professionals staying 
           updated on industry news.

Bob: Perfect! Now, what are we including in the MVP? List the specific 
     features that MUST be in version 1.0.

Developer: - One-click summarization from any article page
           - 3-5 bullet point summaries
           - Copy summary to clipboard
           - Basic settings (summary length preference)
           - Works on major news sites (TechCrunch, Medium, etc.)

Bob: Good scope! What are we explicitly excluding from this iteration?

Developer: - Multi-language support (English only for MVP)
           - PDF summarization
           - Video/audio content
           - Sharing summaries with others
           - Browser sync across devices

Bob: Smart to keep it focused. How might we build it? Share your initial 
     technical thoughts.

Developer: Chrome Extension with Manifest V3, React for popup UI, 
           IBM watsonx.ai for summarization, content script to extract 
           article text, Chrome storage API for settings.

Bob: Solid tech stack! How do we know it works? Define your acceptance 
     criteria.

Developer: - Summaries generate in under 5 seconds
           - 90% accuracy in capturing key points (user survey)
           - Works on 95% of tested news sites
           - Extension loads without impacting page performance
           - Zero crashes in 1000 test summarizations

Bob: Measurable criteria - excellent! What's the timeline?

Developer: Week 1: Extension scaffold and content extraction
           Week 2: watsonx.ai integration
           Week 3: UI polish and settings
           Week 4: Testing and Chrome Web Store submission
           Target: 4 weeks to public launch

Bob: Finally, what resources do we need?

Developer: 1 full-stack developer (me), IBM watsonx.ai API access 
           ($50/month estimated), Chrome Web Store developer account ($5 one-time)

Bob: Perfect! I have everything I need. Let me synthesize this into a 
     comprehensive PRD...

[Bob generates PRD using watsonx.ai]

Bob: ✅ Here's your Product Requirements Document:

# AI Article Summarizer - Chrome Extension PRD

## Overview
A Chrome extension that uses IBM watsonx.ai to automatically generate 
concise 3-5 bullet point summaries of news articles and blog posts...

[Full PRD content]

---

**Generated:** 2026-05-16T13:00:00Z
**Saved to:** `ideation/ai-article-summarizer-prd-20260516-130000.md`

You're all set! Ready to start coding?
```

---

## 🎯 Best Practices

### 1. **Complete All Pillars**
Don't skip questions - each pillar serves a purpose in creating a comprehensive PRD.

### 2. **Be Honest About Constraints**
If you have limited time or budget, say so. Bob will help you scope appropriately.

### 3. **Iterate if Needed**
You can always run the process again to refine your PRD as requirements evolve.

### 4. **Save Your PRDs**
Keep generated PRDs in version control alongside your code for future reference.

### 5. **Share with Stakeholders**
Use the generated PRD to align your team before writing code.

---

## 🆘 Troubleshooting

### "Missing critical pillars" Error
**Problem:** You haven't answered all required questions.  
**Solution:** Ensure you've provided answers for: description, in_scope, acceptance, and timeline.

### "Response too short" Error
**Problem:** Your answers are too brief (< 20 characters).  
**Solution:** Provide more detailed responses. Bob needs context to generate quality PRDs.

### PRD Quality Issues
**Problem:** Generated PRD lacks detail or misses key points.  
**Solution:** Provide more comprehensive answers during the interview. The quality of output depends on input quality.

### File Save Failed
**Problem:** PRD generated but not saved to file.  
**Solution:** Check file permissions. The PRD is still returned in chat, so you can copy it manually.

---

## 📞 Support

For issues or questions:
1. Check the test suite: `python test_ideation.py`
2. Review ARCHITECTURE.md for technical details
3. Examine sample-prd.md for expected output format

---

**Made with IBM Bob** 🤖