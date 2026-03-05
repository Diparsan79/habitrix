
import json
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, Any, List

DATA_PATH = Path("data.json")
XP_PER_COMPLETION = 10

def today_iso() -> str:
    return date.today().isoformat()


def yesterday_iso() -> str:
    return (date.today() - timedelta(days=1)).isoformat()

def load_data() -> Dict[str, Any]:
    """Load JSON data from DATA_PATH. Create empty structure if missing."""
    if not DATA_PATH.exists():
        return {}
    try:
        return json.loads(DATA_PATH.read_text(encoding="utf-8"))
    except Exception:
        # if file corrupted, start fresh (safe fallback)
        return {}
def save_data(data: Dict[str, Any]) -> None:
    """Save JSON data (pretty-printed)."""
    DATA_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def ensure_habit_structure(habit: Dict[str, Any]) -> None:
    """Make sure a habit dict has required keys."""
    habit.setdefault("dates_completed", [])  # list of ISO dates
    habit.setdefault("streak", 0)             # current streak (int)
    habit.setdefault("xp", 0)                 # xp earned for that habit (int)

def list_sectors(data: Dict[str, Any]) -> List[str]:
    return sorted(data.keys())


def list_habits(data: Dict[str, Any], sector: str) -> List[str]:
    return sorted(data.get(sector, {}).keys())


def add_sector(data: Dict[str, Any], sector_name: str) -> None:
    if sector_name in data:
        print("Sector already exists.")
        return
    data[sector_name] = {}
    save_data(data)
    print(f"Sector '{sector_name}' added.")

def add_habit(data: Dict[str, Any], sector: str, habit_name: str) -> None:
    if sector not in data:
        print("Sector doesn't exist.")
        return
    if habit_name in data[sector]:
        print("Habit already exists in this sector.")
        return
    data[sector][habit_name] = {"dates_completed": [], "streak": 0, "xp": 0}
    save_data(data)
    print(f"Habit '{habit_name}' added to sector '{sector}'.")

def mark_habit_done(data: Dict[str, Any], sector: str, habit: str) -> None:
    """
    Mark today's completion for a habit.
    Rules:
     - If already marked today -> inform user
     - If last completed was yesterday -> streak += 1
     - Otherwise -> streak = 1 (either first time or missed day -> reset)
     - Add XP_PER_COMPLETION to habit xp and save today's date
    """
    ensure_habit_structure(data[sector][habit])
    h = data[sector][habit]
    today = today_iso()
    yesterday = yesterday_iso()