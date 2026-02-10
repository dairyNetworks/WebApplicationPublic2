import json
import time
from pathlib import Path
from fastapi import FastAPI

def load_json_file(file_path: str):
    """Load a JSON file with timing and logging."""
    start_time = time.time()
    path = Path(file_path)

    if not path.exists():
        print(f"⚠️ JSON file not found: {file_path}")
        return []

    try:
        with open(path, encoding='utf-8-sig') as f:
            data = json.load(f)
        elapsed = time.time() - start_time
        print(f"✅ Loaded {len(data)} records from {file_path} in {elapsed:.3f}s")
        return data
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error in {file_path}: {e}")
        return []
    except Exception as e:
        print(f"❌ Unexpected error loading {file_path}: {e}")
        return []
