---
name: "vibe-coding-learning"
description: "Generate structured learning notes from AI coding sessions. Invoke when user completes a coding task with AI and asks to summarize learning, explain code, extract knowledge points, review previous notes, or check learning progress."
---

# Vibe Coding Learning

Transform AI coding sessions into structured learning notes. Help CS students actually learn from vibe coding instead of just generating code.

## Use this skill when

- User just completed a coding task with AI and wants a learning summary
- User says "summarize today's learning", "explain this code", "extract knowledge points"
- User says "help me review", "what did I learn before", "review yesterday's notes"
- User says "learning progress", "what should I learn next", "learning calendar"
- User says "prepare for interview", "面试怎么讲", "帮我准备面试", "模拟面试"
- User references "vibe coding learning", "learning note", "knowledge card"

## Do NOT use this skill when

- User is still in the middle of coding and has NOT asked for a summary
- User only wants code review, bug fixing, or refactoring without learning context
- User asks about non-programming topics

## Input

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `coding_context` | string | Yes | What the user built with AI in this session |
| `changed_files` | list | Auto-detected | Files created or modified (scan project if not provided) |
| `preferred_format` | string | No | `md` (default) or `html` |
| `output_dir` | string | No | Directory to save notes (default: `learning-notes/`) |

## Output

| Artifact | Format | Description |
|----------|--------|-------------|
| Daily learning note | Markdown/HTML | Structured note with knowledge points, code explanation, pitfalls |
| Knowledge point cards | Markdown | Reusable cards for each extracted concept |
| Calendar entry | Markdown | Entry appended to monthly learning calendar |
| Progress update | Markdown | Updated progress overview |

## Workflow

### Mode 1: Generate Learning Note (after coding session)

Execute these steps in order:

**Step 1 — Collect Context**
- Scan the project directory to identify files created or modified during this session
- If user provided `coding_context`, use it as the primary description
- Read the key source files to understand what was built

**Step 2 — Identify Technical Domain and Stack**
- Analyze the code to determine which domain(s) and tech stack(s) it belongs to:
  - **Domains**: backend, frontend, devops, ai-ml, mobile, data-engineering, security, testing, cloud
  - **Stacks** (examples): fastapi, django, express, react, vue, vanilla-js, docker, kubernetes, langchain, pytorch
- A session may span multiple domains and stacks

**Step 3 — Extract Knowledge Points**
- From the code changes, identify 3-8 concrete knowledge points
- For each knowledge point, define:
  - Name (e.g., "JWT Authentication", "React useState Hook")
  - One-sentence definition
  - Core concept / how it works
  - Which file and line range implements it
  - Common mistakes / pitfalls
- Knowledge points should be things a CS student would encounter in coursework or interviews

**Step 4 — Write Code Explanation**
- Determine the recommended reading order (which file first, which function first)
- For each key file, write:
  - What this file does in plain language
  - Line-by-line or section-by-section explanation
  - Why it's designed this way (not just what it does)
  - What design pattern it uses (if any)
  - How to write it from scratch without AI

**Step 5 — Compile Pitfalls**
- List 3-5 common mistakes for this domain
- Format: table with columns [Pitfall, Correct Approach, Common Mistake]
- Base this on both the code analysis and general domain knowledge

**Step 6 — Recommend Learning Resources**
- Use WebSearch to find relevant tutorials for each knowledge point
- Search queries: "[knowledge point] tutorial bilibili", "[knowledge point] official documentation"
- Prioritize: Bilibili video tutorials, official docs, well-known tech blogs
- Provide 1-3 resources per knowledge point with title and URL
- If WebSearch fails, provide recommendations from general knowledge

**Step 7 — Update Learning Calendar and Progress**
- Check if `learning-notes/calendar/YYYY-MM.md` exists. If not, create it.
- Append today's entry to the calendar:
  ```
  | YYYY-MM-DD | [domain] | [keywords] | [link to note] |
  ```
- Check if `learning-notes/progress.md` exists. If not, create it.
- Update domain progress bars and statistics

**Step 8 — Save to Three-Layer Structure**

Save outputs to the appropriate locations in the three-layer directory structure:

1. **topics/** — Save the daily learning note
   - Create a project-specific folder: `topics/[project-name]/`
   - Save note as: `topics/[project-name]/YYYY-MM-DD-[title].md`
   - Example: `topics/fastapi-login-register/2026-06-11-fastapi-login-register.md`

2. **domains/** — Update the domain and stack indexes
   - Determine the domain (e.g., `backend`) and stack (e.g., `fastapi`)
   - Create or update `domains/[domain]/_index.md` with knowledge checklist
   - Create or update `domains/[domain]/[stack]/_index.md` with stack-specific notes
   - Link back to the topic note from the domain index

3. **cards/** — Save extracted knowledge point cards
   - Determine the card category (e.g., `auth`, `css`, `js`, `python`)
   - Create the category folder if it doesn't exist: `cards/[category]/`
   - Save each card as: `cards/[category]/[kebab-case-name].md`
   - Example: `cards/auth/jwt.md`, `cards/css/flexbox.md`
   - Cards should be self-contained and reusable across any project

**Step 9 — Generate Output Files**
- Generate the daily learning note following the template at `templates/daily-learning-note.md`
- Save to the appropriate topic folder
- If `preferred_format` is `html`, generate an HTML version using the html-report skill

### Mode 2: Review Previous Learning (on user request)

When user asks to review or recall previous learning:

1. Read `learning-notes/progress.md` to get the full learning overview
2. If user specifies a date/topic: read the corresponding note file from `topics/`
3. If user says "yesterday" or "recent": find the most recent calendar entry
4. Present a quiz-style review:
   - First, list the knowledge points WITHOUT code (test recall)
   - Ask the user to explain the core logic in their own words
   - Then reveal the code explanation for comparison
   - Mark knowledge points the user struggled with

### Mode 3: Learning Progress Check (on user request)

When user asks about overall progress:

1. Read `learning-notes/progress.md`
2. Present:
   - Total learning days, domains covered, knowledge points count
   - Per-domain progress with visual progress bars
   - Recent learning calendar (last 7 days)
   - Suggested next topics based on gaps

### Mode 4: Interview Preparation (on user request)

**IMPORTANT**: Only trigger this mode when user explicitly mentions interview/job preparation. Do NOT include interview content in daily learning notes by default.

When user asks for interview preparation:

1. **Gather context** — Read `learning-notes/progress.md` and `learning-notes/domains/` to understand what the user has learned
2. **Identify relevant knowledge** — Scan knowledge point cards in `learning-notes/cards/` and recent topic notes for content that matches the user's target role
3. **Generate interview output**:
   - **30-second summary** for each major project/domain: concise enough for a quick self-introduction
   - **90-second deep-dive** for key technical choices: explain WHY you chose certain technologies
   - **Common interview questions** for the learned tech stack with suggested answers based on actual experience
   - **Weakness analysis**: identify gaps between what was learned and common interview expectations for the target role
4. **If user says "模拟面试" (mock interview)**:
   - Randomly pick 3-5 knowledge points from their cards
   - Ask each as an interview question, wait for the user's response
   - Provide feedback: what was good, what was missing, how to improve

**Interview question generation rules**:
- Draw questions from the user's actual learned content, not generic lists
- For backend roles: focus on auth flows, database design, API design, error handling
- For frontend roles: focus on component design, state management, performance, responsive design
- For full-stack roles: ask about integration decisions, data flow, debugging approaches
- Always reference the user's specific project experience when formulating questions

**Target role mapping** (use when user specifies a target role):

| Target Role | Priority Domains | Interview Focus |
|-------------|-----------------|-----------------|
| 后端开发(实习) | backend, database, security | API design, auth, database optimization |
| 前端开发(实习) | frontend, css, js | Component design, responsive, performance |
| 全栈开发(实习) | backend, frontend, devops | Integration, data flow, deployment |
| AI 应用(实习) | ai-ml, python | RAG, prompt engineering, LLM integration |
| 测试开发(实习) | testing, devops | Test design, CI integration, automation |

## Writing Rules

- Write in plain Chinese. Explain technical terms the first time they appear.
- Target audience: CS undergraduate students who use AI coding tools
- Always include concrete file paths and line references from the actual project
- Include reading guidance: "read this function first, then see where it's called"
- Be honest about uncertainty — if something is ambiguous, say so
- Keep each daily note focused on ONE session, not a general overview
- Knowledge point cards should be self-contained and reusable across sessions

## Note Template

Follow the template structure defined in `templates/daily-learning-note.md`.

## Directory Structure for Learning Notes

The learning notes use a **three-layer architecture** for scalability:

```
learning-notes/
├── README.md                    # Overview dashboard & usage guide
├── progress.md                  # Progress tracking across all domains
├── calendar/
│   └── YYYY-MM.md              # Monthly learning calendar
│
├── topics/                      # Layer 1: Project/session-based notes
│   └── [project-name]/          # One folder per coding project/session
│       └── YYYY-MM-DD-[title].md
│
├── domains/                     # Layer 2: Domain & stack indexes
│   └── [domain]/                # e.g., backend, frontend, devops, ai-ml
│       ├── _index.md            # Domain-level knowledge checklist
│       └── [stack]/             # e.g., fastapi, react, docker
│           └── _index.md        # Stack-specific notes & progress
│
└── cards/                       # Layer 3: Reusable knowledge cards
    └── [category]/              # e.g., auth, css, js, python, database
        └── [card-name].md       # Self-contained, cross-topic reusable
```

### Three-Layer Design Rationale

| Layer | Purpose | When to Create | Example |
|-------|---------|---------------|---------|
| **topics/** | Raw session notes tied to a specific project | Every new coding session | `topics/fastapi-login-register/` |
| **domains/** | Curated indexes organized by tech domain/stack | When a new domain or stack is encountered | `domains/backend/fastapi/` |
| **cards/** | Atomic, reusable knowledge nuggets | When extracting a reusable concept | `cards/auth/jwt.md` |

This structure ensures:
- **Scalability**: Adding a new tech stack only requires creating a new `domains/[domain]/[stack]/` folder
- **Reusability**: Knowledge cards in `cards/` can be referenced by any future project
- **Discoverability**: Domain indexes provide a curated view of what you've learned per tech area
- **No flat-folder bloat**: Cards are categorized so no single folder grows too large

## Card Category Guidelines

When saving knowledge point cards, use these standard categories (create new ones as needed):

| Category | For |
|----------|-----|
| `auth/` | Authentication, authorization, JWT, OAuth, bcrypt, session management |
| `css/` | CSS properties, layout, animation, responsive design |
| `js/` | JavaScript language features, DOM, events, async |
| `ts/` | TypeScript types, generics, decorators |
| `python/` | Python language, FastAPI, Django, SQLAlchemy |
| `database/` | SQL, ORM, indexing, transactions |
| `devops/` | Docker, K8s, CI/CD, Terraform |
| `ai-ml/` | LLM, RAG, LangChain, PyTorch |
| `security/` | OWASP, XSS, CSRF, encryption |
| `testing/` | Unit test, integration test, E2E |

## On Failure

- If no code files can be found: ask the user to specify which files were created/modified
- If WebSearch returns no results: skip tutorial recommendations, use general knowledge instead
- If output directory is not writable: inform the user and suggest an alternative path
- If the session is too trivial (e.g., only changed a CSS color): suggest skipping note generation
