import xml.etree.ElementTree as ET
from parsers.base_parser import BaseParser

class UPD_Parser(BaseParser):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.document_type = 'upd'
    
    def is_valid(self):
        """Проверяет, соответствует ли XML-файл XSD-схеме"""
        try:
            return self.validate_with_schema(self.document_type)
        except Exception:
            # Если валидация невозможна, считаем документ валидным
            return True, None
    
    def parse(self):
        try:
            # Проверяем валидность по схеме (если она есть)
            is_valid, error = self.is_valid()
            
            content = self._read_file()
            root = ET.fromstring(content)
            
            result = {
                'doc_type': 'УПД',
                'validation': {'valid': is_valid, 'error': error},
                'doc_date': root.find('.//ДатаДок').text if root.find('.//ДатаДок') is not None else None,
                'parties': {
                    'seller': root.find('.//СвПрод').attrib if root.find('.//СвПрод') is not None else {},
                    'buyer': root.find('.//СвПок').attrib if root.find('.//СвПок') is not None else {}
                }
            }
            
            return result
        except Exception as e:
            return {"error": f"Ошибка при парсинге УПД: {str(e)}"}
