---
name: system2-thinking
description: Apply deliberate reasoning for complex design decisions. Use when exploring multiple options, analyzing trade-offs, or making architectural choices where System 1 fast intuition is insufficient.
---

# System 2 Thinking

## Overview

Apply structured deliberative reasoning for complex design and architectural decisions. This skill helps explore multiple paths, analyze trade-offs systematically, and select optimal solutions before implementation.

**When to use:**
- Exploring multiple design/architecture options
- Making architectural or UX decisions with trade-offs
- Researching and synthesizing information from multiple sources
- When "System 1" fast intuition might miss important considerations

## Core Principles

System 2 thinking contrasts with System 1 (fast, intuitive, error-prone):

| System 1 | System 2 |
|----------|----------|
| Quick answers | Deliberate exploration |
| Single path | Multiple alternatives |
| Confirmation bias | Systematic analysis |
| "Just do it" | "What are the options?" |

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

### 3. Select Optimal Path

Choose based on:
- Best fit for user needs
- Lowest complexity for required functionality
- Extensibility for future requirements
- Alignment with existing patterns

### 4. Validate with External Research

For non-trivial decisions, validate with:
- Web search for best practices
- Documentation lookup (Context7)
- AI assistant consultation (Gemini, Claude, etc.)

## Example: Skeleton Overlay UI Design

### User Request
"Design UI for skeleton overlay on tennis stroke video with 5 phases"

### Step 1: Explore Paths

1. **Canvas Overlay** - Draw skeleton directly on video canvas
2. **Header Button** - Modal/popup overlay toggled from header
3. **Transport Bar** - Controls integrated into video playback bar
4. **Right Panel** - Dedicated sidebar for skeleton info
5. **Toggle Mode + Interactive Panel** - Hybrid: transport toggle + right panel details

### Step 2: Analyze

| Path | Pros | Cons |
|------|------|------|
| Canvas Overlay | Seamless, performant | No controls visible |
| Header Button | Clean UI | Modal disrupts flow |
| Transport Bar | iMovie-style familiar | Limited space |
| Right Panel | Rich info | Complex, takes space |
| Hybrid | Best of both | More components |

### Step 3: Select
**Toggle Mode + Interactive Panel** - Balances simplicity with functionality, follows existing patterns.

### Step 4: Validate with External Research
Used Gemini to get phase-specific requirements for tennis biomechanics.

## Tennis Stroke Phases Reference

From Gemini research, phase-specific requirements:

**Phase 1: Preparation (Green)**
- Split Step Indicator: pressure ring under feet
- Shoulder Rotation Angle: 2D arc display
- Unit Turn Marker: shoulder-hip connection line
- Center of Gravity: balance point dot

**Phase 2: Backswing (Yellow)**
- Racket Tip Path: yellow trail/vector
- Elbow Flexion Angle: live degree readout
- Loading Indicator: dominant leg highlight
- Hip vs. Shoulder Gap: X-factor visualization

**Phase 3: Contact (Red)**
- Impact Point: flash effect at contact
- Shoulder-Elbow-Wrist: straight line check
- Knee Extension: vertical force arrow
- Head Stability: fixed crosshair on eyes

**Phase 4: Follow-through (Blue)**
- Extension Length: shoulder-to-racket distance
- Deceleration Heatmap: skeleton ghosts
- Rotation Completion: circular arrow

**Phase 5: Recovery (Purple)**
- Crossover Step: ground path tracking
- Balance Recovery: neutral stance timer

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

## Resources

### references/

- `tennis-phases.md`: Detailed phase requirements and biomechanics metrics

### scripts/

No scripts needed - this is a reasoning framework.

### assets/

No assets needed.
