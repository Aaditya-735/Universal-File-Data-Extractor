from dataclasses import dataclass, field
from models.statistics import Statistics
from typing import Dict, Any


@dataclass(slots=True)
class ExtractionResult:
    
    file_name: str

    file_type: str

    text: str

    metadata: Dict[str, Any] = field(default_factory=dict)

    statistics: Statistics = field(default_factory=Statistics)

    tables: list = field(default_factory=list)

    images: list = field(default_factory=list)