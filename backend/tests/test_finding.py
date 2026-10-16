import pytest

# J'importe mes classes dans finding ici 
from app.models.finding import (
    Confidence,
    Finding,
    FindingStatus,
    Severity,
)


def creer_finding():
    return Finding(
        scanner="bandit",
        rule_id="B602",
        title="Utilisation potentiellement dangeureuse de subprocess",
        severity=Severity.HIGH,
        confidence=Confidence.HIGH,
        file="src/commande.py",
        line=4,
        description="Une commande est exécutée avec shell=True.",
        recommendation="Éviter shell=True lorsque cela n'est pas nécessaire.",
    )

def test_creation_finding():
    finding = creer_finding()
    assert finding.scanner == "bandit"
    assert finding.rule_id == "B602"
    assert finding.severity == Severity.HIGH
    assert finding.confidence == Confidence.HIGH
    assert finding.file == "src/commande.py"
    assert finding.line == 4

def test_valeurs_par_defaut():
    finding = creer_finding()
    assert finding.status == FindingStatus.OPEN
    assert finding.evidence is None
    assert finding.cve is None
    assert finding.id != ""

# Vérifier si deux identifiants id de ma classe sont bien différent
def test_identifiants_differents():
    finding1 = creer_finding()
    finding2 = creer_finding()
    assert finding1.id != finding2.id

def test_champ_obligatoire_vide():
    with pytest.raises(ValueError):
        Finding(
            scanner="",
            rule_id="B602",
            title="Commande potentiellement dangereuse",
            severity=Severity.HIGH,
            confidence=Confidence.HIGH,
            description="Une commande est exécutée",
            recommendation="Éviter shell=True lorsque cela n'est pas nécessaire.",
        )

def test_numero_ligne_invalide():
    with pytest.raises(ValueError):
        Finding(
            scanner="",
            rule_id="B602",
            title="Commande potentiellement dangereuse",
            severity=Severity.HIGH,
            confidence=Confidence.HIGH,
            file="src/commande.py",
            line=0,
            description="Une commande est exécutée",
            recommendation="Éviter shell=True lorsque cela n'est pas nécessaire.",
        )