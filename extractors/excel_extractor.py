from pathlib import Path

import pandas as pd

from extractors.base_extractor import BaseExtractor
from models.extraction_result import ExtractionResult
from utils.statistics import StatisticsGenerator


class ExcelExtractor(BaseExtractor):
   
    def extract(self, file_path: str) -> ExtractionResult:
        
        dataframe = pd.read_excel(file_path)

        text = dataframe.to_string(index=False)
        size = Path(file_path).stat().st_size

        rows = len(dataframe)
        cols = len(dataframe.columns)
        excel = pd.ExcelFile(file_path)

        metadata = {
            "Sheets": len(excel.sheet_names),
            "Rows": rows,
            "Columns": cols,
            "File Size": f"{size} bytes"
        }

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