import requests
import os
import time
import json
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

class LegalAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def analyze_text(self, text: str, max_retries: int = 3) -> dict:
        """
        Анализирует текст документа через Perplexity API с расширенным саммори для разработчиков
        """
        # Улучшенный промпт с акцентом на бизнес-требования и методологию
        prompt = f"""Ты старший технический аналитик с опытом интеграции с ФНС России. 
Проанализируй XML-документ ФНС и создай подробное техническое саммори для разработчиков интеграционных решений.

Обязательно структурируй анализ по следующим разделам:

### Тип документа
Определи точно какой это документ ФНС (УПД, счет-фактура, декларация 3-НДФЛ и т.д.). Укажи версию формата.

### Бизнес-назначение
Подробно опиши бизнес-цель документа, какие хозяйственные операции он отражает и в каких бизнес-процессах используется.

### Нормативная база
Укажи приказы ФНС, НК РФ и другие НПА, которые регламентируют формат и применение этого документа.

### Ключевые реквизиты
Перечисли важнейшие атрибуты и элементы, их назначение и обязательность заполнения.

### Сроки и даты
Опиши все критические даты из документа (дата формирования, период и т.д.) и их значение.

### Технические особенности формата
Опиши структуру документа, ключевые элементы XML. Укажи возможные проблемы интеграции.

### Бизнес-требования для разработчиков
Четко перечисли требования к обработке документа в информационных системах, включая:
- Требования к валидации
- Алгоритмы расчетов, если применимо
- Требования к сохранению и предоставлению данных

### Интеграционная схема
Опиши типичный процесс интеграции с системами ФНС для данного документа. Включи точки обмена данными.

### Типичные ошибки интеграции
Перечисли распространенные ошибки при работе с этим типом документа и их решения.

### Резюме
Краткий итог о документе (3-5 предложений), выделяющий ключевые аспекты.

XML-документ:
{text[:5000]}
"""

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.base_url,
                    headers=self.headers,
                    json={
                        "model": "llama-3.1-sonar-small-128k-online",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.1,  # Снижаем температуру для более точных ответов
                        "max_tokens": 4000   # Увеличиваем длину ответа
                    },
                    timeout=60  # Увеличенный таймаут
                )
                
                if response.status_code == 200:
                    content = response.json()['choices'][0]['message']['content']
                    return {
                        'analysis': content,
                        'sources': []
                    }
                
                if response.status_code == 429:
                    wait_time = (2 ** attempt) + 1
                    time.sleep(wait_time)
                    continue
                
                error_msg = response.json().get('error', {}).get('message', 'Неизвестная ошибка API')
                return {
                    'analysis': f"Ошибка {response.status_code}: {error_msg}",
                    'sources': []
                }

            except Exception as e:
                if attempt == max_retries - 1:
                    return {
                        'analysis': f"Ошибка при анализе: {str(e)}",
                        'sources': []
                    }
                time.sleep(2)
        
        return {
            'analysis': "Не удалось получить ответ после нескольких попыток",
            'sources': []
        }
    
    def answer_question(self, document_context, question):
        """
        Отвечает на вопрос о документе с улучшенной надежностью
        """
        prompt = f"""Как эксперт по налоговому законодательству РФ и интеграции с ФНС, ответь детально на вопрос о документе.
Твой ответ должен содержать:
1. Конкретные данные из документа
2. Ссылки на нормативную базу
3. Технические детали для разработчиков, где уместно

Контекст документа:
{document_context}

Вопрос: {question}
"""
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": "llama-3.1-sonar-small-128k-online",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                    "max_tokens": 2000
                },
                timeout=60
            )
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    return result['choices'][0]['message']['content']
                except (KeyError, IndexError, json.JSONDecodeError) as e:
                    return f"Ошибка при обработке ответа API: {str(e)}"
            else:
                return f"Ошибка API (код {response.status_code})"
                
        except Exception as e:
            return f"Произошла ошибка: {str(e)}"
