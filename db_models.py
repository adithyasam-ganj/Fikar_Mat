import os, enum
from datetime import datetime, date
from typing import Optional

from sqlalchemy import (
    BigInteger, String, Integer, DateTime, Boolean, Text, JSON, Enum,
    ForeignKey, Index, LargeBinary, select, Float, Date
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DB_PATH = os.getenv("FIKARMAT_DB", "D:/Data_Science/LangGraph/fikarmat.db")

##################################### Models ##############################################

class Base(DeclarativeBase):
    pass

class ChatType(enum.Enum):
    private = "private"
    group = "group"
    supergroup = "supergroup"
    channel = "channel"

class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # Telegram user id
    username: Mapped[Optional[str]] = mapped_column(String(64))
    first_seen: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    language_code: Mapped[Optional[str]] = mapped_column(String(8))
    started_bot: Mapped[bool] = mapped_column(Boolean, default=True)
    # nudge related timestamps
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime, index=True)
    last_score_nudge_at: Mapped[Optional[datetime]] = mapped_column(DateTime, index=True)
    exam_date: Mapped[Optional[datetime]] = mapped_column(DateTime, index=True)


class Chat(Base):
    __tablename__ = "chats"
    chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    type: Mapped[ChatType] = mapped_column(Enum(ChatType))
    title: Mapped[Optional[str]] = mapped_column(String(255))
    last_interaction: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.chat_id", ondelete="CASCADE"), index=True)
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger, index=True)  # nullable for bot/system msgs
    ts: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    direction: Mapped[str] = mapped_column(String(8))  # "in" (user->bot) or "out"
    text_hash: Mapped[Optional[str]] = mapped_column(String(64), index=True) # HMAC/SHA-256 hex
    summary_enc: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    rag_used: Mapped[bool] = mapped_column(Boolean, default=False)
    token_usage: Mapped[Optional[dict]] = mapped_column(JSON)

    # sentiment agent fields
    bert_label: Mapped[Optional[str]] = mapped_column(String(16))
    bert_conf: Mapped[Optional[float]] = mapped_column(Float)
    gpt_sentiment: Mapped[Optional[str]] = mapped_column(String(16))
    final_sentiment: Mapped[Optional[str]] = mapped_column(String(16))
    risk_level: Mapped[Optional[str]] = mapped_column(String(8))   # "green/amber/red"
    suicide_mention: Mapped[Optional[bool]] = mapped_column(Boolean)

class Score(Base):
    """
    Monthly average exam score per student.

    - user_id: FK to users.user_id
    - month: first day of that month (e.g., 2025-11-01)
    - avg_score: numeric score for that month (0–100 or whatever scale you pick)
    """
    __tablename__ = "scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), index=True)
    month: Mapped[date] = mapped_column(Date, index=True)
    avg_score: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

Index("ix_messages_chat_ts", Message.chat_id, Message.ts)

class Config(Base):
    __tablename__ = "config"
    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    value: Mapped[str] = mapped_column(Text)