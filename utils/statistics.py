from models import Statistics


class StatisticsGenerator:
   
    AVERAGE_READING_SPEED = 200  # words per minute

    @staticmethod
    def generate(text: str) -> Statistics:
        
        text = text.strip()

        if not text:
            return Statistics()

        words = text.split()

        word_count = len(words)

        character_count = len(text)

        line_count = len(text.splitlines())

        paragraphs = [
            p for p in text.split("\n\n")
            if p.strip()
        ]

        paragraph_count = len(paragraphs)

        reading_time = round(
            word_count /
            StatisticsGenerator.AVERAGE_READING_SPEED,
            2
        )

        return Statistics(
            word_count=word_count,
            character_count=character_count,
            line_count=line_count,
            paragraph_count=paragraph_count,
            reading_time_minutes=reading_time,
        )