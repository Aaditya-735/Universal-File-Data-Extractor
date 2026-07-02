from dataclasses import dataclass


@dataclass(slots=True)
class Metadata:
  
    author: str = ""
    title: str = ""
    subject: str = ""
    creator: str = ""
    producer: str = ""

    page_count: int = 0

    creation_date: str = ""
    modification_date: str = ""

    file_size: int = 0