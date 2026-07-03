from PIL import Image
import pytesseract

from extractors.base_extractor import BaseExtractor

from models import ExtractionResult

from utils.image_metadata import ImageMetadataExtractor
from utils.statistics import StatisticsGenerator


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\AG\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)


class ImageExtractor(BaseExtractor):

    def extract(self, file_path: str) -> ExtractionResult:

        image = Image.open(file_path)

        text = pytesseract.image_to_string(image)

        metadata = ImageMetadataExtractor.extract(file_path)

        statistics = StatisticsGenerator.generate(text)

        return ExtractionResult(
            file_name=file_path,
            file_type="IMAGE",
            text=text,
            metadata=metadata,
            statistics=statistics
        )