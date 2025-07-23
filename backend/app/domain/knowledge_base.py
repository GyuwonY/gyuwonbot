from enum import Enum
from sqlalchemy import Integer, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from typing import Optional, List
from datetime import datetime

Base = declarative_base()


class SourceTypeEnum(Enum):
    QNA = "qna"
    RESUME = "resume"


class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    source_type: Mapped[SourceTypeEnum] = mapped_column(
        PGEnum(
            SourceTypeEnum,
            values_callable=lambda x: [e.value for e in x],
            name="source_type",
            create_type=True
        ),
        nullable=False,
    )
    
    q_id: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
    )

    persona: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    topic: Mapped[str] = mapped_column(String(100), nullable=False)

    question: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    embedding: Mapped[List[float]] = mapped_column(Vector(1536), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
