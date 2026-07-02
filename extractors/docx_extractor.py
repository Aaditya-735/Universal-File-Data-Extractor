from pathlib import Path

from docx import Document

from extractors.base_extractor import BaseExtractor
from models import ExtractionResult
from models.metadata import Metadata
from utils.statistics import StatisticsGenerator


class DOCXExtractor(BaseExtractor):
    
    def extract(self, file_path: str) -> ExtractionResult:
        
        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        extracted_text = "\n".join(paragraphs)

        properties = document.core_properties

        metadata = Metadata(
            author=properties.author or "",
            title=properties.title or "",
            subject=properties.subject or "",
            creator="Microsoft Word",
            page_count=0,  # DOCX doesn't directly expose page count
            file_size=Path(file_path).stat().st_size,
        )

        statistics = StatisticsGenerator.generate(extracted_text)

        return ExtractionResult(
            file_name=file_path,
            file_type="DOCX",
            text=extracted_text,
            metadata=metadata,
            statistics=statistics,
            tables=[],
            images=[],
        )