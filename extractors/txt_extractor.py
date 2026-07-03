from extractors.base_extractor import BaseExtractor

from models import ExtractionResult

from utils.metadata import MetadataExtractor
from utils.statistics import StatisticsGenerator


class TXTExtractor(BaseExtractor):

    def extract(self, file_path: str) -> ExtractionResult:

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        metadata = MetadataExtractor.extract(file_path)

        statistics = StatisticsGenerator.generate(text)

        return ExtractionResult(
            file_name=file_path,
            file_type="TXT",
            text=text,
            metadata=metadata,
            statistics=statistics
        )