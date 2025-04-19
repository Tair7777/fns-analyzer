import xml.etree.ElementTree as ET
from parsers.base_parser import BaseParser

class InvoiceParser(BaseParser):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.document_type = 'invoice'
    
    def is_valid(self):
        try:
            return self.validate_with_schema(self.document_type)
        except Exception:
            return True, None
    
    def parse(self):
        try:
            is_valid, error = self.is_valid()
            
            content = self._read_file()
            root = ET.fromstring(content)
            
            result = {
                'doc_type': 'Счет-фактура',
                'validation': {'valid': is_valid, 'error': error},
                'doc_number': root.find('.//НомерСчФ').text if root.find('.//НомерСчФ') is not None else None,
                'doc_date': root.find('.//ДатаСчФ').text if root.find('.//ДатаСчФ') is not None else None,
                'amount': root.find('.//СумИтого').text if root.find('.//СумИтого') is not None else None
            }
            
            return result
        except Exception as e:
            return {"error": f"Ошибка при парсинге счета-фактуры: {str(e)}"}