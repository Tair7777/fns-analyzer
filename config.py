import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# API Perplexity
API_KEY = os.getenv('PERPLEXITY_API_KEY')
API_URL = "https://api.perplexity.ai/chat/completions"

# Пути к директориям
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "data")
SCHEMA_DIR = os.path.join(ROOT_DIR, "schemas")

# Маппинг типов документов на схемы XSD
SCHEMA_MAPPING = {
    'upd': 'upd/ON_NSCHFDOPPR_1_997_01_05_03_02.xsd',
    'invoice': 'invoice/invoice_schema.xsd',
    'egroul': 'egroul/egroul_schema.xsd',
    'ndfl': 'ndfl/ON_NDFL3_1_000_00_05_03_02.xsd',
    'unknown': 'upd/ON_NSCHFDOPPR_1_997_01_05_03_02.xsd'  # Схема по умолчанию
}
