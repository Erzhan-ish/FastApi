from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey, Enum as SQLAlchemyEnum
from src.db import Base
from src.schemas.enums import NewsType
from sqlalchemy.orm import relationship

class NewsModel(Base):
    __tablename__ = 'news'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    background_image_url: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    short_description: Mapped[str] = mapped_column(Text, nullable=False)

    # One-to-many: News -> many NewsItem
    items: Mapped[list["NewsItemModel"]] = relationship("NewsItemModel", back_populates="news", cascade="all, delete-orphan")

    def __str__(self):
        return self.title


class NewsItemModel(Base):
    __tablename__ = 'news_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey('news.id'), nullable=False)
    news_type: Mapped[NewsType] = mapped_column(SQLAlchemyEnum(NewsType), nullable=False)  # SQLAlchemyEnum для выпадающего списка
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    short_description: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[str] = mapped_column(String, nullable=False)
    link_url: Mapped[str] = mapped_column(String, nullable=False)

    # Many-to-one: NewsItem -> News
    news: Mapped["NewsModel"] = relationship("NewsModel", back_populates="items")

    def __str__(self):
        return self.title
