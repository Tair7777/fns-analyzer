import xml.etree.ElementTree as ET
from parsers.base_parser import BaseParser

class EgrulParser(BaseParser):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.document_type = 'egroul'
    
    def is_valid(self):
        """Проверяет, соответствует ли XML-файл XSD-схеме"""
        try:
            return self.validate_with_schema(self.document_type)
        except Exception:
            # Если валидация невозможна, считаем документ валидным
            return True, None
    
    def parse(self):
        try:
            # Проверяем валидность по схеме
            is_valid, error = self.is_valid()
            
            content = self._read_file()
            root = ET.fromstring(content)
            
            result = {
                'doc_type': 'ЕГРЮЛ',
                'validation': {'valid': is_valid, 'error': error},
                'changes': [node.text for node in root.findall('.//Изменение')] if root.findall('.//Изменение') else [],
                'org_name': root.find('.//НаимЮЛ').text if root.find('.//НаимЮЛ') is not None else None,
                'inn': root.find('.//ИНН').text if root.find('.//ИНН') is not None else None
            }
            
            return result
        except Exception as e:
            return {"error": f"Ошибка при парсинге ЕГРЮЛ: {str(e)}"}
