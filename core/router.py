from typing import Callable


class FileRouter:
    
    def __init__(self):
        self.routes: dict[str, Callable] = {}

    def register_route(self, file_type: str, extractor: Callable) -> None:
        
        self.routes[file_type] = extractor

    def get_extractor(self, file_type: str) -> Callable:
       
        extractor = self.routes.get(file_type)

        if extractor is None:
            raise ValueError(
                f"No extractor registered for '{file_type}'"
            )

        return extractor