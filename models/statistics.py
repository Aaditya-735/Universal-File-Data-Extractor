from dataclasses import dataclass


@dataclass(slots=True)
class Statistics:
   
    word_count: int = 0

    character_count: int = 0

    line_count: int = 0

    paragraph_count: int = 0

    reading_time_minutes: float = 0.0