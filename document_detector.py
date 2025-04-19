class DocumentDetector:
    """
    Определение типа документа ФНС на основе его содержимого
    """
    def detect_document_type(self, content):
        """
        Определяет тип документа на основе его структуры
        
        :param content: содержимое документа
        :return: тип документа ('upd', 'ndfl', 'egroul', 'invoice', 'unknown')
        """
        if '<Файл ИдФайл="ON_NSCHFDOPPR' in content or '<СвСчФакт' in content:
            return 'upd'
        elif '<Файл ИдФайл="NO_NDFL' in content:
            return 'ndfl'
        elif '<ЕГРЮЛ' in content:
            return 'egroul'
        elif '<Invoice' in content or '<СчетФактура' in content:
            return 'invoice'
        else:
            return 'unknown'
