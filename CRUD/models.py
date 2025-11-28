from .db import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey


class NewsModel(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, index=True)
    background_image_url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    short_description = Column(Text, nullable=False)

class NewsItemModel(Base):
    __tablename__ = 'news_items'

    id = Column(Integer, primary_key=True, index=True)
    news_id = Column(Integer, ForeignKey('news.id'), nullable=False)
    news_type = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    short_description = Column(Text, nullable=False)
    date = Column(String, nullable=False)
    link_url = Column(String, nullable=False)