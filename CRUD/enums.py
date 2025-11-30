from enum import Enum as PyEnum

class NewsType(PyEnum):
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
