from dataclasses import dataclass, field
from enum import StrEnum
from uuid import uuid4


# La classe de la gravité de notre problème
class Severity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# La classe pour le niveau de confiance accordé à la détection
class Confidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# La classe pour statut de la découverte
class FindingStatus(StrEnum):
    OPEN = "open"
    CONFIRMED = "confirmed"
    FALSE_POSITIVE = "false_positive"
    FIXED = "fixed"
    ACCEPTED_RISK = "accepted_risk"

# La classe Finding décrit les informations qu'une découverte doit gérer
@dataclass
class Finding:
    scanner : str
    rule_id : str
    title : str
    severity : Severity
    confidence : Confidence
    description : str
    recommendation : str

    file : str | None = None
    line : int | None = None
    evidence : str | None = None
    cve : str | None = None

    status : FindingStatus = FindingStatus.OPEN
    #Générer un identifiant unique de type UUID adapté à l'identification de la découvertes
    id : str = field(default_factory=lambda: str(uuid4()))

    # Les infos obligatoires que doivent contenir la description de mes problèmes
    def __post_init__(self):
        required_fields = {
            "scanner" : self.scanner,
            "rule_id" : self.rule_id,
            "title" : self.title,
            "description" : self.description,
            "recommendation" : self.recommendation,
        }

        for name, value in required_fields.items():
            if not value.strip():
                raise ValueError(f"Attribut '{name}' ne peut pas être vide.")

        if self.line is not None and self.line < 1:
            raise ValueError("Numéro de ligne doit être supérieur à 0.")