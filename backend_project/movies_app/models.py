
from sqlalchemy import Column, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base


class Base:
    """Base model class for resources."""

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


DeclarativeBase = declarative_base(cls=Base)
