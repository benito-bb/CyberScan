import json
import subprocess
import sys
from pathlib import Path

from app.models.finding import Confidence, Finding, Severity
from app.services.projet_fichiers import discover_python_files

"""
Analyse un projet Python avec Bandit
Paramètre : chemin du projet à analyser.
Et retourne : La liste des découvertes converties en objets Finding

Raises: si le projet n'existe pas, si le chemin est un fichier ou si Bandit ne peut pas fait d'analyse
"""

def scan_with_bandit(project_path: str | Path) -> list[Finding]:
    root = Path(project_path).resolve()

    # Récuperer les fichiers à analyser avec notre fonction dans projet_fichiers
    python_files = discover_python_files(root)

    if not python_files:
        return []

    # Puis construire la commande de Bandit sur nos fichiers récupérer
    command = [sys.executable, "-m", "bandit", "-f", "json", "-q", 
               *[str((root / path).resolve()) for path in python_files],]

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    
    # Bandit peut renvoyer 1 lorsque des problèmes sont détectés
    # Cela n'indique nécessairement une erreur d'exécution
    if completed.returncode not in (0, 1):
        raise RuntimeError(
            "L'analyse Bandit a échoué : "
            f"{completed.stderr.strip()}"
        ) 

    try:
        report = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError("Impossible de lire le résultat JSON de bandit.") from error

    findings = []
    for result in report.get("results", []):
        filename = Path(result["filename"])

        if not filename.is_absolute():
            filename = root / filename

        try:
            relative_filename = (filename.resolve().relative_to(root).as_posix())
        except ValueError as error:
            raise RuntimeError("Bandit a renvoyé un fichier situé en dehors du projet analysé.") from error

        severity = Severity(result["issue_severity"].lower())
        confidence = Confidence(result["issue_confidence"].lower())
        rule_id = result["test_id"]
        description = result["issue_text"]

        finding = Finding(
            scanner="bandit",
            rule_id=rule_id,
            title=result.get("test_name", description),
            severity=severity,
            confidence=confidence,
            file=relative_filename,
            line=result.get("line_number"),
            description=description,
            recommendation=(
                f"Examiner la règle Bandit {rule_id} et corriger le code si le problème est confirmé."
                "Consulter la documentation de la règle pour adaptées votre correction."
            ),
        )

        findings.append(finding)

    return findings