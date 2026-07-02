from pathlib import Path

import streamlit as st

from core.detector import FileDetector
from core.router import FileRouter

from extractors.pdf_extractor import PDFExtractor
from extractors.docx_extractor import DOCXExtractor
from extractors.csv_extractor import CSVExtractor
from extractors.excel_extractor import ExcelExtractor

from utils.exporter import Exporter


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Universal File Data Extractor",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Universal File Data Extractor")
st.write("Extract information from PDF, DOCX, CSV and Excel files.")

# -----------------------------
# Router
# -----------------------------

router = FileRouter()

router.register_route("PDF", PDFExtractor().extract)
router.register_route("DOCX", DOCXExtractor().extract)
router.register_route("CSV", CSVExtractor().extract)
router.register_route("EXCEL", ExcelExtractor().extract)

# -----------------------------
# Upload
# -----------------------------

uploaded_file = st.file_uploader(
    "Choose a file",
    type=["pdf", "docx", "csv", "xlsx"]
)

if uploaded_file:

    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    file_path = upload_dir / uploaded_file.name

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    if st.button("Extract Data"):

        file_type = FileDetector.detect_file_type(str(file_path))

        extractor = router.get_extractor(file_type)

        if extractor is None:
            st.error("Unsupported File Type")
            st.stop()

        result = extractor(str(file_path))

        Exporter.export_json(
            result,
            "outputs/result.json"
        )

        Exporter.export_text(
            result,
            "outputs/result.txt"
        )

        st.success("Extraction Completed")

        # ------------------------
        # File Information
        # ------------------------

        st.header("File Information")

        col1, col2 = st.columns(2)

        col1.write("**File Name**")
        col1.write(result.file_name)

        col2.write("**File Type**")
        col2.write(result.file_type)

        # ------------------------
        # Metadata
        # ------------------------

        st.header("Metadata")

        st.write(f"**Author:** {result.metadata.author}")
        st.write(f"**Title:** {result.metadata.title}")
        st.write(f"**Pages:** {result.metadata.page_count}")
        st.write(f"**File Size:** {result.metadata.file_size} bytes")

        # ------------------------
        # Statistics
        # ------------------------

        st.header("Statistics")

        c1, c2, c3 = st.columns(3)

        c1.metric("Words", result.statistics.word_count)
        c2.metric("Characters", result.statistics.character_count)
        c3.metric("Lines", result.statistics.line_count)

        c4, c5 = st.columns(2)

        c4.metric("Paragraphs", result.statistics.paragraph_count)
        c5.metric(
            "Reading Time",
            f"{result.statistics.reading_time_minutes} min"
        )

        # ------------------------
        # Text
        # ------------------------

        st.header("Extracted Content")

        st.text_area(
            "",
            result.text,
            height=400
        )

        # ------------------------
        # Downloads
        # ------------------------

        st.header("Download")

        with open(
            "outputs/result.json",
            "rb"
        ) as file:

            st.download_button(
                "Download JSON",
                data=file,
                file_name="result.json",
                mime="application/json"
            )

        with open(
            "outputs/result.txt",
            "rb"
        ) as file:

            st.download_button(
                "Download TXT",
                data=file,
                file_name="result.txt",
                mime="text/plain"
            )