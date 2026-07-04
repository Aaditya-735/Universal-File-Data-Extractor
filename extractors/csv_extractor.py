from pathlib import Path

import pandas as pd

from extractors.base_extractor import BaseExtractor
from models.extraction_result import ExtractionResult
from utils.statistics import StatisticsGenerator


class CSVExtractor(BaseExtractor):
    
    def extract(self, file_path: str) -> ExtractionResult:
        
        dataframe = pd.read_csv(file_path)

        text = dataframe.to_string(index=False)
        size = Path(file_path).stat().st_size

        metadata = {
            "Rows": len(dataframe),
            "Columns": len(dataframe.columns),
            "File Size": f"{size} bytes"
        }

        statistics = StatisticsGenerator.generate(text)

        return ExtractionResult(
            file_name=file_path,
            file_type="CSV",
            text=text,
            metadata=metadata,
            statistics=statistics,
            tables=[dataframe.to_dict(orient="records")],
            images=[],
        )