from pathlib import Path

BASE = Path("decision-control-plane")

STRUCTURE = {
    "README.md": "",
    "requirements.txt": "python>=3.9\n",
    ".gitignore": "__pycache__/\n.env\n.venv/\n",
    "src/decision_control_plane/__init__.py": "",
    "src/decision_control_plane/core/__init__.py": "",
    "src/decision_control_plane/core/types.py": "",
    "src/decision_control_plane/core/ports.py": "",
    "src/decision_control_plane/core/domain.py": "",
    "src/decision_control_plane/infrastructure/__init__.py": "",
    "src/decision_control_plane/infrastructure/clock.py": "",
    "src/decision_control_plane/infrastructure/entropy.py": "",
    "src/decision_control_plane/governance/__init__.py": "",
    "src/decision_control_plane/governance/engine.py": "",
    "src/decision_control_plane/simulation/__init__.py": "",
    "src/decision_control_plane/simulation/stability.py": "",
    "src/decision_control_plane/app/__init__.py": "",
    "src/decision_control_plane/app/main.py": "",
}

def main():
    for path, content in STRUCTURE.items():
        full_path = BASE / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)

    print("✅ Repository structure created successfully.")

if __name__ == "__main__":
    main()
