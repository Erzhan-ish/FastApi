from enum import Enum

class NewsType(str, Enum):
    news = "news"
    announcement = "announcement"
    report = "report"
    press = "press"

    @property
    def label(self):
        return {
            "news": "Новость",
            "announcement": "Анонс",
            "report": "Отчёт",
            "press": "Пресс-релиз"
        }[self.value]
