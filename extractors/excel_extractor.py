from pathlib import Path

import pandas as pd

from extractors.base_extractor import BaseExtractor
from models import ExtractionResult, Metadata
from utils.statistics import StatisticsGenerator


class ExcelExtractor(BaseExtractor):
   
    def extract(self, file_path: str) -> ExtractionResult:
        
        dataframe = pd.read_excel(file_path)

        text = dataframe.to_string(index=False)

        metadata = Metadata(
            file_size=Path(file_path).stat().st_size
        )

        statistics = StatisticsGenerator.generate(text)

        return ExtractionResult(
            file_name=file_path,
            file_type="EXCEL",
            text=text,
            metadata=metadata,
            statistics=statistics,
            tables=[dataframe.to_dict(orient="records")],
            images=[],
        )