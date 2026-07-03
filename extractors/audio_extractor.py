import os
import whisper
import shutil
import subprocess

from extractors.base_extractor import BaseExtractor
from models import ExtractionResult
from utils.audio_metadata import AudioMetadataExtractor
from utils.statistics import StatisticsGenerator




 

class AudioExtractor(BaseExtractor):

    def __init__(self):
        # Loads the small Whisper model once
        self.model = whisper.load_model("base")

    def extract(self, file_path: str) -> ExtractionResult:
    
        FFMPEG_PATH = shutil.which("ffmpeg")

        if FFMPEG_PATH is None:
            FFMPEG_PATH = r"C:\Users\AG\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe"

        os.environ["PATH"] += os.pathsep + os.path.dirname(FFMPEG_PATH)

        subprocess.run([FFMPEG_PATH, "-version"])

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