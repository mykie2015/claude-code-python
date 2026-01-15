---
name: system2-thinking
description: Apply deliberate reasoning for complex design decisions. Use when exploring multiple options, analyzing trade-offs, or making architectural choices where System 1 fast intuition is insufficient.
---

# System 2 Thinking

## Overview

Apply structured deliberative reasoning for complex design and architectural decisions. This skill helps explore multiple paths, analyze trade-offs systematically, and select optimal solutions before implementation.

**When to use:**
- Making architectural or UX decisions with trade-offs
- Researching and synthesizing information from multiple sources
- When "System 1" fast intuition might miss important considerations
- **Test-Time Compute**: When you need to "think longer" by iterating on internal drafts
- **Self-Correction**: When complex logic requires an explicit verification loop to catch errors
- **Persistence**: When you need to track the history of major architectural decisions

## Core Principles

System 2 thinking contrasts with System 1 (fast, intuitive, error-prone):

| System 1 | System 2 |
|----------|----------|
| Quick answers | Deliberate exploration |
| Single path | Multiple alternatives |
| Confirmation bias | Systematic analysis |
| "Just do it" | "What are the options?" |
| One-shot generation | **Iterative Drafting & Self-Correction** |
| Assumes correctness | **Verifies logic internally** |

## Workflow

### 1. Explore Multiple Paths

Generate 3+ distinct approaches before evaluating any:

```
Explore: List all possible approaches (even bad ones)
  ├─ Path A: [Description]
  ├─ Path B: [Description]
  ├─ Path C: [Description]
  └─ Path N: [Wildcard/creative options]
```

### 2. Analyze Each Path

For each path, document:
- **Pros**: Advantages and strengths
- **Cons**: Limitations and risks
- **Complexity**: Implementation difficulty
- **Trade-offs**: What is gained vs. sacrificed

### 3. Simulate & Self-Correct (Test-Time Compute)

Before final selection, apply "Test-Time Compute" by simulating the execution of the top candidates:

1. **Drafting**: Mentally (or via scratchpad) draft the core logic/flow.
2. **Critique**: Actively look for flaws, edge cases, or logical gaps.
    *   "Self-Correction Loop": *If I implement this, where will it break?*
3. **Refine**: Fix the identified errors in the draft.

*Goal: Iterate on internal drafts before committing to a solution.*

### 4. Select Optimal Path

Choose based on:
- Best fit for user needs
- Lowest complexity for required functionality
- Extensibility for future requirements
- Alignment with existing patterns

### 5. Validate with External Research

For non-trivial decisions, validate with:
- Web search for best practices
- Documentation lookup (Context7)
### 6. Persist Decision

Log the thinking process for future reference.

```bash
python3 .claude/skills/system2-thinking/scripts/decision_tracker.py log \
    --topic "[Topic]" \
    --draft "[Initial thought]" \
    --critique "[Analysis/Critique]" \
    --final "[Selected Path]"
```

### 7. Review & Refine (Feedback Loop)

When new information arises or a decision is proven right/wrong, log feedback to improve future context.

```bash
# First find the decision ID
python3 .claude/skills/system2-thinking/scripts/decision_tracker.py search "[Topic]"

# Add feedback
python3 .claude/skills/system2-thinking/scripts/decision_tracker.py add-feedback \
    --id [ID] \
    --content "After implementation, we found that [new insight]... next time consider [improvement]"
```



## Practical Prompts

Use these as templates:

```
"Analyze [design/architecture problem] using System 2 thinking:
1. List 4+ distinct approaches
2. Analyze pros/cons of each
3. Select optimal path with rationale
4. Validate with research if needed"
```

```
"Apply System 2 reasoning to [complex decision]:
- Explore alternatives
- Analyze trade-offs systematically
- Recommend best approach with justification"
```

```
"Using a 'Test-Time Compute' approach:
1. Draft a solution for [problem]
2. Critically analyze the draft for 3 potential errors or limitations
3. Self-correct these errors
4. Present the final refined solution"
```

## Example: High-Scale Database Selection

### User Request
"Determine the backing store for a new User Activity Feed feature (10k writes/sec)."

### Step 1: Explore Paths

1.  **PostgreSQL** - Use existing relational cluster
2.  **Cassandra/Scylla** - Wide-column write-optimized store
3.  **DynamoDB** - Managed serverless NoSQL
4.  **Redis + SQL** - Hybrid buffer approach

### Step 2: Analyze

| Path | Pros | Cons |
|------|------|------|
| PostgreSQL | Familiar, ACID | Scale limits, maintenance |
| Cassandra | Massive write scale | High operational burden |
| DynamoDB | Low ops, auto-scale | Vendor lock-in, cost risk |
| Redis+SQL | Fast, absorbs spikes | Complex dual-write logic |

### Step 3: Simulate & Self-Correct
*   **Draft**: Choose DynamoDB for low ops.
*   **Critique**: How do we handle analytics queries? Dynamo cannot scan efficiently.
*   **Refine**: Add DynamoDB Streams -> BigQuery pipeline for analytics requirements.

### Step 4: Select
**DynamoDB** - Fits the specific access pattern (Key-Value lookup by UserID) and removes operational overhead for the team.

## Resources

### references/

- `database-selection-analysis.md`: Detailed trade-off analysis for high-throughput architecture

### scripts/

### scripts/

- `decision_tracker.py`: CLI tool to log and search decision history in a local SQLite database (`.claude/thinking_history.db`).
  - Usage: `python3 .claude/skills/system2-thinking/scripts/decision_tracker.py log ...`
  - Usage: `python3 .claude/skills/system2-thinking/scripts/decision_tracker.py search [query]`
  - Usage: `python3 .claude/skills/system2-thinking/scripts/decision_tracker.py add-feedback --id [ID] --content "[Feedback]"`

### assets/

No assets needed.
