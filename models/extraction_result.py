from dataclasses import dataclass, field

from models.metadata import Metadata
from models.statistics import Statistics


@dataclass(slots=True)
class ExtractionResult:
    
    file_name: str

    file_type: str

    text: str

    metadata: Metadata = field(default_factory=Metadata)

    statistics: Statistics = field(default_factory=Statistics)

    tables: list = field(default_factory=list)

    images: list = field(default_factory=list)