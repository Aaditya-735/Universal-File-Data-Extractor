from extractors.base_extractor import BaseExtractor
from models.extraction_result import ExtractionResult
from utils.metadata import MetadataExtractor
from utils.statistics import StatisticsGenerator
from pathlib import Path


class TXTExtractor(BaseExtractor):

    def extract(self, file_path: str) -> ExtractionResult:

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            encoding = "utf-8"
            line_count = len(text.splitlines())
            size = Path(file_path).stat().st_size

            metadata = {
                "Encoding": encoding,
                "Lines": line_count,
                "File Size": f"{size} bytes"
            }

        statistics = StatisticsGenerator.generate(text)

        return ExtractionResult(
            file_name=file_path,
            file_type="TXT",
            text=text,
            metadata=metadata,
            statistics=statistics
        )