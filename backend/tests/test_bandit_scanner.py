import pytest

from app.services.bandit_scanner import scan_with_bandit


def test_detection_subprocess_shell_true(tmp_path):
    fichier = tmp_path / "unsafe.py"

    fichier.write_text(
        "import subprocess\n"
        "\n"
        "def executer(commande):\n"
        "   subprocess.run(commande, shell=True)\n",
        encoding="utf-8",
    )

    findings = scan_with_bandit(tmp_path)
    assert any(finding.rule_id == "B602" for finding in findings)

def test_project_sans_alerte_connue(tmp_path):
    fichier = tmp_path / "main.py"

    fichier.write_text(
        "def addition(a, b):\n"
        "   return a + b\n",
        encoding="utf-8",
    )

    findings = scan_with_bandit(tmp_path)
    assert findings == []

def test_projet_inexistant(tmp_path):
    chemin = tmp_path / "inexistant"

    with pytest.raises(FileNotFoundError):
        scan_with_bandit(chemin)

def test_chemin_qui_est_un_fichier(tmp_path):
    fichier = tmp_path / "main.py"

    fichier.write_text("print('bonjour')", encoding="utf-8")

    with pytest.raises(NotADirectoryError):
        scan_with_bandit(fichier)

def test_scanner_ignore_les_dossiers_exclus(tmp_path):
    dossier_env = tmp_path / ".venv"
    dossier_env.mkdir()

    fichier = dossier_env / "unsafe.py"
    fichier.write_text(
        "import subprocess\n"
        "subprocess.run('commande', shell=True)\n",
        encoding="utf-8",
    )

    findings = scan_with_bandit(tmp_path)
    assert findings == []