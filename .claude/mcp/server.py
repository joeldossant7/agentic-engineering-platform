from mcp.server.fastmcp import FastMCP
from pathlib import Path
import json

mcp = FastMCP("skills-server")

BASE_DIR = Path(__file__).parent
SKILLS_DIR = BASE_DIR / "skills"
REGISTRY_PATH = BASE_DIR / "registry.json"

with open(REGISTRY_PATH, "r") as f:
    registry = json.load(f)


@mcp.tool()
def list_skills():
    return list(registry.keys())


@mcp.tool()
def load_skill(name: str):
    if name not in registry:
        return f"Skill '{name}' not found."

    skill_path = BASE_DIR / registry[name]

    with open(skill_path, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    mcp.run()

# IN PROGRESS: This server is a simple implementation to serve skills from the "skills" directory based on a registry defined in "registry.json". It provides two tools: one to list available skills and another to load the content of a specific skill.