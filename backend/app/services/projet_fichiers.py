from pathlib import Path

# Les dossiers qui doivent être ignorées
DEFAULT_IGNORED_DIRS = {
    ".git", 
    ".venv", "venv", 
    "__pycache__", ".pytest_cache", ".ruff_cache",
    "node_modules", "dist", "build",
}

"""
Prendre en paramètre le chemin du projet à analyser ainsi que
le nom des dossiers à ignorer que l'utilisateur lui meme peut donner
Et retourne une LISTE des fichiers Python découverts
"""

def discover_python_files(project_path: str | Path, ignored_dirs: set[str] | None = None,) -> list[Path]:
    root = Path(project_path)

    if not root.exists():
        raise FileNotFoundError(f"Le projet : {root} n'est pas trouvé.")
    if not root.is_dir():
        raise NotADirectoryError(f"Le chemin : {root} n'est pas un dossier.")

    ignored = DEFAULT_IGNORED_DIRS | (ignored_dirs or set())
    python_files = []
    for path in root.rglob("*.py"):
        relative_path = path.relative_to(root)

        if any(part in ignored for part in relative_path.parts[:-1]):
            continue

        if path.is_file():
            python_files.append(relative_path)

    return sorted(python_files)