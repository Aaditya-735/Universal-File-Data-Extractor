from core.app_logger import logger
from core.detector import FileDetector
from core.router import FileRouter

from extractors.pdf_extractor import extract as pdf_extract
from extractors.csv_extractor import extract as csv_extract

print("=" * 50)
print(" Universal File Data Extractor ")
print("=" * 50)

router = FileRouter()

router.register_route("PDF", pdf_extract)
router.register_route("CSV", csv_extract)

filename = "students.csv"

file_type = FileDetector.detect_file_type(filename)

logger.info(f"Detected File Type : {file_type}")

extractor = router.get_extractor(file_type)

extractor(filename)