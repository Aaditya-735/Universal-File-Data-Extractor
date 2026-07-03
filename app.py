from core.detector import FileDetector
from core.router import FileRouter
from core.app_logger import setup_logger

from extractors.pdf_extractor import PDFExtractor
from extractors.docx_extractor import DOCXExtractor
from extractors.csv_extractor import CSVExtractor
from extractors.excel_extractor import ExcelExtractor
from extractors.txt_extractor import TXTExtractor
from extractors.image_extractor import ImageExtractor
from extractors.audio_extractor import AudioExtractor
from utils.exporter import Exporter


logger = setup_logger()


def display_result(result):
    
    print("\n" + "=" * 70)
    print("UNIVERSAL FILE DATA EXTRACTOR")
    print("=" * 70)

    print(f"File Name      : {result.file_name}")
    print(f"File Type      : {result.file_type}")

    print("\nMETADATA")
    print("-" * 70)

    for key, value in result.metadata.items():
        print(f"{key:<15}: {value}")

    print("\nSTATISTICS")
    print("-" * 70)
    print(f"Words          : {result.statistics.word_count}")
    print(f"Characters     : {result.statistics.character_count}")
    print(f"Lines          : {result.statistics.line_count}")
    print(f"Paragraphs     : {result.statistics.paragraph_count}")
    print(f"Reading Time   : {result.statistics.reading_time_minutes} min")

    print("\nEXTRACTED CONTENT")
    print("-" * 70)

    preview = result.text[:1000]

    print(preview)

    if len(result.text) > 1000:
        print("\n...Output Truncated...")


def main():

    router = FileRouter()

    router.register_route("PDF", PDFExtractor().extract)
    router.register_route("DOCX", DOCXExtractor().extract)
    router.register_route("CSV", CSVExtractor().extract)
    router.register_route("EXCEL", ExcelExtractor().extract)
    router.register_route("TXT",TXTExtractor().extract)
    router.register_route("IMAGE",ImageExtractor().extract)
    router.register_route("AUDIO",AudioExtractor().extract)

    print("=" * 70)
    print("Universal File Data Extractor")
    print("=" * 70)

    file_path = input("\nEnter file path : ").strip()

    file_type = FileDetector.detect_file_type(file_path)

    logger.info(f"Detected File Type : {file_type}")

    extractor = router.get_extractor(file_type)

    if extractor is None:
        print("\nUnsupported File Type")
        return

    result = extractor(file_path)

    display_result(result)

    Exporter.export_json(
        result,
        "outputs/result.json"
    )

    Exporter.export_text(
        result,
        "outputs/result.txt"
    )

    print("\nResults exported successfully.")

    print("JSON :", "outputs/result.json")

    print("TEXT :", "outputs/result.txt")


if __name__ == "__main__":
    main()