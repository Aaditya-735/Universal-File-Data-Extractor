from pathlib import Path

import fitz  # PyMuPDF

from models import Metadata


class MetadataExtractor:
    
    @staticmethod
    def extract(file_path: str) -> Metadata:
        
        pdf = fitz.open(file_path)

        info = pdf.metadata

        metadata = Metadata(
            author=info.get("author", ""),
            title=info.get("title", ""),
            subject=info.get("subject", ""),
            creator=info.get("creator", ""),
            producer=info.get("producer", ""),
            page_count=pdf.page_count,
            creation_date=info.get("creationDate", ""),
            modification_date=info.get("modDate", ""),
            file_size=Path(file_path).stat().st_size,
        )

        pdf.close()

        return metadata