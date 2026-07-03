from pathlib import Path


class FileDetector:
   

    SUPPORTED_TYPES = {
        ".pdf": "PDF",
        ".docx": "DOCX",
        ".xlsx": "EXCEL",
        ".xls": "EXCEL",
        ".csv": "CSV",
        ".txt": "TXT",
        ".png": "IMAGE",
        ".jpg": "IMAGE",
        ".jpeg": "IMAGE",
        ".mp3": "AUDIO",
        ".wav": "AUDIO",
        ".m4a": "AUDIO",
        ".flac": "AUDIO",
        ".aac":"AUDIO",
        
    }

    @classmethod
    def detect_file_type(cls, file_path: str) -> str:
       

        extension = Path(file_path).suffix.lower()

        if extension in cls.SUPPORTED_TYPES:
            return cls.SUPPORTED_TYPES[extension]

        raise ValueError(f"Unsupported file type: {extension}")