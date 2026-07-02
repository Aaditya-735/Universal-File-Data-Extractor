import json
from dataclasses import asdict
from pathlib import Path


class Exporter:
    
    @staticmethod
    def export_json(result, output_path: str):

        Path(output_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(output_path, "w", encoding="utf-8") as file:

            json.dump(
                asdict(result),
                file,
                indent=4,
                ensure_ascii=False
            )

    @staticmethod
    def export_text(result, output_path: str):

        Path(output_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(output_path, "w", encoding="utf-8") as file:

            file.write(result.text)