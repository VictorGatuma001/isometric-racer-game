# Isometric Racer

A 3D-inspired top-down racing game with isometric perspective, realistic car physics, and AI opponents. Race 3 laps around a twisting track against three computer-controlled opponents in this retro-style racer.

## Features

- **Isometric 3D perspective** — Classic angled view (30° isometric projection) for visual depth
- **Realistic car physics** — Acceleration, braking, momentum, friction, and turning dynamics
- **3 AI opponents** — Each with independent pathfinding and racing behavior
- **Dynamic track** — Multiple waypoints with curves, width variations, and boundaries
- **Live race tracking** — Real-time lap counter, position standings, and race timer
- **Collision system** — Cars slide/bounce on grass when off-road; boundaries prevent complete derailment
- **Camera system** — Isometric camera follows the player car smoothly


## Installation & Running

**Requirements:** Python 3.12+, Pygame

```bash
git clone https://github.com/<your-username>/isometric-racer.git
cd isometric-racer
pip install -r requirements.txt
python3 main.py
```

## Controls

| Key | Action |
|---|---|
| `UP` / `W` | Accelerate |
| `DOWN` / `S` | Brake |
| `LEFT` / `A` | Steer left |
| `RIGHT` / `D` | Steer right |

Menu/Results: `SPACE` to continue

## Game Rules

1. **3 laps** to complete the race
2. **Stay on track** — grass slows you down (70% speed reduction)
3. **Beat the AI** — finish before they do
4. **No collisions** — cars pass through each other (focus is on speed, not bumper cars)

## Project Structure

```
isometric_racer/
├── main.py          # Entry point
├── game.py          # Game loop, states, and rendering
├── car.py           # Player car class with physics
├── ai_car.py        # AI opponent behavior and pathfinding
├── track.py         # Track generation, waypoints, collisions
├── iso_utils.py     # Isometric projection math utilities
├── constants.py     # Game configuration
├── requirements.txt
└── .gitignore
```

## Design Highlights

### Isometric Projection
The game uses a **30° isometric projection** to render a 3D perspective with 2D sprites. World coordinates are converted to screen coordinates using:

```python
iso_x = (x - y) * cos(30°)
iso_y = (x + y) * sin(30°)
```

This creates the classic tilted view without needing a full 3D engine.

### Car Physics
- **Acceleration** — Smooth speed increase when throttling
- **Inertia** — Speed doesn't instantly drop when releasing throttle
- **Turning radius** — Turning effectiveness increases with speed (drift simulator feel)
- **Friction** — Gradual slowdown when coasting
- **Off-road penalty** — Grass reduces speed by 30% to encourage staying on track

### AI Behavior
Each AI car:
1. **Pathfinding** — Follows waypoints around the track
2. **Waypoint switching** — Targets the next waypoint when close enough
3. **Steering** — Smoothly turns to face the target
4. **Throttle control** — Light throttle on sharp turns, full throttle on straights
5. **Speed** — Slightly slower than the player (5.5 vs 6.0 max speed)

The AI is fast enough to be competitive but beatable with good driving.

### Collision Detection
- **Track boundaries** — Cars bounce back and slow down when hitting grass
- **Car-to-car** — No collision (they pass through) to keep gameplay fast and focused
- **Lap detection** — Crossing the finish line registers a lap completion

## Possible Future Enhancements

- **Power-ups** — Speed boost, shield, slowdown traps
- **Multiple tracks** — Different courses with varying difficulty
- **Damage system** — Cars slow down if hit hard by walls
- **Multiplayer** — 2-player split-screen racing
- **Sound effects & music** — Engine sounds, collision SFX, background track
- **Particle effects** — Dust clouds, skid marks, explosions
- **Weather system** — Rain reduces traction, adds randomness
- **Leaderboard** — Track best times locally
- **Difficulty levels** — Easy/Normal/Hard AI

## Technical Notes

- **Isometric math** is in `iso_utils.py` — fully reversible (world ↔ screen conversion)
- **Physics simulation** runs at 60 FPS for smooth motion
- **No external assets** — All graphics generated programmatically
- **Modular design** — Track, cars, and AI are separate classes for easy extension

## License

MIT — do whatever you'd like with it.
