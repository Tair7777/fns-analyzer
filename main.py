import os
import sys
from parsers.upd_parser import UPD_Parser
from parsers.invoice_parser import InvoiceParser
from parsers.egroul_parser import EgrulParser
from parsers.text_parser import TextParser
from analyzer import LegalAnalyzer
from config import DATA_DIR

def parse_document(file_path):
    """Парсит документ на основе его расширения и имени"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.xml':
        # Определяем тип XML по имени файла
        if 'upd' in file_path.lower():
            parser = UPD_Parser(file_path)
        elif 'invoice' in file_path.lower():
            parser = InvoiceParser(file_path)
        elif 'egroul' in file_path.lower() or 'egrul' in file_path.lower():
            parser = EgrulParser(file_path)
        else:
            # Неопознанный XML-файл
            return {'content': open(file_path, 'r', encoding='utf-8').read(), 
                    'validation': {'valid': True, 'error': None}}
                    
        return parser.parse()
    elif ext == '.txt':
        return TextParser(file_path).parse()
    else:
        return {'error': f'Неизвестный или неподдерживаемый формат: {ext}'}

def main():
    # Проверяем, передан ли аргумент командной строки
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        file_path = os.path.join(DATA_DIR, file_name)
    else:
        # По умолчанию берем УПД
        file_path = os.path.join(DATA_DIR, 'upd_example.xml')
    
    # Проверяем, существует ли файл
    if not os.path.exists(file_path):
        print(f"Ошибка: Файл {file_path} не существует")
        return
    
    # Парсим документ
    print(f"Анализируем документ: {file_path}")
    doc_data = parse_document(file_path)
    
    # Проверяем на ошибки
    if 'error' in doc_data:
        print(f"Ошибка при парсинге: {doc_data['error']}")
        return
    
    # Проверяем результаты валидации
    is_valid = doc_data.get('validation', {}).get('valid', True)
    if not is_valid:
        print(f"Предупреждение: Документ не прошел валидацию по XSD-схеме")
        print(f"Причина: {doc_data['validation']['error']}")
    
    # Анализируем с помощью Perplexity API
    analyzer = LegalAnalyzer()
    analysis_result = analyzer.analyze_text(str(doc_data), is_valid)
    
    # Выводим результат
    print("\nРезультаты анализа:")
    print("-" * 50)
    print(analysis_result)
    print("-" * 50)

if __name__ == "__main__":
    main()
