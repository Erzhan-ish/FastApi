from .db import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from .enums import NewsType

class NewsModel(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    background_image_url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    short_description = Column(Text, nullable=False)

    # One-to-many: News -> many NewsItem
    items = relationship("NewsItemModel", back_populates="news", cascade="all, delete-orphan")

    def __str__(self):
        return self.title

class NewsItemModel(Base):
    __tablename__ = 'news_items'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    news_id = Column(Integer, ForeignKey('news.id'), nullable=False)
    news_type = Column(SQLAlchemyEnum(NewsType), nullable=False) # SQLAlchemyEnum для выпадающего списка
    image_url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    short_description = Column(Text, nullable=False)
    date = Column(String, nullable=False)
    link_url = Column(String, nullable=False)

    # Many-to-one: NewsItem -> News
    news = relationship("NewsModel", back_populates="items")

    def __str__(self):
        return self.title