from parsers.base_parser import BaseParser
import re

class TextParser(BaseParser):
    """Парсер для текстовых документов."""
    
    def __init__(self):
        super().__init__()
        self.patterns = {
            'inn': r'ИНН\s*[:|=]?\s*(\d{10}|\d{12})',
            'kpp': r'КПП\s*[:|=]?\s*(\d{9})',
            'date': r'от\s*(\d{2}[./-]\d{2}[./-]\d{4})',
            'sum': r'(?:сумма|итого)[:\s]*(?:составляет)?\s*(\d+[\s,.]?\d*)\s*(?:руб|₽)?',
            'document_number': r'(?:документ|счет|накладная)[:\s]*(?:№)?\s*([A-Za-zА-Яа-я0-9-_/]+)'
        }
    
    def parse(self, content):
        """
        Извлекает структурированную информацию из текста.
        
        Args:
            content (str): Текстовое содержимое для анализа
            
        Returns:
            dict: Извлеченные данные
        """
        result = {}
        
        for key, pattern in self.patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                result[key] = match.group(1)
        
        self.data = result
        return result
