import os
import whisper
import shutil
import subprocess

from extractors.base_extractor import BaseExtractor
from models.extraction_result import ExtractionResult
from utils.audio_metadata import AudioMetadataExtractor
from utils.statistics import StatisticsGenerator




 

class AudioExtractor(BaseExtractor):

    def __init__(self):
        # Loads the small Whisper model once
        self.model = whisper.load_model("base")

    def extract(self, file_path: str) -> ExtractionResult:
    
        ffmpeg_path = shutil.which("ffmpeg")

        if ffmpeg_path is None:
            raise FileNotFoundError(
                "FFmpeg is not installed or not available in PATH."
        )

        subprocess.run(
            [ffmpeg_path, "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )

        transcript = self.model.transcribe(file_path)["text"].strip()

        metadata = AudioMetadataExtractor.extract(file_path)

        statistics = StatisticsGenerator.generate(transcript)


        return ExtractionResult(
            file_name=file_path,
            file_type="AUDIO",
            text=transcript,
            metadata=metadata,
            statistics=statistics,
        )