from pathlib import Path

import fitz  # PyMuPDF



class MetadataExtractor:
    
    @staticmethod
    def extract(file_path: str) -> dict:
        
        pdf = fitz.open(file_path)

        info = pdf.metadata

        author = info.get("author", "")
        title = info.get("title", "")
        pages = pdf.page_count
        file_size = Path(file_path).stat().st_size

            
        result = {
            "Author": author,
            "Title": title,
            "Pages": pages,
            "File Size": f"{file_size} bytes"
        }
        

        pdf.close()

        return result
        