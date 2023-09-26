from abc import ABC, abstractmethod

# Абстрактний клас для інформаційних вікон
class View(ABC):
    def __init__(self):
        self.data = None

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def save(self):
        pass

# Конкретна реалізація для вікна контактів
class ContactView(View):
    def __init__(self):
        super().__init__()

    def display(self):
        # Логіка для відображення контактів користувача
        pass

    def save(self):
        # Логіка для збереження контактів користувача
        pass

# Конкретна реалізація для вікна нотаток
class NoteView(View):
    def __init__(self):
        super().__init__()

    def display(self):
        # Логіка для відображення нотаток
        pass

    def save(self):
        # Логіка для збереження нотаток
        pass

# Конкретна реалізація для вікна команд
class CommandView(View):
    def __init__(self):
        super().__init__()

    def display(self):
        # Логіка для відображення доступних команд
        pass

    def save(self):
        # Логіка для збереження історії команд
        pass
