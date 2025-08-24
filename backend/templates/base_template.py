from abc import ABC, abstractmethod
from typing import Dict, Any, List
import json
from pathlib import Path


class BaseTemplate(ABC):
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category
        self.components = {}
        self.styles = {}
        self.structure = {}
    
    @abstractmethod
    def get_structure(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_styles(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def render(self, business_data: Dict[str, Any]) -> str:
        pass
    
    def get_component(self, component_name: str) -> str:
        return self.components.get(component_name, "")
    
    def save_to_file(self, content: str, output_path: Path):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding='utf-8')