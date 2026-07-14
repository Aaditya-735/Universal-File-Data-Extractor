import cv2
import re
import easyocr

from extractors.base_extractor import BaseExtractor
from models.extraction_result import ExtractionResult

from utils.image_metadata import ImageMetadataExtractor
from utils.statistics import StatisticsGenerator


class ImageExtractor(BaseExtractor):
    def __init__(self):
        self.reader = easyocr.Reader(
            ['en'],
            gpu=False
        )

    # --------------------------------------------------------
    # Image Preprocessing
    # --------------------------------------------------------

    def preprocess(self, image):

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        gray = cv2.resize(
            gray,
            None,
            fx=2,
            fy=2,
            interpolation=cv2.INTER_CUBIC
        )

        gray = cv2.fastNlMeansDenoising(gray)

        return gray

    # --------------------------------------------------------
    # Decide how image should be split
    # --------------------------------------------------------

    def split_image(self, image):

        height, width = image.shape[:2]

        # Very tall image
        # (documents, invoices, resumes etc.)
        if height > width * 1.6:
            return [image]

        # Very wide image
        # Split vertically
        if width > height * 1.6:

            half = width // 2

            return [
                image[:, :half],
                image[:, half:]
            ]

        # Square or product grid
        # Split into 4 quadrants

        half_h = height // 2
        half_w = width // 2

        q1 = image[:half_h, :half_w]
        q2 = image[:half_h, half_w:]
        q3 = image[half_h:, :half_w]
        q4 = image[half_h:, half_w:]

        return [
            q1,
            q2,
            q3,
            q4
        ]
    
        # --------------------------------------------------------
    # OCR Engine
    # --------------------------------------------------------

    def extract_text(self, image):

        image = self.preprocess(image)

       

        result = self.reader.readtext(
            image,
            paragraph=False,
            detail=1
        )

        words = []

        for box, text, conf in result:

            if conf < 0.45:
                continue

            x = min(point[0] for point in box)
            y = min(point[1] for point in box)

            words.append({
                "x": x,
                "y": y,
                "text": text
            })

        if not words:
            return ""

        words.sort(key=lambda w: (w["y"], w["x"]))

        lines = []

        current = []
        current_y = words[0]["y"]

        threshold = max(
            12,
            image.shape[0] // 70
        )

        for word in words:

            if abs(word["y"] - current_y) <= threshold:
                current.append(word)

            else:

                current.sort(key=lambda w: w["x"])

                lines.append(
                    " ".join(w["text"] for w in current)
                )

                current = [word]
                current_y = word["y"]

        if current:

            current.sort(key=lambda w: w["x"])

            lines.append(
                " ".join(w["text"] for w in current)
            )

        cleaned = []

        for line in lines:

            line = re.sub(r"\s+", " ", line)

            line = line.replace("|", "")
            line = line.replace("©", "")
            line = line.replace("®", "")

            line = line.strip()

            if len(line) == 1:
                continue

            cleaned.append(line)
            line = re.sub(r"[ ]{2,}", " ", line)
            line = line.strip(" .,-")

        return "\n".join(cleaned)

    
    # --------------------------------------------------------
    # Main Extraction Function
    # --------------------------------------------------------

    def extract(self, file_path: str) -> ExtractionResult:

        image = cv2.imread(file_path)

        if image is None:
            raise ValueError(f"Unable to read image: {file_path}")

        # Automatically decide how to split the image
        image_parts = self.split_image(image)

        extracted_sections = []

        for part in image_parts:

            section_text = self.extract_text(part)

            if section_text:
                extracted_sections.append(section_text)

        # Merge OCR output
        text = "\n\n".join(extracted_sections)

        # -------------------------
        # Final cleanup
        # -------------------------

        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove duplicate blank lines
        lines = []

        previous_blank = False

        for line in text.splitlines():

            line = line.strip()

            if line == "":

                if previous_blank:
                    continue

                previous_blank = True

            else:
                previous_blank = False

            lines.append(line)

        text = "\n".join(lines).strip()

        metadata = ImageMetadataExtractor.extract(file_path)

        statistics = StatisticsGenerator.generate(text)

        return ExtractionResult(
            file_name=file_path,
            file_type="IMAGE",
            text=text,
            metadata=metadata,
            statistics=statistics
        )