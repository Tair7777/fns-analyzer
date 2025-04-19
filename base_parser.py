class BaseParser:
    """Базовый класс для всех парсеров в приложении."""
    
    def __init__(self):
        self.data = {}
    
    def parse(self, content):
        """
        Разбор содержимого и возврат структурированных данных.
        
        Args:
            content (str): Содержимое для разбора
            
        Returns:
            dict: Разобранные данные
        """
        raise NotImplementedError("Дочерние классы должны реализовать метод parse()")
    
    def get_data(self):
        """
        Получение разобранных данных.
        
        Returns:
            dict: Разобранные данные
        """
        return self.data
