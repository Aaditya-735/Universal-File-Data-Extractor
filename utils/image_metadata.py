from pathlib import Path
from PIL import Image


class ImageMetadataExtractor:
    """
    Extract metadata from image files.
    """

    @staticmethod
    def extract(file_path: str) -> dict:
        image = Image.open(file_path)

        dpi = image.info.get("dpi", "Not Available")

        return {
            "File Size": f"{Path(file_path).stat().st_size} bytes",
            "Width": f"{image.width} px",
            "Height": f"{image.height} px",
            "Format": image.format,
            "Color Mode": image.mode,
            "DPI": dpi,
        }