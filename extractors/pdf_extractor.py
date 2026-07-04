from typing import Any

import pdfplumber

from extractors.base_extractor import BaseExtractor
from models.extraction_result import ExtractionResult
from utils.metadata import MetadataExtractor
from utils.statistics import StatisticsGenerator


class PDFExtractor(BaseExtractor):
   
    def extract(self, file_path: str) -> ExtractionResult:
        
        text = ""

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        metadata = MetadataExtractor.extract(file_path)

        statistics = StatisticsGenerator.generate(text)

        return ExtractionResult(
            file_name=file_path,
            file_type="PDF",
            text=text,
            metadata=metadata,
            statistics=statistics,
            tables=[],
            images=[],
        )