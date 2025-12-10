# utils.py
import os, sys, shutil
from pathlib import Path

def resource_path(rel_path: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel_path)

def ensure_persistent_db(bundled_name="study_tracker.db", persistent_folder_name=".studytracker"):
    """Copy bundled DB to user folder on first run and return persistent path."""
    home = Path.home()
    dest_dir = home / persistent_folder_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / bundled_name
    if not dest.exists():
        src = Path(resource_path(bundled_name))
        if src.exists():
            shutil.copy2(str(src), str(dest))
    return str(dest)
