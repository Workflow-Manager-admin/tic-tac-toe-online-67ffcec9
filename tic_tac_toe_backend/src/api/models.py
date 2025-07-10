from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import enum

Base = declarative_base()

# Enums for game status and player symbol
class GameStatus(str, enum.Enum):
    ACTIVE = "active"
    FINISHED = "finished"

class PlayerSymbol(str, enum.Enum):
    X = "X"
    O = "O"

# PUBLIC_INTERFACE
class User(Base):
    """Database model for application users."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    games_as_x = relationship("Game", back_populates="player_x", foreign_keys='Game.player_x_id')
    games_as_o = relationship("Game", back_populates="player_o", foreign_keys='Game.player_o_id')
    moves = relationship("Move", back_populates="user")
    leaderboard_entry = relationship("Leaderboard", back_populates="user", uselist=False)

# PUBLIC_INTERFACE
class Game(Base):
    """Database model for a Tic Tac Toe game."""
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    player_x_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    player_o_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(GameStatus), default=GameStatus.ACTIVE, nullable=False)
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    player_x = relationship("User", foreign_keys=[player_x_id], back_populates="games_as_x")
    player_o = relationship("User", foreign_keys=[player_o_id], back_populates="games_as_o")
    winner = relationship("User", foreign_keys=[winner_id])
    moves = relationship("Move", back_populates="game", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('player_x_id', 'player_o_id', 'created_at', name='_unique_game'),
    )

# PUBLIC_INTERFACE
class Move(Base):
    """Database model for a move in a Tic Tac Toe game."""
    __tablename__ = "moves"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    move_number = Column(Integer, nullable=False)
    row = Column(Integer, nullable=False)
    col = Column(Integer, nullable=False)
    symbol = Column(Enum(PlayerSymbol), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    game = relationship("Game", back_populates="moves")
    user = relationship("User", back_populates="moves")

    __table_args__ = (
        UniqueConstraint('game_id', 'move_number', name='_unique_game_move_number'),
    )

# PUBLIC_INTERFACE
class Leaderboard(Base):
    """Database model for leaderboard standings."""
    __tablename__ = "leaderboards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    draws = Column(Integer, default=0)
    score = Column(Integer, default=0)

    user = relationship("User", back_populates="leaderboard_entry")
