from abc import ABC, abstractmethod
from typing import Any


class BaseExtractor(ABC):
    
    @abstractmethod
    def extract(self, file_path: str) -> dict[str, Any]:
        
        pass