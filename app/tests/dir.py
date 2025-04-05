from pathlib import Path


try:
    temp_dir = Path(f"/tmp/zupra-mcp--4444")
    temp_dir.mkdir(parents=True, exist_ok=True)
    print(f"Directory created: {temp_dir.resolve()}")
except FileExistsError:
    print("Directory already exists")