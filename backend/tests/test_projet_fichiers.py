from pathlib import Path

import pytest

from app.services.projet_fichiers import discover_python_files


# Créer un ensemble de dossier projet avec fichiers pour tester ma 
# fonction de découvertes des fichiers que mon logiciel analysera
def test_decouverte_fichiers_python(tmp_path):
    (tmp_path / "main.py").write_text("print('bonjour')", encoding="utf-8",)
    (tmp_path / "README.md").write_text("# Mon projet", encoding="utf-8",)

    utils = tmp_path / "utils"
    utils.mkdir()
    (utils / "calculs.py").write_text("def addition(a, b):\n    return a+b", encoding="utf-8",)

    result = discover_python_files(tmp_path)
    assert result == [
        Path("main.py"),
        Path("utils/calculs.py"),
    ]

def test_dossiers_par_defaut_ignores(tmp_path):
    (tmp_path / "main.py").write_text("print('bonjour')", encoding="utf-8",)

    venv = tmp_path / ".venv"
    venv.mkdir()
    (venv / "package.py").write_text("print('fichier virtuel')", encoding="utf-8",)

    result = discover_python_files(tmp_path)
    assert result == [
        Path("main.py"),
    ]

def test_dossier_personnalise_ignore(tmp_path):
    (tmp_path / "main.py").write_text("print('bonjour')", encoding="utf-8",)

    archives = tmp_path / "archives"
    archives.mkdir()
    (archives / "ancien.py").write_text("print('ancien fichier')", encoding="utf-8",)

    result = discover_python_files(tmp_path, ignored_dirs={"archives"},)
    assert result == [
        Path("main.py"),
    ]

def test_projet_inexistant(tmp_path):
    chemin_inexistant = tmp_path / "inexistant"

    with pytest.raises(FileNotFoundError):
        discover_python_files(chemin_inexistant)

def test_chemin_vers_fichier(tmp_path):
    fichier = tmp_path / "main.py"
    fichier.write_text("print('bonjour')", encoding="utf-8")

    with pytest.raises(NotADirectoryError):
        discover_python_files(fichier)