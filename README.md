# Race of Math (Py-Race)
*A minimalist, top-down arcade racing experience built with Python and Pygame.*

---

## 2. Overview / Description
**Race of Math** (internally known as `py-race`) is a 2D top-down racing game where players control a car, avoiding traffic and chasing a flag to score points before time runs out. The project emphasizes clean code architecture and serves as a robust example of game development using `pygame`.

### Why it exists
This project was created to demonstrate:
- Modular game architecture in Python.
- Efficient 2D rendering and collision detection.
- A clean, scalable project structure suitable for education and expansion.

### Main Technologies
- **Python 3.x**
- **Pygame** (Rendering, Input, Sound)

## 3. Key Features
- **Arcade Gameplay**: Fast-paced driving with acceleration, drifting mechanics, and grass slowdowns.
- **Dynamic Traffic**: AI-controlled traffic that obeys road rules (mostly) and turns at intersections.
- **Interactive Map**: A tile-based map system with varying friction surfaces.
- **Objective System**: Chase the checkered flag to extend your time and boost your score.
- **Visual Feedback**: Tire tracks, collision alerts, and HUD overlays.
- **Procedural Generation**: Enter a seed to generate unique, deterministic track layouts every time you play.

## 4. Architecture Overview
The project follows a **domain-driven, modular architecture** to separate concerns and improve maintainability.

### Folder Structure
```
py-race/
├── src/
│   ├── assets/         # Game assets (images, sounds)
│   ├── core/           # Core engine systems (Camera, Loader, Settings)
│   ├── data/           # Static data configurations (Maps, Tile definitions)
│   ├── entities/       # Game objects (Player, Traffic, MapTiles)
│   ├── managers/       # Game logic managers (Game state, Scoring)
│   ├── ui/             # User Interface elements (HUD, Alerts)
│   └── main.py         # Application Entry Point
├── README.md           # Project Documentation
└── requirements.txt    # (Optional) Dependency list
```

### Main Modules
- **Core**: Handles the "engine" parts like the camera view (`camera.py`) and asset loading (`loader.py`).
- **Entities**: Contains classes for the `Player`, `Traffic` cars, and particle effects like `Tracks`.
- **Managers**: `game_manager.py` handles the game rules, scoring, and level logic.
- **Data**: `maps.py` defines the level layout using 2D arrays, separating data from logic.

## 5. Requirements
- **OS**: Windows, macOS, or Linux. (Tested primarily on Windows).
- **Hardware**: Basic GPU support recommended for smooth 60 FPS.
- **Dependencies**:
    - Python 3.6+
    - Pygame (`pip install pygame`)

## 6. Installation Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/michelbr84/py-race.git
   cd py-race
   ```

2. **Install Dependencies**
   Ensure you have Python installed, then run:
   ```bash
   pip install pygame
   ```

3. **Run the Project**
   Navigate to the project root and execute:
   ```bash
   python src/main.py
   ```
   *Note: Ensure you run it from the root directory so asset paths resolve correctly.*

## 7. Usage Guide
- **Launch**: Run `src/main.py`.
- **Objective**: Drive to the **Checkered Flag** to gain time and points. Avoid crashing into traffic!
- **Controls**:
    - **Arrow Keys**: Steer, Accelerate, Brake.
    - **P**: Reset Position.
    - **M**: Toggle Menu/Info.
    - **ESC**: Quit Game.

## 8. Configuration Options
Adjust gameplay settings in `src/core/settings.py`:
- `TRAFFIC_COUNT`: Number of AI cars (Default: 45).
- `COUNTDOWN_FULL`: Initial time limit.
- `FLAG_SCORE`: Points awarded per flag.

## 9. API Documentation
*Not applicable for this standalone game.*

## 10. Testing Instructions
Currently, the project relies on manual testing.
To verify functionality:
1. Run the game.
2. Ensure assets load without error.
3. Check collisions with borders and traffic.

## 11. ToDo / Roadmap

**Completed Tasks**
- [x] Full codebase refactoring (v2.0).
- [x] Separation of concerns (Entities vs Data).
- [x] Modular directory structure.
- [x] **Procedural Level Generation** (Seed-based).
- [x] **Start Menu** with Seed Input.
- [x] **Sound Effects Integration**.
- [x] **Advanced Features** (High Score, Levels, Settings).
- [x] Final Polish.

**In Progress**
- [ ] No active tasks.

**Planned / Future Tasks**
- [ ] Online Leaderboards.

## 12. Known Issues
- Traffic cars may occasionally overlap at spawn.
- Camera is hard-locked to player center; no smooth lerp yet.

## 13. Change Log
- **2025-12-10**: Major Refactoring to v2.0 structure. Separation of core, entities, and data.

## 14. Contributing Guidelines
1. Fork the repo.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add AmazingFeature'`).
4. Push to the branch.
5. Open a Pull Request.

**Code Style**: Follow PEP 8. Use 4 spaces for indentation.

## 15. How to Report Bugs
Please open an issue on GitHub using the template:
- **Description**: What happened?
- **Steps to Reproduce**: How can we see it?
- **Expected Behavior**: What should have happened?

## 16. License
Distributed under the MIT License. See `LICENSE.md` for more information.

## 17. FAQ
**Q: Can I change the map?**
A: Yes! Edit `src/data/maps.py` to modify the tile grid.

**Q: Why is the car slow on grass?**
A: It's a feature! Sticky friction is applied on non-road surfaces.

## 18. Credits
- **Developer**: Robin Duda (chilimannen) - Original Author.
- **Maintenance**: [Michel/Antigravity]
- **Assets**: OpenGameArt.org (Various authors).

## 19. Last Updated
*Last updated: 2025-12-10*
