# Tennis Stroke Phases - Biomechanics Requirements

## Overview

5-phase tennis stroke model with color coding and biomechanics metrics for each phase.

## Phase Color Mapping

| Phase | Color | Purpose |
|-------|-------|---------|
| 1: Preparation | Green (#22c55e) | Ready position, weight distribution |
| 2: Backswing | Yellow (#eab308) | Energy loading, racket loading |
| 3: Contact | Red (#ef4444) | Impact, peak velocity |
| 4: Follow-through | Blue (#3b82f6) | Deceleration, extension |
| 5: Recovery | Purple (#a855f7) | Balance restoration, court recovery |

## Phase 1: Preparation (Green)

**Goals**: Ready position, split step, weight distribution

### Metrics to Display
- Split Step Indicator: Pressure ring under feet (0-100% load)
- Shoulder Rotation Angle: Degrees relative to baseline (target: 45-90°)
- Unit Turn Marker: Lead shoulder to hip line (green)
- Center of Gravity (CoG): Balance point dot with stability indicator

### Key Joints
- Ankles (ground contact)
- Hips (weight distribution)
- Shoulders (rotation reference)

## Phase 2: Backswing (Yellow)

**Goals**: Energy storage, racket loading, X-factor stretch

### Metrics to Display
- Racket Tip Path: Yellow trail showing loop trajectory
- Elbow Flexion Angle: Live degrees (optimal: 90-110° for forehand)
- Loading Indicator: Dominant leg highlight (color intensity = load)
- Hip vs. Shoulder Gap: "X-factor" degrees (target: 30-45°)

### Key Joints
- Right elbow (righthanded)
- Right hip (loading side)
- Left shoulder (rotation reference)

## Phase 3: Contact (Red)

**Goals**: Peak transfer, impact precision, head stability

### Metrics to Display
- Impact Point: Flash effect at contact location
- Shoulder-Elbow-Wrist Alignment: Straight line (long lever check)
- Knee Extension Velocity: Vertical arrow (ground reaction force)
- Head Stability: Crosshair fixed on eyes (no lateral movement)

### Optimal Angles at Contact
- Racket: 45° above horizontal
- Left arm: Extended forward
- Knees: Slightly flexed (not fully extended)
- Shoulders: Open to target

## Phase 4: Follow-through (Blue)

**Goals**: Deceleration, extension, rotation completion

### Metrics to Display
- Extension Length: Shoulder to racket distance (forward reach)
- Deceleration Heatmap: Faded skeleton "ghosts" showing arm path
- Rotation Completion: Circular arrow with total degrees (shoulder turn completion)

### Key Joints
- Right wrist (racket follow)
- Left shoulder (rotation finish)
- Right hip (rotation tracking)

## Phase 5: Recovery (Purple)

**Goals**: Balance restoration, court positioning

### Metrics to Display
- Crossover Step Tracker: Ground path for first recovery step
- Balance Recovery Timer: Milliseconds to neutral "ready" stance
- Court Position: X-Y coordinates relative to center

### Success Criteria
- Recovery time: <500ms for competitive play
- Balance stability: <5cm CoG movement
- Court position: Moving toward center before recovery complete

## Joint Reference (COCO 17 Keypoints)

```
0:  nose
1:  left_eye
2:  right_eye
3:  left_ear
4:  right_ear
5:  left_shoulder
6:  right_shoulder
7:  left_elbow
8:  right_elbow
9:  left_wrist
10: right_wrist
11: left_hip
12: right_hip
13: left_knee
14: right_knee
15: left_ankle
16: right_ankle
```

## Skeleton Connections

- Shoulders: 5-6
- Arms: 5-7-9, 6-8-10
- Torso: 5-6-12-11
- Hips: 11-12
- Legs: 11-13-15, 12-14-16

## Phase Transition Rules

1. **Prep → Backswing**: Detected when racket starts upward motion
2. **Backswing → Contact**: Racket reaches maximum extension back
3. **Contact → Follow-through**: Impact moment (velocity peak)
4. **Follow-through → Recovery**: Racket passes hip, arm starts decelerating
5. **Recovery → Prep**: Player returns to balanced ready position
