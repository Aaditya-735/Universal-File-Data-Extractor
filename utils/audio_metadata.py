from mutagen import File
from pathlib import Path


class AudioMetadataExtractor:

    @staticmethod
    def extract(file_path: str) -> dict:

        metadata = {}

        audio = File(file_path)

        metadata["File Size"] = f"{Path(file_path).stat().st_size} bytes"

        if audio is None:
            return metadata

        if audio.info:

            metadata["Duration"] = f"{audio.info.length:.2f} sec"

            if hasattr(audio.info, "bitrate"):
                metadata["Bitrate"] = f"{audio.info.bitrate // 1000} kbps"

            if hasattr(audio.info, "sample_rate"):
                metadata["Sample Rate"] = f"{audio.info.sample_rate} Hz"

            if hasattr(audio.info, "channels"):
                metadata["Channels"] = audio.info.channels

        return metadata